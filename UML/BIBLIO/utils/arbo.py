#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liste l'arborescence complète du dossier PARENT (../) et de ses sous-dossiers.
Écrit le résultat dans arbo.txt, au même niveau que ce script.
"""

import sys
from pathlib import Path


# Dossier où se trouve ce script (arbo.py)
DOSSIER_SCRIPT = Path(__file__).resolve().parent

# Fichier de sortie, au même niveau que le script
FICHIER_SORTIE = DOSSIER_SCRIPT / "arbo.txt"

# Dossier à explorer : le parent du dossier du script (../)
DOSSIER_A_EXPLORER = DOSSIER_SCRIPT.parent


def arborescence(racine: Path, sortie, prefixe: str = "",
                 afficher_fichiers: bool = True):
    """
    Écrit récursivement l'arborescence d'un dossier dans le flux 'sortie'.
    """
    try:
        entrees = sorted(
            racine.iterdir(),
            key=lambda p: (p.is_file(), p.name.lower())
        )
    except PermissionError:
        print(f"{prefixe}└── [Accès refusé] {racine.name}", file=sortie)
        return

    if not afficher_fichiers:
        entrees = [e for e in entrees if e.is_dir()]

    for i, entree in enumerate(entrees):
        dernier = (i == len(entrees) - 1)
        connecteur = "└── " if dernier else "├── "

        if entree.is_symlink():
            symbole = "[L] "
        elif entree.is_dir():
            symbole = "[D] "
        else:
            symbole = "[F] "

        print(f"{prefixe}{connecteur}{symbole}{entree.name}", file=sortie)

        if entree.is_dir() and not entree.is_symlink():
            extension = "    " if dernier else "│   "
            arborescence(entree, sortie, prefixe + extension, afficher_fichiers)


def main():
    afficher_fichiers = True

    for arg in sys.argv[1:]:
        if arg in ("-d", "--dossiers-seulement"):
            afficher_fichiers = False
        elif arg in ("-h", "--help"):
            print("Usage: python arbo.py [OPTIONS]")
            print()
            print("Options:")
            print("  -d, --dossiers-seulement   N'afficher que les dossiers")
            print("  -h, --help                 Afficher cette aide")
            print()
            print(f"Explore : {DOSSIER_A_EXPLORER}")
            print(f"Écrit   : {FICHIER_SORTIE}")
            return

    with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
        f.write(f"{DOSSIER_A_EXPLORER}\n")
        arborescence(DOSSIER_A_EXPLORER, f, afficher_fichiers=afficher_fichiers)

    print(f"✅ Arborescence écrite dans : {FICHIER_SORTIE}")


if __name__ == "__main__":
    main()