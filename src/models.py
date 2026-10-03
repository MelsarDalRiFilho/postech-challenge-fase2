"""Definição dos modelos candidatos.

Três classificadores distintos, todos com peso maior para a classe minoritária
(mau pagador), já que ela representa menos de 2% da base.
"""

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import RANDOM_STATE


def _encoder(num_cols, cat_cols, scale: bool) -> ColumnTransformer:
    num = StandardScaler() if scale else "passthrough"
    return ColumnTransformer([
        ("num", num, num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ])


def get_models(num_cols: list[str], cat_cols: list[str]) -> dict[str, Pipeline]:
    """Modelos candidatos, cada um encapsulado em um Pipeline.

    Usar Pipeline evita vazamento de dados: encoder e scaler são ajustados
    apenas no fold de treino durante a validação cruzada. Só a Regressão
    Logística é padronizada — modelos de árvore não dependem da escala.
    """
    return {
        "regressao_logistica": Pipeline([
            ("prep", _encoder(num_cols, cat_cols, scale=True)),
            ("clf", LogisticRegression(
                class_weight="balanced", max_iter=2000, random_state=RANDOM_STATE,
            )),
        ]),
        "random_forest": Pipeline([
            ("prep", _encoder(num_cols, cat_cols, scale=False)),
            ("clf", RandomForestClassifier(
                n_estimators=300,
                min_samples_leaf=5,
                class_weight="balanced",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            )),
        ]),
        "gradient_boosting": Pipeline([
            ("prep", _encoder(num_cols, cat_cols, scale=False)),
            ("clf", HistGradientBoostingClassifier(
                class_weight="balanced", random_state=RANDOM_STATE,
            )),
        ]),
    }
