#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/database.py

"""
Chargement / sauvegarde de la base JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..utils.paths import fichier_db
from .models import Livre, Categorie, Usager, Personnel, Emprunt, Reservation


VERSION_SCHEMA = 1


class Database:
    """
    Base de données JSON en mémoire.
    Charger au démarrage, sauvegarder à la demande.
    """

    def __init__(self, chemin: Path | None = None):
        self.chemin: Path = chemin or fichier_db()
        self.livres: list[Livre] = []
        self.categories: list[Categorie] = []
        self.usagers: list[Usager] = []
        self.personnels: list[Personnel] = []
        self.emprunts: list[Emprunt] = []
        self.reservations: list[Reservation] = []

    # ---------- Chargement / sauvegarde ----------

    def charger(self) -> None:
        if not self.chemin.exists():
            self._initialiser_vide()
            self.sauvegarder()
            return

        with open(self.chemin, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)

        self.livres = [Livre.from_dict(d) for d in data.get("livres", [])]
        self.categories = [Categorie.from_dict(d) for d in data.get("categories", [])]
        self.usagers = [Usager.from_dict(d) for d in data.get("usagers", [])]
        self.personnels = [Personnel.from_dict(d) for d in data.get("personnels", [])]
        self.emprunts = [Emprunt.from_dict(d) for d in data.get("emprunts", [])]
        self.reservations = [Reservation.from_dict(d) for d in data.get("reservations", [])]

    def sauvegarder(self) -> None:
        data = {
            "version": VERSION_SCHEMA,
            "livres": [l.to_dict() for l in self.livres],
            "categories": [c.to_dict() for c in self.categories],
            "usagers": [u.to_dict() for u in self.usagers],
            "personnels": [p.to_dict() for p in self.personnels],
            "emprunts": [e.to_dict() for e in self.emprunts],
            "reservations": [r.to_dict() for r in self.reservations],
        }
        self.chemin.parent.mkdir(parents=True, exist_ok=True)
        with open(self.chemin, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ---------- Initialisation minimale ----------

    def _initialiser_vide(self) -> None:
        """Crée un personnel ADMIN par défaut pour pouvoir se connecter."""
        from .enums import TypePersonnel
        self.personnels = [
            Personnel(
                id=1,
                nom="Admin",
                prenom="Système",
                email="admin@biblio.local",
                mot_de_passe="admin",
                type=TypePersonnel.ADMIN,
            )
        ]

    # ---------- Génération d'ID ----------

    def prochain_id(self, collection: str) -> int:
        """Retourne le prochain id libre pour une collection."""
        mapping = {
            "livres": self.livres,
            "categories": self.categories,
            "usagers": self.usagers,
            "personnels": self.personnels,
            "emprunts": self.emprunts,
            "reservations": self.reservations,
        }
        items = mapping.get(collection, [])
        if not items:
            return 1
        return max(item.id for item in items) + 1