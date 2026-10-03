"""Limpeza, construção do alvo e feature engineering."""

import numpy as np
import pandas as pd

from src.config import BAD_STATUS, DAYS_EMPLOYED_SENTINEL, TARGET


def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Resumo de nulos por coluna, em contagem e percentual."""
    total = df.isna().sum()
    pct = (total / len(df) * 100).round(2)
    return (
        pd.DataFrame({"nulos": total, "pct": pct})
        .query("nulos > 0")
        .sort_values("nulos", ascending=False)
    )


def build_target(credit: pd.DataFrame) -> pd.DataFrame:
    """Um registro por cliente: mau_pagador = 1 se teve algum mês com atraso >= 60 dias.

    O limiar está em config.BAD_STATUS e é justificado no notebook 02.
    """
    bad = credit["STATUS"].isin(BAD_STATUS)
    return (
        bad.groupby(credit["ID"]).max().astype(int)
        .rename(TARGET).reset_index()
    )


def drop_duplicated_ids(app: pd.DataFrame) -> pd.DataFrame:
    """Remove todos os IDs que aparecem mais de uma vez no cadastro.

    Não há como saber qual das linhas corresponde ao histórico de crédito,
    então nenhuma delas é confiável.
    """
    return app[~app["ID"].duplicated(keep=False)].copy()


def profile_groups(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    """Número do perfil: linhas com os mesmos valores em `cols` recebem o mesmo número.

    Usado como grupo na validação, para que cópias do mesmo perfil não fiquem
    ao mesmo tempo no treino e no teste.
    """
    return df.groupby(cols, dropna=False, sort=False).ngroup().rename("perfil_id")


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Converte as colunas brutas em variáveis legíveis e cria as derivadas."""
    out = df.copy()
    sem_vinculo = out["DAYS_EMPLOYED"] == DAYS_EMPLOYED_SENTINEL

    out["idade_anos"] = (-out["DAYS_BIRTH"] / 365.25).round(1)
    out["aposentado_ou_sem_vinculo"] = sem_vinculo.astype(int)
    out["anos_empregado"] = np.where(
        sem_vinculo, 0.0, (-out["DAYS_EMPLOYED"] / 365.25).round(1)
    )
    # Pensionista com tempo de emprego preenchido: dados contraditórios no cadastro.
    out["cadastro_inconsistente"] = (
        (out["NAME_INCOME_TYPE"] == "Pensioner") & ~sem_vinculo
    ).astype(int)
    out["renda_per_capita"] = out["AMT_INCOME_TOTAL"] / out["CNT_FAM_MEMBERS"].clip(lower=1)
    out["OCCUPATION_TYPE"] = out["OCCUPATION_TYPE"].fillna("Nao informado")

    for col in ["FLAG_OWN_CAR", "FLAG_OWN_REALTY"]:
        out[col] = (out[col] == "Y").astype(int)
    out["CODE_GENDER"] = (out["CODE_GENDER"] == "F").astype(int)
    out = out.rename(columns={"CODE_GENDER": "FLAG_FEMININO"})

    return out.drop(columns=["DAYS_BIRTH", "DAYS_EMPLOYED"])
