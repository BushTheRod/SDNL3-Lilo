#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# utils/arbo.py

# python utils\arbo.py           # arbo + stats
# python utils\arbo.py -d        # uniquement les dossiers (+ stats)
# python utils\arbo.py -s        # arbo seule, sans stats

"""
Liste l'arborescence complète + statistiques de code.

- Compte les fichiers de code selon une liste d'extensions
- Compte le nombre de lignes total (et par langage)
- Ignore : packages, images, libs, caches, venv, node_modules, etc.
"""

import sys
from pathlib import Path
from collections import defaultdict


# Dossier où se trouve ce script
DOSSIER_SCRIPT = Path(__file__).resolve().parent
FICHIER_SORTIE = DOSSIER_SCRIPT / "arbo.txt"
DOSSIER_A_EXPLORER = DOSSIER_SCRIPT.parent


# ---------- Configuration ----------

# Extensions considérées comme "code"
EXTENSIONS_CODE = {
    ".py", ".pyw",
    ".js", ".mjs", ".cjs",
    ".ts", ".tsx",
    ".jsx",
    ".html", ".htm",
    ".css", ".scss", ".sass", ".less",
    ".java",
    ".c", ".h", ".cpp", ".hpp", ".cc",
    ".cs",
    ".php",
    ".rb",
    ".go",
    ".rs",
    ".swift",
    ".kt",
    ".sql",
    ".sh", ".bash", ".ps1", ".bat",
    ".json", ".xml", ".yml", ".yaml", ".toml", ".ini",
    ".md", ".rst", ".txt",
}

# Dossiers à ignorer (par nom exact)
DOSSIERS_IGNORES = {
    "__pycache__", ".git", ".svn", ".hg",
    "node_modules", "venv", ".venv", "env", ".env",
    "dist", "build", ".idea", ".vscode",
    "site-packages", "lib", "libs", "packages",
    "bower_components", "vendor",
    "target", "bin", "obj",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".eggs", "*.egg-info",
    "docs", "documentation",
    "fonts", "images", "img", "assets", "static", "media",
}

# Extensions à ne jamais compter (images, binaires, etc.)
EXTENSIONS_EXCLUES = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".pyo", ".class",
    ".mp3", ".mp4", ".avi", ".mov", ".wav", ".ogg",
    ".ttf", ".otf", ".woff", ".woff2", ".eot",
    ".db", ".sqlite", ".sqlite3",
}


# ---------- Arborescence ----------

def arborescence(racine: Path, sortie, prefixe: str = "",
                 afficher_fichiers: bool = True):
    """Écrit récursivement l'arborescence d'un dossier dans 'sortie'."""
    try:
        entrees = sorted(
            racine.iterdir(),
            key=lambda p: (p.is_file(), p.name.lower())
        )
    except PermissionError:
        print(f"{prefixe}└── [Accès refusé] {racine.name}", file=sortie)
        return

    # Filtre dossiers ignorés
    entrees = [
        e for e in entrees
        if not (e.is_dir() and e.name in DOSSIERS_IGNORES)
        and e.suffix.lower() not in EXTENSIONS_EXCLUES
    ]

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


# ---------- Statistiques ----------

def compter_lignes(fichier: Path) -> int:
    """Compte les lignes d'un fichier (tolérant aux erreurs d'encodage)."""
    try:
        with open(fichier, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (OSError, UnicodeDecodeError):
        return 0


def parcourir_code(racine: Path) -> dict:
    """
    Parcourt récursivement 'racine' et retourne un dict de stats :
      {
        "fichiers": [(chemin_relatif, langage, lignes), ...],
        "par_extension": {".py": (nb_fichiers, nb_lignes), ...},
        "total_fichiers": int,
        "total_lignes": int,
      }
    """
    fichiers = []
    par_extension = defaultdict(lambda: [0, 0])  # ext -> [nb_fichiers, nb_lignes]

    def _walk(dossier: Path):
        try:
            entrees = sorted(dossier.iterdir())
        except PermissionError:
            return

        for entree in entrees:
            if entree.is_symlink():
                continue
            if entree.is_dir():
                if entree.name in DOSSIERS_IGNORES:
                    continue
                _walk(entree)
            elif entree.is_file():
                ext = entree.suffix.lower()
                if ext in EXTENSIONS_EXCLUES:
                    continue
                if ext not in EXTENSIONS_CODE:
                    continue
                lignes = compter_lignes(entree)
                try:
                    relatif = entree.relative_to(racine)
                except ValueError:
                    relatif = entree
                fichiers.append((relatif, ext, lignes))
                par_extension[ext][0] += 1
                par_extension[ext][1] += lignes

    _walk(racine)

    total_fichiers = sum(v[0] for v in par_extension.values())
    total_lignes = sum(v[1] for v in par_extension.values())

    return {
        "fichiers": fichiers,
        "par_extension": dict(par_extension),
        "total_fichiers": total_fichiers,
        "total_lignes": total_lignes,
    }


def ecrire_stats(sortie, racine: Path, stats: dict):
    """Écrit le bloc de statistiques dans 'sortie'."""
    print("\n" + "=" * 60, file=sortie)
    print("  STATISTIQUES DE CODE", file=sortie)
    print("=" * 60, file=sortie)

    # Par extension
    print("\nPar type de fichier :", file=sortie)
    print(f"  {'Extension':<12} {'Fichiers':>10} {'Lignes':>10}", file=sortie)
    print(f"  {'-'*12} {'-'*10} {'-'*10}", file=sortie)

    for ext, (nb_fichiers, nb_lignes) in sorted(
            stats["par_extension"].items(),
            key=lambda x: -x[1][1]
    ):
        print(f"  {ext:<12} {nb_fichiers:>10} {nb_lignes:>10}", file=sortie)

    print(f"  {'-'*12} {'-'*10} {'-'*10}", file=sortie)
    print(f"  {'TOTAL':<12} {stats['total_fichiers']:>10} "
          f"{stats['total_lignes']:>10}", file=sortie)

    # Détail par fichier
    print("\nDétail par fichier :", file=sortie)
    print(f"  {'Fichier':<55} {'Lignes':>8}", file=sortie)
    print(f"  {'-'*55} {'-'*8}", file=sortie)
    for chemin, ext, lignes in sorted(stats["fichiers"],
                                      key=lambda x: str(x[0]).lower()):
        chemin_str = str(chemin).replace("\\", "/")
        if len(chemin_str) > 53:
            chemin_str = "…" + chemin_str[-52:]
        print(f"  {chemin_str:<55} {lignes:>8}", file=sortie)

    print("\n" + "=" * 60, file=sortie)
    print(f"  TOTAL : {stats['total_fichiers']} fichier(s) de code, "
          f"{stats['total_lignes']} ligne(s)", file=sortie)
    print("=" * 60, file=sortie)


# ---------- Main ----------

def main():
    afficher_fichiers = True
    stats_actives = True

    for arg in sys.argv[1:]:
        if arg in ("-d", "--dossiers-seulement"):
            afficher_fichiers = False
        elif arg in ("-s", "--sans-stats"):
            stats_actives = False
        elif arg in ("-h", "--help"):
            print("Usage: python arbo.py [OPTIONS]")
            print()
            print("Options:")
            print("  -d, --dossiers-seulement   N'afficher que les dossiers")
            print("  -s, --sans-stats           Ne pas afficher les stats de code")
            print("  -h, --help                 Afficher cette aide")
            print()
            print(f"Explore : {DOSSIER_A_EXPLORER}")
            print(f"Écrit   : {FICHIER_SORTIE}")
            return

    with open(FICHIER_SORTIE, "w", encoding="utf-8") as f:
        # 1. Arborescence
        f.write(f"{DOSSIER_A_EXPLORER}\n")
        arborescence(DOSSIER_A_EXPLORER, f, afficher_fichiers=afficher_fichiers)

        # 2. Stats
        if stats_actives:
            stats = parcourir_code(DOSSIER_A_EXPLORER)
            ecrire_stats(f, DOSSIER_A_EXPLORER, stats)

    print(f"✅ Arborescence écrite dans : {FICHIER_SORTIE}")

    if stats_actives:
        stats = parcourir_code(DOSSIER_A_EXPLORER)
        print(f"   {stats['total_fichiers']} fichier(s) de code — "
              f"{stats['total_lignes']} ligne(s) au total")


if __name__ == "__main__":
    main()