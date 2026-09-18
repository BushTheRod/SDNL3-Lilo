#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/test_fondations.py

"""Test rapide des fondations — à lancer une fois puis supprimer."""

from src.core.database import Database
from src.core.enums import TypePersonnel, StatutEmprunt


def main():
    db = Database()
    db.charger()

    print(f"Livres     : {len(db.livres)}")
    print(f"Catégories : {len(db.categories)}")
    print(f"Personnels : {len(db.personnels)}")

    for l in db.livres:
        print(f"  - [{l.id}] {l.titre} (stock={l.stock})")

    # Test ajout
    from src.core.models import Categorie
    cat = Categorie(id=db.prochain_id("categories"), nom="Test")
    db.categories.append(cat)
    db.sauvegarder()
    print("✅ Sauvegarde OK")


if __name__ == "__main__":
    main()