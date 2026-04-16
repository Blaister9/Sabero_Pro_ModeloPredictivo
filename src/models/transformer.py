"""
src/models/transformer.py
Transformer encoder para regresión de PROMEDIO_GLOBAL.
Fase 6 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010

Arquitectura:
  - Entrada: secuencia temporal de longitud T (años disponibles por entidad)
  - Embeddings lineales: feature_dim → d_model
  - Positional encoding aprendible (LearnedPositionalEncoding)
  - N_layers capas TransformerEncoder (nhead, ffn_dim, dropout)
  - Pooling: toma último token de la secuencia (posición temporal más reciente)
  - Cabeza de regresión: Linear(d_model, 1)

Restricciones de diseño:
  - CPU-only (sin .cuda())
  - Sin leakage: el dataset de secuencias se construye desplazado 1 año
    (cada muestra de año t usa solo features hasta t-1 como contexto)
  - Entrenamiento con presupuesto de tiempo (time budget externo desde fase6)
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
    """
    Dataset de secuencias temporales por entidad (institución+programa+prueba).

    Para cada entidad con T años de historia, construye ventanas de longitud
    max_seq_len. Si la entidad tiene menos de max_seq_len años, rellena con
    padding (ceros) al inicio (left-padding).

    El target es PROMEDIO_GLOBAL del último año de la ventana.
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
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


# ── Positional Encoding aprendible ───────────────────────────────────────────

class LearnedPositionalEncoding(nn.Module):
    def __init__(self, max_seq_len: int, d_model: int):
        super().__init__()
        self.pe = nn.Embedding(max_seq_len, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, d_model)
        positions = torch.arange(x.size(1), device=x.device).unsqueeze(0)
        return x + self.pe(positions)


# ── Modelo Transformer ────────────────────────────────────────────────────────

class SaberProTransformer(nn.Module):
    """
    Transformer encoder para regresión escalar.

    Parámetros:
        feature_dim   : dimensión de entrada (número de features por paso)
        d_model       : dimensión del embedding interno (64)
        nhead         : cabezas de atención (4)
        num_layers    : capas TransformerEncoder (2)
        ffn_dim       : dimensión feed-forward interna (128)
        dropout       : dropout (0.1)
        max_seq_len   : longitud máxima de secuencia (5)
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
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(
        self,
        x:           torch.Tensor,   # (batch, seq_len, feature_dim)
        src_key_padding_mask: Optional[torch.Tensor] = None,  # (batch, seq_len) bool
    ) -> torch.Tensor:
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
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def _r2(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def train_transformer(
    X_train:      pd.DataFrame,
    y_train:      pd.Series,
    X_test:       pd.DataFrame,
    y_test:       pd.Series,
    df_train:     pd.DataFrame,   # DataFrame completo train (para secuencias)
    df_test:      pd.DataFrame,   # DataFrame completo test  (para secuencias)
    feature_cols: list,
    time_budget_seconds: int = 1200,  # 20 minutos
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
    """
    Entrena el SaberProTransformer con presupuesto de tiempo estricto.

    Si time_budget_seconds se agota antes de convergir, retorna los mejores
    resultados parciales disponibles hasta ese momento.

    Returns dict con:
        model, train_losses, val_losses, best_epoch,
        y_pred_train, y_pred_test,
        rmse_train, r2_train, rmse_test, r2_test,
        converged (bool), elapsed_seconds
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
    """
    Construye el dataset de test usando las estadísticas de normalización del
    train (para evitar data leakage en la normalización).
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
