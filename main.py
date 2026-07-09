"""Master entry point for the Saber Pro predictive pipeline.

This script orchestrates the existing phase scripts without duplicating their
training, cleaning, or reporting logic.  It adds a reproducibility preflight so
missing raw data, processed CSVs, or model artifacts fail with actionable
messages instead of obscure stack traces.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_YEARS = [2020, 2021, 2022, 2023, 2024]


@dataclass(frozen=True)
class Phase:
    number: int
    name: str
    script: str
    needs_raw: bool = False
    needs_clean_csv: bool = False
    needs_features_csv: bool = False
    needs_lgbm_model: bool = False
    produces_clean_csv: bool = False
    produces_features_csv: bool = False
    produces_lgbm_model: bool = False


PHASES = {
    1: Phase(1, "Auditoria de datos raw", "fase1_auditoria.py", needs_raw=True),
    2: Phase(
        2,
        "Limpieza y pivot",
        "fase2_limpieza.py",
        needs_raw=True,
        produces_clean_csv=True,
    ),
    3: Phase(
        3,
        "Feature engineering",
        "fase3_features.py",
        needs_clean_csv=True,
        produces_features_csv=True,
    ),
    4: Phase(4, "Baseline Ridge/Lasso", "fase4_baseline.py", needs_features_csv=True),
    5: Phase(
        5,
        "LightGBM + Optuna + SHAP",
        "fase5_lightgbm.py",
        needs_features_csv=True,
        produces_lgbm_model=True,
    ),
    6: Phase(6, "Transformer + outliers", "fase6_transformer.py", needs_features_csv=True),
    7: Phase(
        7,
        "Demo de inferencia",
        "demo_inference.py",
        needs_features_csv=True,
        needs_lgbm_model=True,
    ),
    8: Phase(8, "Paper academico", "scripts/build_paper.py"),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Orquesta las fases reproducibles del proyecto Saber Pro.",
    )
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        default=DEFAULT_YEARS,
        help="Anios esperados en data/raw/. Default: 2020 2021 2022 2023 2024.",
    )
    parser.add_argument(
        "--from-phase",
        type=int,
        default=1,
        choices=range(1, 9),
        metavar="{1..8}",
        help="Primera fase a ejecutar cuando no se usa --only. Default: 1.",
    )
    parser.add_argument(
        "--to-phase",
        type=int,
        default=8,
        choices=range(1, 9),
        metavar="{1..8}",
        help="Ultima fase a ejecutar cuando no se usa --only. Default: 8.",
    )
    parser.add_argument(
        "--only",
        type=int,
        nargs="+",
        choices=range(1, 9),
        metavar="{1..8}",
        help="Ejecuta solo las fases indicadas, en el orden dado.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida precondiciones y muestra comandos sin ejecutarlos.",
    )
    parser.add_argument(
        "--list-phases",
        action="store_true",
        help="Lista las fases disponibles y termina.",
    )
    return parser.parse_args(argv)


def repo_root() -> Path:
    return Path(__file__).resolve().parent


def selected_phases(args: argparse.Namespace) -> list[Phase]:
    if args.only:
        return [PHASES[n] for n in args.only]
    if args.from_phase > args.to_phase:
        raise ValueError("--from-phase no puede ser mayor que --to-phase")
    return [PHASES[n] for n in range(args.from_phase, args.to_phase + 1)]


def raw_candidates(root: Path, year: int) -> list[Path]:
    raw_dir = root / "data" / "raw"
    return [
        raw_dir / f"saber_pro_{year}.xlsx",
        raw_dir / f"saber_pro_{year}.csv",
        raw_dir / f"Saber_Pro_{year}.xlsx",
        raw_dir / f"SaberPro{year}.xlsx",
    ]


def find_raw_file(root: Path, year: int) -> Path | None:
    for candidate in raw_candidates(root, year):
        if candidate.exists():
            return candidate
    return None


def format_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def print_phase_list() -> None:
    print("Fases disponibles:")
    for phase in PHASES.values():
        print(f"  {phase.number}. {phase.name} -> {phase.script}")


def preflight(root: Path, phases: list[Phase], years: list[int], dry_run: bool = False) -> int:
    clean_csv = root / "data" / "processed" / "saber_pro_limpio.csv"
    features_csv = root / "data" / "processed" / "saber_pro_features.csv"
    lgbm_model = root / "outputs" / "lgbm_model.pkl"

    selected_numbers = {phase.number for phase in phases}
    will_produce_clean = any(phase.produces_clean_csv for phase in phases)
    will_produce_features = any(phase.produces_features_csv for phase in phases)
    will_produce_model = any(phase.produces_lgbm_model for phase in phases)

    if years != DEFAULT_YEARS and selected_numbers & {1, 2, 3, 4, 5, 6, 7}:
        if dry_run:
            print("AVISO: --years difiere de la ventana academica 2020-2024.")
            print("Dry-run continuara solo para validar archivos esperados.")
            print("La ejecucion real de fases de modelado con otros anios sigue bloqueada.")
            print("")
        else:
            print("ERROR: --years fue recibido, pero los scripts de fase actuales")
            print("todavia estan calibrados internamente para 2020-2024.")
            print("Para evitar resultados enganosos, main.py solo ejecuta fases")
            print("modeladas con la ventana de referencia 2020-2024.")
            print("")
            print("Siguiente paso tecnico: parametrizar fase1..fase6 para que")
            print("reciban years/test-year desde main.py.")
            return 2

    if any(phase.needs_raw for phase in phases):
        missing = [year for year in years if find_raw_file(root, year) is None]
        if missing:
            print("ERROR: faltan datos crudos requeridos para las fases 1-2.")
            print("")
            print("Archivos esperados en data/raw/ con nombre canonico:")
            for year in missing:
                print(f"  - data/raw/saber_pro_{year}.xlsx")
            print("")
            print("Los archivos raw no se versionan en Git por tamano.")
            print("Descarguelos desde ICFES y ubiquelos con esos nombres.")
            print("")
            if clean_csv.exists() or features_csv.exists():
                print("Artefactos procesados disponibles localmente:")
                if clean_csv.exists():
                    print(f"  - {format_path(clean_csv, root)}")
                if features_csv.exists():
                    print(f"  - {format_path(features_csv, root)}")
                print("")
                print("Puede continuar desde CSVs procesados, por ejemplo:")
                print("  python main.py --from-phase 3 --to-phase 6")
                print("  python main.py --from-phase 4 --to-phase 6")
            return 2

    if any(phase.needs_clean_csv for phase in phases) and not clean_csv.exists() and not will_produce_clean:
        print("ERROR: falta data/processed/saber_pro_limpio.csv.")
        print("Genere ese CSV ejecutando la fase 2 con datos raw disponibles.")
        return 2

    if any(phase.needs_features_csv for phase in phases) and not features_csv.exists() and not will_produce_features:
        print("ERROR: falta data/processed/saber_pro_features.csv.")
        print("Genere ese CSV ejecutando la fase 3 antes de entrenar modelos.")
        return 2

    if any(phase.needs_lgbm_model for phase in phases) and not lgbm_model.exists() and not will_produce_model:
        print("ERROR: falta outputs/lgbm_model.pkl para inferencia.")
        print("Este archivo no se versiona en Git; se genera con la fase 5:")
        print("  python main.py --only 5")
        return 2

    for phase in phases:
        script_path = root / phase.script
        if not script_path.exists():
            print(f"ERROR: no existe el script de fase: {phase.script}")
            return 2

    return 0


def run_phase(root: Path, phase: Phase, dry_run: bool) -> int:
    cmd = [sys.executable, phase.script]
    printable = " ".join(cmd)
    print("")
    print(f"== Fase {phase.number}: {phase.name}")
    print(f"$ {printable}")

    if dry_run:
        return 0

    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    completed = subprocess.run(cmd, cwd=root, env=env)
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_phases:
        print_phase_list()
        return 0

    try:
        phases = selected_phases(args)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2

    root = repo_root()
    print("Saber Pro pipeline - preflight")
    print(f"Repositorio: {root}")
    print("Fases seleccionadas: " + ", ".join(str(phase.number) for phase in phases))

    status = preflight(root, phases, sorted(args.years), dry_run=args.dry_run)
    if status != 0:
        return status

    if args.dry_run:
        print("Preflight OK. Dry-run: no se ejecutaran scripts.")

    for phase in phases:
        status = run_phase(root, phase, args.dry_run)
        if status != 0:
            print("")
            print(f"ERROR: la fase {phase.number} termino con codigo {status}.")
            return status

    print("")
    print("Pipeline terminado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
