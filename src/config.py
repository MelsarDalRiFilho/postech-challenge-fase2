"""Configuração central do projeto: caminhos, semente e constantes.

Importe daqui em todos os notebooks para que os resultados sejam reproduzíveis.
"""

from pathlib import Path

# --- Semente -----------------------------------------------------------------
# Use em TODO ponto que envolva aleatoriedade: train_test_split, modelos, CV.
RANDOM_STATE = 42

# --- Caminhos ----------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"
MODELS = RESULTS / "models"
METRICS = RESULTS / "metrics"

# --- Dataset -----------------------------------------------------------------
APPLICATION_FILE = DATA_RAW / "application_record.csv"   # perfil do solicitante
CREDIT_FILE = DATA_RAW / "credit_record.csv"             # histórico mensal de pagamento
PROCESSED_FILE = "dataset_tratado"                       # nome do CSV em data/processed/

TARGET = "mau_pagador"
GROUP = "perfil_id"   # mesmo perfil cadastral = mesmo grupo na validação

# STATUS do credit_record: 0 = 1-29 dias de atraso, 1 = 30-59, 2 = 60-89,
# 3 = 90-119, 4 = 120-149, 5 = 150+ ou baixa como perda; C = quitado; X = sem uso.
# Mau pagador = pelo menos um mês com atraso de 60 dias ou mais.
BAD_STATUS = {"2", "3", "4", "5"}

# Valor sentinela de DAYS_EMPLOYED para aposentados / sem vínculo empregatício.
DAYS_EMPLOYED_SENTINEL = 365243

# --- Split -------------------------------------------------------------------
TEST_SIZE = 0.2
CV_FOLDS = 5
