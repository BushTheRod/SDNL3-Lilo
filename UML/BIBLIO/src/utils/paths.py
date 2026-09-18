#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/utils/paths.py

"""
Gestion des chemins compatibles dev / exécutable PyInstaller.
"""

import sys
from pathlib import Path


def est_compile() -> bool:
    """True si on tourne dans un exécutable PyInstaller."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def racine_projet() -> Path:
    """
    Retourne la racine du projet.
    - En dev : dossier contenant 'src/'
    - En .exe : dossier où se trouve l'exécutable
    """
    if est_compile():
        return Path(sys.executable).resolve().parent
    # src/utils/paths.py -> remonte de 3 niveaux
    return Path(__file__).resolve().parents[2]


def dossier_datas() -> Path:
    """Dossier 'datas' à la racine du projet."""
    d = racine_projet() / "datas"
    d.mkdir(parents=True, exist_ok=True)
    return d


def fichier_db() -> Path:
    """Chemin vers DB_Lilo.json."""
    return dossier_datas() / "DB_Lilo.json"