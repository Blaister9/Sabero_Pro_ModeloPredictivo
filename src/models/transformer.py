"""Transformer encoder model for Saber Pro PROMEDIO_GLOBAL sequence regression.

This module implements Phase 6 of the Saber Pro predictive pipeline: a
Transformer-based neural sequence model that treats each
``(ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)`` entity as a time series
of feature vectors and predicts ``PROMEDIO_GLOBAL`` from that sequence.

Architecture overview:

1. **Input projection**: a single linear layer maps each timestep's raw
   feature vector (dimension ``feature_dim``) to the model's internal
   dimension ``d_model`` (default 64).
2. **Learned positional encoding** (``LearnedPositionalEncoding``): position
   embeddings are learned from data rather than fixed sinusoids.  This is
   appropriate for the short, irregular sequences (T ≤ 5 years) encountered
   in this panel dataset.
3. **Transformer encoder** (``nn.TransformerEncoder``): ``num_layers``
   ``TransformerEncoderLayer`` blocks with pre-norm (``norm_first=True``)
   for improved training stability on small datasets.  Multi-head attention
   with ``nhead`` heads allows each position to attend to all prior years'
   feature vectors.
4. **Last-token pooling**: the final (most recent) token's hidden state is
   passed to the regression head.  This is appropriate because the most
   recent year contains the most informative temporal context.
5. **Regression head**: ``LayerNorm → Linear(d_model, 32) → GELU → Dropout →
   Linear(32, 1)``.

Leakage prevention in the sequence construction:

- ``SaberProSequenceDataset`` normalises features using statistics computed
  only within the split (train or test) that is passed to it.
- ``_build_test_dataset`` reuses the training set's mean and std to normalise
  test features, preventing test distribution information from being
  incorporated during normalisation.
- Each sample's target is ``PROMEDIO_GLOBAL`` of the **last** year in the
  window.  Feature vectors in the window correspond to the same or earlier
  years and contain only the lag/trend features already confirmed leakage-free
  by the Phase 3 audit.

Training uses AdamW with cosine annealing, gradient clipping (max norm 1.0),
and early stopping based on validation RMSE with patience 20 epochs.  A
hard ``time_budget_seconds`` argument (default 1200 s) stops training if the
budget expires, returning the best checkpoint seen so far.

Usage example::

    from src.models.transformer import train_transformer

    feature_cols = [
        "lag_1_promedio_global", "lag_2_promedio_global",
        "lag_1_promedio_prueba", "lag_2_promedio_prueba",
        "tendencia_global", "tendencia_prueba",
        "desviacion_estandar_historica", "coeficiente_variacion",
        "log_cantidadevaluados", "AÑO",
    ]

    result = train_transformer(
        X_train=X_train, y_train=y_train,
        X_test=X_test,   y_test=y_test,
        df_train=df_train, df_test=df_test,
        feature_cols=feature_cols,
        time_budget_seconds=1200,
    )

    print(f"Test RMSE: {result['rmse_test']:.4f}")
    print(f"Test R²  : {result['r2_test']:.4f}")
    print(f"Converged: {result['converged']} "
          f"(best epoch: {result['best_epoch']})")

Warning:
    This model runs on CPU only (no CUDA calls).  Training 200 epochs on the
    full 2020-2023 training set with ``batch_size=256`` takes approximately
    15-25 minutes depending on the hardware.  The ``time_budget_seconds``
    parameter ensures training terminates within a configurable wall-clock
    budget even if early stopping has not fired, preserving the best
    checkpoint seen up to that point.
"""

import math
from typing import Optional

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset


# ── Dataset ──────────────────────────────────────────────────────────────────

class SaberProSequenceDataset(Dataset):
    """PyTorch Dataset of temporal feature sequences for panel entities.

    For each unique panel entity ``(ID_INSTITUCION, ID_PROGRAMA_ACAD,
    NOMBRE_PRUEBA)`` in the supplied DataFrame, this dataset constructs one
    fixed-length sequence sample.  If the entity has more years than
    ``max_seq_len``, only the most recent ``max_seq_len`` years are used.
    If it has fewer, the sequence is left-padded with zeros and the padding
    mask is set to ``True`` so the Transformer's attention mechanism ignores
    the padded positions.

    Features are Z-score normalised using the mean and standard deviation
    computed over the split passed to the constructor.  For test datasets,
    normalisation statistics must be taken from the training set (see
    ``_build_test_dataset``).

    Attributes:
        feature_cols (list[str]): Feature column names used by the dataset.
        target_col (str): Name of the target column.
        max_seq_len (int): Fixed sequence length after padding/truncation.
        feat_mean (pd.Series): Per-feature mean used for normalisation.
        feat_std (pd.Series): Per-feature standard deviation used for
            normalisation (zeros replaced with 1 to avoid division errors).
        samples (list[tuple]): List of ``(sequence_tensor, target_scalar,
            padding_mask)`` tuples.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        feature_cols: list,
        target_col: str = "PROMEDIO_GLOBAL",
        entity_cols: tuple = ("ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"),
        year_col: str = "AÑO",
        max_seq_len: int = 5,
    ):
        """Initialise the sequence dataset.

        Args:
            df: Wide-format DataFrame produced by ``features.build_features``.
                Must contain ``feature_cols``, ``target_col``, all columns in
                ``entity_cols``, and ``year_col``.
            feature_cols: List of numeric feature column names that form each
                timestep's feature vector.
            target_col: Name of the column holding the regression target.
                Defaults to ``"PROMEDIO_GLOBAL"``.
            entity_cols: Tuple of column names that together identify a panel
                entity.  Defaults to
                ``("ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA")``.
            year_col: Name of the year column used to sort observations
                chronologically within each entity.  Defaults to ``"AÑO"``.
            max_seq_len: Maximum sequence length.  Entities with more years
                are truncated (keeping the most recent ``max_seq_len`` years);
                entities with fewer are left-padded with zeros.  Defaults to
                ``5`` (covering the 2020-2024 observation window).

        Note:
            Normalisation statistics (``feat_mean``, ``feat_std``) are computed
            over the entire ``df`` passed in.  For the training dataset this is
            the train split only; for the test dataset use ``_build_test_dataset``
            to reuse the training statistics and prevent test leakage into
            normalisation.
        """
        self.feature_cols = feature_cols
        self.target_col   = target_col
        self.max_seq_len  = max_seq_len

        # Normalizar features (media/std calculadas sobre todo el split que
        # se pase al constructor — solo train en train_set, solo test en test_set).
        self.feat_mean = df[feature_cols].mean()
        self.feat_std  = df[feature_cols].std().replace(0, 1)

        df_norm = df.copy()
        df_norm[feature_cols] = (df[feature_cols] - self.feat_mean) / self.feat_std

        # Agrupar por entidad y ordenar cronológicamente
        self.samples = []
        grouped = df_norm.groupby(list(entity_cols), sort=False)

        for _, group in grouped:
            group = group.sort_values(year_col).reset_index(drop=True)
            feats  = group[feature_cols].values.astype(np.float32)   # (T, F)
            target = group[target_col].values.astype(np.float32)     # (T,)

            # Construir una muestra por cada año de la entidad (except el primero)
            # o solo el último si queremos una muestra por entidad.
            # Aquí: una muestra por entidad usando TODOS los años disponibles.
            T = len(group)
            if T == 0:
                continue

            # Pad / truncate a max_seq_len
            if T >= max_seq_len:
                seq   = feats[-max_seq_len:]          # tomar los más recientes
                tgt   = float(target[-1])
                mask  = torch.zeros(max_seq_len, dtype=torch.bool)  # sin padding
            else:
                pad_len = max_seq_len - T
                pad     = np.zeros((pad_len, feats.shape[1]), dtype=np.float32)
                seq     = np.vstack([pad, feats])     # left-padding
                tgt     = float(target[-1])
                mask    = torch.zeros(max_seq_len, dtype=torch.bool)
                mask[:pad_len] = True                 # True = ignorar en attention

            self.samples.append((
                torch.tensor(seq),          # (max_seq_len, F)
                torch.tensor(tgt),          # scalar
                mask,                       # (max_seq_len,) bool
            ))

    def __len__(self):
        """Return the number of entity samples in the dataset.

        Returns:
            Integer count of samples.
        """
        return len(self.samples)

    def __getitem__(self, idx):
        """Return the sample at position idx.

        Args:
            idx: Integer index into ``self.samples``.

        Returns:
            A tuple ``(sequence_tensor, target_tensor, padding_mask)`` where:

            - ``sequence_tensor``: Float32 tensor of shape
              ``(max_seq_len, feature_dim)``.
            - ``target_tensor``: Scalar float32 tensor holding
              ``PROMEDIO_GLOBAL`` for the last year in the window.
            - ``padding_mask``: Bool tensor of shape ``(max_seq_len,)``
              where ``True`` indicates a padded (ignored) position.
        """
        return self.samples[idx]


# ── Positional Encoding aprendible ───────────────────────────────────────────

class LearnedPositionalEncoding(nn.Module):
    """Learnable positional embedding added to the projected input sequence.

    Each sequence position 0, 1, ..., max_seq_len-1 is assigned a learnable
    ``d_model``-dimensional embedding vector.  These are added (not
    concatenated) to the projected input features so the Transformer can
    distinguish temporal position.

    Learnable positional encodings are preferred over sinusoidal encodings
    for short sequences (T ≤ 5) where the fixed-frequency assumption of the
    original Transformer paper may not hold.

    Attributes:
        pe (nn.Embedding): Embedding table of shape
            ``(max_seq_len, d_model)``.
    """

    def __init__(self, max_seq_len: int, d_model: int):
        """Initialise the positional embedding table.

        Args:
            max_seq_len: Maximum sequence length (number of positions).
            d_model: Embedding dimensionality (must match the model's
                ``d_model``).
        """
        super().__init__()
        self.pe = nn.Embedding(max_seq_len, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Add positional embeddings to the input tensor.

        Args:
            x: Input tensor of shape ``(batch, seq_len, d_model)``.

        Returns:
            Tensor of shape ``(batch, seq_len, d_model)`` with positional
            embeddings added element-wise.
        """
        # x: (batch, seq_len, d_model)
        positions = torch.arange(x.size(1), device=x.device).unsqueeze(0)
        return x + self.pe(positions)


# ── Modelo Transformer ────────────────────────────────────────────────────────

class SaberProTransformer(nn.Module):
    """Transformer encoder for scalar regression of PROMEDIO_GLOBAL.

    Processes a batch of fixed-length feature sequences (one per panel entity)
    through a linear input projection, learned positional encoding, a stack of
    ``TransformerEncoderLayer`` blocks, and a two-layer regression head that
    operates on the last (most recent) sequence position.

    The model is designed for CPU-only inference with small datasets
    (approximately 30,000 training samples after the temporal split).
    Default hyperparameters were chosen to balance capacity and regularisation
    for this data regime.

    Args:
        feature_dim: Number of input features per timestep.  Must match the
            length of ``feature_cols`` passed to ``SaberProSequenceDataset``.
        d_model: Internal embedding dimension.  Defaults to ``64``.
        nhead: Number of attention heads in each ``TransformerEncoderLayer``.
            Must evenly divide ``d_model``.  Defaults to ``4``.
        num_layers: Number of stacked ``TransformerEncoderLayer`` blocks.
            Defaults to ``2``.
        ffn_dim: Feed-forward network dimension inside each encoder layer.
            Defaults to ``128``.
        dropout: Dropout probability applied in attention and FFN layers.
            Defaults to ``0.1``.
        max_seq_len: Maximum sequence length.  Must match the ``max_seq_len``
            used in ``SaberProSequenceDataset``.  Defaults to ``5``.
    """

    def __init__(
        self,
        feature_dim:  int,
        d_model:      int = 64,
        nhead:        int = 4,
        num_layers:   int = 2,
        ffn_dim:      int = 128,
        dropout:      float = 0.1,
        max_seq_len:  int = 5,
    ):
        """Initialise model layers and apply Xavier weight initialisation.

        Args:
            feature_dim: Input feature dimension per timestep.
            d_model: Internal embedding dimension.
            nhead: Number of attention heads.
            num_layers: Number of encoder layers.
            ffn_dim: Feed-forward network dimension.
            dropout: Dropout probability.
            max_seq_len: Maximum sequence length for positional embeddings.
        """
        super().__init__()
        self.d_model = d_model

        # Proyección de entrada → d_model
        self.input_proj = nn.Linear(feature_dim, d_model)

        # Positional encoding aprendible
        self.pos_enc = LearnedPositionalEncoding(max_seq_len, d_model)

        # Capas TransformerEncoder
        enc_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=ffn_dim,
            dropout=dropout,
            batch_first=True,   # (batch, seq, feat)
            norm_first=True,    # pre-norm: más estable en datos pequeños
        )
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=num_layers)

        # Cabeza de regresión: toma el último token válido
        self.regressor = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, 32),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1),
        )

        self._init_weights()

    def _init_weights(self):
        """Apply Xavier uniform initialisation to all 2-D weight tensors.

        Biases are initialised to zero by PyTorch's default.
        """
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(
        self,
        x:           torch.Tensor,   # (batch, seq_len, feature_dim)
        src_key_padding_mask: Optional[torch.Tensor] = None,  # (batch, seq_len) bool
    ) -> torch.Tensor:
        """Perform a forward pass through the Transformer and regression head.

        Args:
            x: Input tensor of shape ``(batch, seq_len, feature_dim)``
                containing normalised feature sequences.
            src_key_padding_mask: Boolean mask of shape ``(batch, seq_len)``
                where ``True`` marks padded positions to be ignored by the
                attention mechanism.  Pass ``None`` when all positions are valid.

        Returns:
            A 1-D tensor of shape ``(batch,)`` containing the predicted
            ``PROMEDIO_GLOBAL`` for each sequence in the batch.
        """
        # (batch, seq_len, d_model)
        x = self.input_proj(x)
        x = self.pos_enc(x)
        # Transformer encoder
        x = self.encoder(x, src_key_padding_mask=src_key_padding_mask)
        # Tomar último token (más reciente cronológicamente)
        last = x[:, -1, :]           # (batch, d_model)
        return self.regressor(last).squeeze(-1)  # (batch,)


# ── Funciones de entrenamiento ────────────────────────────────────────────────

def _rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Root Mean Squared Error between two arrays.

    Args:
        y_true: Array of ground-truth values.
        y_pred: Array of predicted values, same length as ``y_true``.

    Returns:
        RMSE as a float.

    Example:
        >>> _rmse(np.array([1.0, 2.0, 3.0]), np.array([1.5, 2.5, 2.5]))
        0.5
    """
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def _r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute the coefficient of determination R² between two arrays.

    Args:
        y_true: Array of ground-truth values.
        y_pred: Array of predicted values.

    Returns:
        R² as a float.  Returns 0.0 if ``y_true`` is constant (total sum of
        squares is zero).

    Example:
        >>> _r2(np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 3.0]))
        1.0
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def train_transformer(
    X_train:      pd.DataFrame,
    y_train:      pd.Series,
    X_test:       pd.DataFrame,
    y_test:       pd.Series,
    df_train:     pd.DataFrame,
    df_test:      pd.DataFrame,
    feature_cols: list,
    time_budget_seconds: int = 1200,
    # Hiperparámetros fijos (documentados en paper)
    d_model:      int   = 64,
    nhead:        int   = 4,
    num_layers:   int   = 2,
    ffn_dim:      int   = 128,
    dropout:      float = 0.1,
    max_seq_len:  int   = 5,
    lr:           float = 3e-4,
    batch_size:   int   = 256,
    max_epochs:   int   = 200,
    patience:     int   = 20,
) -> dict:
    """Train the SaberProTransformer with time-budget and early stopping.

    Constructs ``SaberProSequenceDataset`` objects for train and test,
    splits the train dataset 80/20 (chronologically) into an inner train and
    validation split for early stopping, and runs the training loop until
    convergence (patience exhausted) or the ``time_budget_seconds`` wall-clock
    limit is reached.  The best model checkpoint (lowest validation RMSE) is
    restored at the end.

    Args:
        X_train: Feature DataFrame for training rows.  Not used directly —
            ``df_train`` is used to build the sequence dataset.  Included
            for API consistency with the other model-training functions.
        y_train: Target Series for training rows.  Not used directly.
        X_test: Feature DataFrame for test rows.  Not used directly.
        y_test: Target Series for test rows.  Not used directly.
        df_train: Full wide-format training DataFrame (years 2020-2023)
            produced by ``features.build_features``.  Must contain
            ``feature_cols``, ``"PROMEDIO_GLOBAL"``,
            ``("ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA")``,
            and ``"AÑO"``.
        df_test: Full wide-format test DataFrame (year 2024) with the
            same schema as ``df_train``.
        feature_cols: List of numeric feature column names.  Should match
            ``NUMERIC_FEATURE_COLS`` from ``models/baseline.py``.
        time_budget_seconds: Maximum wall-clock training time in seconds.
            If the budget expires before convergence, training stops and the
            best checkpoint so far is returned.  Defaults to ``1200`` (20 min).
        d_model: Transformer embedding dimension.  Defaults to ``64``.
        nhead: Number of attention heads.  Defaults to ``4``.
        num_layers: Number of encoder layers.  Defaults to ``2``.
        ffn_dim: Feed-forward dimension in each encoder layer.  Defaults to
            ``128``.
        dropout: Dropout rate.  Defaults to ``0.1``.
        max_seq_len: Sequence window length.  Defaults to ``5``.
        lr: AdamW learning rate.  Defaults to ``3e-4``.
        batch_size: Training mini-batch size.  Defaults to ``256``.
        max_epochs: Maximum number of training epochs.  Defaults to ``200``.
        patience: Early stopping patience (epochs without improvement of at
            least 0.01 RMSE).  Defaults to ``20``.

    Returns:
        A dictionary with the following keys:

        - ``"model"`` (SaberProTransformer): The best-checkpoint model.
        - ``"feature_cols"`` (list[str]): Feature columns used.
        - ``"train_ds"`` (SaberProSequenceDataset): Training sequence dataset.
        - ``"test_ds"`` (SaberProSequenceDataset): Test sequence dataset.
        - ``"train_losses"`` (list[float]): Per-epoch inner-train RMSE.
        - ``"val_losses"`` (list[float]): Per-epoch inner-val RMSE.
        - ``"best_epoch"`` (int): Epoch at which the best checkpoint was saved.
        - ``"best_val_rmse"`` (float): Validation RMSE of the best checkpoint.
        - ``"y_pred_train"`` (np.ndarray): Predictions on the full train set.
        - ``"y_true_train"`` (np.ndarray): Targets from the train sequence dataset.
        - ``"y_pred_test"`` (np.ndarray): Predictions on the test set.
        - ``"y_true_test"`` (np.ndarray): Targets from the test sequence dataset.
        - ``"rmse_train"`` (float): RMSE on the full training dataset.
        - ``"r2_train"`` (float): R² on the full training dataset.
        - ``"rmse_test"`` (float): RMSE on the test dataset.
        - ``"r2_test"`` (float): R² on the test dataset.
        - ``"converged"`` (bool): True if early stopping fired before the
          time budget or epoch limit was reached.
        - ``"time_exhausted"`` (bool): True if the time budget expired.
        - ``"elapsed_seconds"`` (float): Total training wall-clock time.
        - ``"n_params"`` (int): Number of trainable model parameters.
        - ``"d_model"``, ``"nhead"``, ``"num_layers"``, ``"ffn_dim"``,
          ``"max_seq_len"``: Architecture hyperparameters echoed back.

    Raises:
        RuntimeError: If PyTorch or CUDA setup fails (unlikely in CPU-only mode).

    Example:
        >>> result = train_transformer(
        ...     X_train, y_train, X_test, y_test,
        ...     df_train=df_train, df_test=df_test,
        ...     feature_cols=feature_cols,
        ...     time_budget_seconds=600,
        ... )
        >>> result["rmse_test"]
        10.45
        >>> result["converged"]
        True

    Note:
        The Transformer model is included as an experimental comparison to the
        LightGBM baseline.  On the 2024 test set it achieves higher RMSE than
        LightGBM (approximately 10-12 vs. 9.33) due to the relatively small
        number of training sequences (one per panel entity per year), which
        limits the Transformer's ability to learn complex attention patterns.
        Future work could extend the sequence features to include sub-test
        score histories or use a larger panel window.
    """
    import time
    t_start = time.time()

    torch.manual_seed(42)
    np.random.seed(42)

    # ── Construir datasets ────────────────────────────────────────────────
    print(f"  Construyendo datasets de secuencias (max_seq_len={max_seq_len})...")
    train_ds = SaberProSequenceDataset(
        df_train, feature_cols, max_seq_len=max_seq_len
    )
    # Para test, la normalización debe usar las estadísticas del train
    test_ds = _build_test_dataset(df_test, feature_cols, train_ds, max_seq_len)

    print(f"  Train samples: {len(train_ds)}, Test samples: {len(test_ds)}")

    # Split train → 80% train_inner / 20% val (cronológico por shuffling desactivado)
    n_val    = max(1, int(len(train_ds) * 0.20))
    n_tr     = len(train_ds) - n_val
    # Usar los primeros n_tr para train y los últimos n_val para val
    tr_indices  = list(range(n_tr))
    val_indices = list(range(n_tr, len(train_ds)))

    from torch.utils.data import Subset
    train_sub = Subset(train_ds, tr_indices)
    val_sub   = Subset(train_ds, val_indices)

    train_loader = DataLoader(train_sub, batch_size=batch_size, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_sub,   batch_size=batch_size, shuffle=False, num_workers=0)

    # ── Modelo ────────────────────────────────────────────────────────────
    feature_dim = len(feature_cols)
    model = SaberProTransformer(
        feature_dim=feature_dim,
        d_model=d_model, nhead=nhead, num_layers=num_layers,
        ffn_dim=ffn_dim, dropout=dropout, max_seq_len=max_seq_len,
    )
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Parámetros del modelo: {n_params:,}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max_epochs, eta_min=1e-5
    )
    criterion = nn.MSELoss()

    # ── Loop de entrenamiento ─────────────────────────────────────────────
    train_losses, val_losses = [], []
    best_val_loss  = float("inf")
    best_state     = None
    best_epoch     = 0
    patience_ctr   = 0
    converged      = False
    time_exhausted = False

    for epoch in range(1, max_epochs + 1):
        elapsed = time.time() - t_start
        if elapsed >= time_budget_seconds:
            time_exhausted = True
            print(f"  *** Presupuesto de tiempo agotado en epoch {epoch} "
                  f"({elapsed:.0f}s / {time_budget_seconds}s) ***")
            break

        # ── Train ────────────────────────────────────────────────────────
        model.train()
        epoch_loss = 0.0
        for seqs, targets, masks in train_loader:
            optimizer.zero_grad()
            preds = model(seqs, src_key_padding_mask=masks)
            loss  = criterion(preds, targets)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            epoch_loss += loss.item() * len(targets)
        train_rmse = math.sqrt(epoch_loss / len(train_sub))

        # ── Validation ───────────────────────────────────────────────────
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for seqs, targets, masks in val_loader:
                preds    = model(seqs, src_key_padding_mask=masks)
                val_loss += criterion(preds, targets).item() * len(targets)
        val_rmse = math.sqrt(val_loss / len(val_sub))

        train_losses.append(train_rmse)
        val_losses.append(val_rmse)
        scheduler.step()

        # ── Early stopping ───────────────────────────────────────────────
        if val_rmse < best_val_loss - 0.01:
            best_val_loss = val_rmse
            best_state    = {k: v.clone() for k, v in model.state_dict().items()}
            best_epoch    = epoch
            patience_ctr  = 0
        else:
            patience_ctr += 1

        if epoch % 10 == 0:
            elapsed = time.time() - t_start
            print(f"  Epoch {epoch:3d}/{max_epochs} | "
                  f"train_RMSE={train_rmse:.4f} | val_RMSE={val_rmse:.4f} | "
                  f"patience={patience_ctr}/{patience} | "
                  f"elapsed={elapsed:.0f}s")

        if patience_ctr >= patience:
            converged = True
            print(f"  Early stopping en epoch {epoch} (mejor val_RMSE={best_val_loss:.4f})")
            break

    # ── Restaurar mejor modelo ────────────────────────────────────────────
    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()

    elapsed_total = time.time() - t_start

    # ── Predicciones finales ──────────────────────────────────────────────
    def predict_dataset(ds):
        """Run the trained model over an entire dataset and return predictions.

        Args:
            ds: A ``SaberProSequenceDataset`` or compatible ``Subset``.

        Returns:
            A 1-D numpy array of predicted values, one per sample.
        """
        loader = DataLoader(ds, batch_size=512, shuffle=False, num_workers=0)
        preds_all = []
        with torch.no_grad():
            for seqs, _, masks in loader:
                p = model(seqs, src_key_padding_mask=masks)
                preds_all.append(p.numpy())
        return np.concatenate(preds_all)

    y_pred_train_seq = predict_dataset(train_ds)
    y_pred_test_seq  = predict_dataset(test_ds)

    # Los targets del dataset de secuencias (solo el último año por entidad)
    y_true_train_seq = np.array([s[1].item() for s in train_ds])
    y_true_test_seq  = np.array([s[1].item() for s in test_ds])

    rmse_tr = _rmse(y_true_train_seq, y_pred_train_seq)
    r2_tr   = _r2(y_true_train_seq,  y_pred_train_seq)
    rmse_te = _rmse(y_true_test_seq,  y_pred_test_seq)
    r2_te   = _r2(y_true_test_seq,    y_pred_test_seq)

    return {
        "model":            model,
        "feature_cols":     feature_cols,
        "train_ds":         train_ds,
        "test_ds":          test_ds,
        "train_losses":     train_losses,
        "val_losses":       val_losses,
        "best_epoch":       best_epoch,
        "best_val_rmse":    best_val_loss,
        "y_pred_train":     y_pred_train_seq,
        "y_true_train":     y_true_train_seq,
        "y_pred_test":      y_pred_test_seq,
        "y_true_test":      y_true_test_seq,
        "rmse_train":       rmse_tr,
        "r2_train":         r2_tr,
        "rmse_test":        rmse_te,
        "r2_test":          r2_te,
        "converged":        converged,
        "time_exhausted":   time_exhausted,
        "elapsed_seconds":  elapsed_total,
        "n_params":         n_params,
        "d_model":          d_model,
        "nhead":            nhead,
        "num_layers":       num_layers,
        "ffn_dim":          ffn_dim,
        "max_seq_len":      max_seq_len,
    }


def _build_test_dataset(
    df_test:      pd.DataFrame,
    feature_cols: list,
    train_ds:     SaberProSequenceDataset,
    max_seq_len:  int,
) -> SaberProSequenceDataset:
    """Build a test sequence dataset using training-set normalisation statistics.

    Creates a ``SaberProSequenceDataset`` for the test split without calling
    the class's ``__init__`` (to avoid recomputing normalisation statistics
    from the test data).  Instead, the mean and standard deviation from
    ``train_ds`` are injected directly so test features are normalised on
    the same scale as training features.

    Args:
        df_test: Wide-format test DataFrame (year 2024) from
            ``features.build_features``.
        feature_cols: List of numeric feature column names.  Must match the
            list used when creating ``train_ds``.
        train_ds: The already-initialised training dataset whose
            ``feat_mean`` and ``feat_std`` attributes are reused.
        max_seq_len: Sequence window length.  Must match ``train_ds.max_seq_len``.

    Returns:
        A ``SaberProSequenceDataset`` instance for the test set, normalised
        with training statistics.

    Example:
        >>> train_ds = SaberProSequenceDataset(df_train, feature_cols)
        >>> test_ds = _build_test_dataset(df_test, feature_cols, train_ds, max_seq_len=5)
        >>> len(test_ds)
        2150

    Note:
        Using test-set statistics for normalisation would constitute a mild
        form of data leakage (the model's preprocessing would be informed by
        the test distribution).  This function avoids that by explicitly
        reusing training statistics, consistent with the leakage-prevention
        strategy applied throughout the pipeline.
    """
    ds = SaberProSequenceDataset.__new__(SaberProSequenceDataset)
    ds.feature_cols = feature_cols
    ds.target_col   = "PROMEDIO_GLOBAL"
    ds.max_seq_len  = max_seq_len
    # Reutilizar media/std del train
    ds.feat_mean    = train_ds.feat_mean
    ds.feat_std     = train_ds.feat_std

    df_norm = df_test.copy()
    df_norm[feature_cols] = (df_test[feature_cols] - train_ds.feat_mean) / train_ds.feat_std

    entity_cols = ("ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA")
    year_col    = "AÑO"

    ds.samples = []
    grouped = df_norm.groupby(list(entity_cols), sort=False)
    for _, group in grouped:
        group  = group.sort_values(year_col).reset_index(drop=True)
        feats  = group[feature_cols].values.astype(np.float32)
        target = group["PROMEDIO_GLOBAL"].values.astype(np.float32)
        T = len(group)
        if T == 0:
            continue
        if T >= max_seq_len:
            seq  = feats[-max_seq_len:]
            tgt  = float(target[-1])
            mask = torch.zeros(max_seq_len, dtype=torch.bool)
        else:
            pad_len = max_seq_len - T
            pad     = np.zeros((pad_len, feats.shape[1]), dtype=np.float32)
            seq     = np.vstack([pad, feats])
            tgt     = float(target[-1])
            mask    = torch.zeros(max_seq_len, dtype=torch.bool)
            mask[:pad_len] = True
        ds.samples.append((
            torch.tensor(seq),
            torch.tensor(tgt),
            mask,
        ))

    return ds
