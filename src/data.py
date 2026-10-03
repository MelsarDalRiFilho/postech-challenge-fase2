"""Carregamento e persistência de dados."""

from pathlib import Path

import pandas as pd

from src.config import APPLICATION_FILE, CREDIT_FILE, DATA_PROCESSED


def _read_raw(path: Path, **kwargs) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} não encontrado. Veja data/README.md para baixar o dataset."
        )
    return pd.read_csv(path, **kwargs)


def load_application() -> pd.DataFrame:
    """Lê o cadastro dos solicitantes (data/raw/application_record.csv)."""
    return _read_raw(APPLICATION_FILE)


def load_credit() -> pd.DataFrame:
    """Lê o histórico mensal de pagamento (data/raw/credit_record.csv).

    STATUS é lido como texto porque mistura dígitos com as letras C e X.
    """
    return _read_raw(CREDIT_FILE, dtype={"STATUS": str})


def save_processed(df: pd.DataFrame, name: str) -> None:
    """Grava um dataset tratado em data/processed/ como CSV."""
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PROCESSED / f"{name}.csv", index=False)


def load_processed(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED / f"{name}.csv")
