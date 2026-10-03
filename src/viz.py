"""Estilo dos gráficos e gravação em results/figures/."""

import matplotlib.pyplot as plt

from src.config import FIGURES

# Cores por papel, não por posição: bom pagador é sempre azul, mau pagador sempre laranja.
COR_BOM = "#2a78d6"
COR_MAU = "#eb6834"
COR_NEUTRA = "#8a8984"
TEXTO = "#0b0b0b"
TEXTO_SEC = "#52514e"
SUPERFICIE = "#fcfcfb"
CORES_MODELOS = ["#2a78d6", "#eb6834", "#1baf7a"]


def aplicar_estilo() -> None:
    """Eixos e grade discretos, texto em tons neutros."""
    plt.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "axes.edgecolor": "#c3c2b7",
        "axes.labelcolor": TEXTO_SEC,
        "axes.titlecolor": TEXTO,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e6e5e0",
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "xtick.color": TEXTO_SEC,
        "ytick.color": TEXTO_SEC,
        "legend.frameon": False,
        "figure.dpi": 100,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def salvar(fig, nome: str) -> None:
    """Grava a figura em results/figures/<nome>.png."""
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{nome}.png")
