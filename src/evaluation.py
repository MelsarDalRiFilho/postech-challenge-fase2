"""Métricas e comparação entre modelos."""

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.config import METRICS

# Métrica usada para ordenar a comparação: área sob a curva precisão-recall,
# a mais informativa quando a classe positiva é rara.
PRIMARY_METRIC = "pr_auc"


def score(y_true, y_pred, y_proba=None) -> dict[str, float]:
    """Conjunto de métricas para classificação binária.

    Acurácia sozinha engana em base desbalanceada — por isso precisão, recall,
    F1, AUC-ROC e PR-AUC vêm junto.
    """
    out = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    if y_proba is not None:
        out["roc_auc"] = roc_auc_score(y_true, y_proba)
        out["pr_auc"] = average_precision_score(y_true, y_proba)
    return out


def comparison_table(results: dict[str, dict]) -> pd.DataFrame:
    """Monta a tabela comparativa e salva em results/metrics/."""
    df = pd.DataFrame(results).T.round(4)
    df = df.sort_values(PRIMARY_METRIC if PRIMARY_METRIC in df else "f1", ascending=False)
    METRICS.mkdir(parents=True, exist_ok=True)
    df.to_csv(METRICS / "comparacao_modelos.csv")
    return df
