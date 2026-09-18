#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/models.py

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Optional

from .enums import TypePersonnel, StatutEmprunt, StatutReservation


# ---------- Helpers de conversion date <-> str (JSON) ----------

def _to_str(d) -> Optional[str]:
    if d is None:
        return None
    if isinstance(d, (date, datetime)):
        return d.isoformat()
    return str(d)


def _to_date(s) -> Optional[date]:
    if not s:
        return None
    if isinstance(s, date):
        return s
    return date.fromisoformat(s)


# ---------- Entités ----------

@dataclass
class Livre:
    id: int
    isbn: str
    titre: str
    auteur: str
    image: str = ""
    stock: int = 0
    annee_publication: Optional[int] = None
    categories: list[int] = field(default_factory=list)  # ids de Categorie

    def est_disponible(self) -> bool:
        return self.stock > 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Livre":
        return cls(
            id=d["id"],
            isbn=d.get("isbn", ""),
            titre=d.get("titre", ""),
            auteur=d.get("auteur", ""),
            image=d.get("image", ""),
            stock=int(d.get("stock", 0)),
            annee_publication=d.get("annee_publication"),
            categories=list(d.get("categories", [])),
        )


@dataclass
class Categorie:
    id: int
    nom: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Categorie":
        return cls(id=d["id"], nom=d.get("nom", ""))


@dataclass
class Usager:
    id: int
    nom: str
    prenom: str
    email: str = ""
    telephone: str = ""
    date_inscription: Optional[date] = None

    def get_nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}".strip()

    def to_dict(self) -> dict:
        d = asdict(self)
        d["date_inscription"] = _to_str(self.date_inscription)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Usager":
        return cls(
            id=d["id"],
            nom=d.get("nom", ""),
            prenom=d.get("prenom", ""),
            email=d.get("email", ""),
            telephone=d.get("telephone", ""),
            date_inscription=_to_date(d.get("date_inscription")),
        )


@dataclass
class Personnel:
    id: int
    nom: str
    prenom: str
    email: str = ""
    mot_de_passe: Optional[str] = None  # None pour GUEST
    type: TypePersonnel = TypePersonnel.GUEST

    def a_mot_de_passe(self) -> bool:
        """Le mot de passe n'a de sens que pour ADMIN/SUPERVISEUR."""
        return self.type in (TypePersonnel.ADMIN, TypePersonnel.SUPERVISEUR)

    def authentifier(self, mot_de_passe: str) -> bool:
        if not self.a_mot_de_passe():
            return False
        return self.mot_de_passe == mot_de_passe

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,
            "type": self.type.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Personnel":
        return cls(
            id=d["id"],
            nom=d.get("nom", ""),
            prenom=d.get("prenom", ""),
            email=d.get("email", ""),
            mot_de_passe=d.get("mot_de_passe"),
            type=TypePersonnel(d.get("type", "GUEST")),
        )


@dataclass
class Emprunt:
    id: int
    usager_id: int
    livre_id: int
    personnel_id: Optional[int] = None
    date_emprunt: Optional[date] = None
    date_retour_prevue: Optional[date] = None
    date_retour_effective: Optional[date] = None
    statut: StatutEmprunt = StatutEmprunt.EN_COURS

    def est_en_retard(self, aujourd_hui: Optional[date] = None) -> bool:
        if self.statut == StatutEmprunt.RENDU:
            return False
        ref = aujourd_hui or date.today()
        return self.date_retour_prevue is not None and ref > self.date_retour_prevue

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "usager_id": self.usager_id,
            "livre_id": self.livre_id,
            "personnel_id": self.personnel_id,
            "date_emprunt": _to_str(self.date_emprunt),
            "date_retour_prevue": _to_str(self.date_retour_prevue),
            "date_retour_effective": _to_str(self.date_retour_effective),
            "statut": self.statut.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Emprunt":
        return cls(
            id=d["id"],
            usager_id=d["usager_id"],
            livre_id=d["livre_id"],
            personnel_id=d.get("personnel_id"),
            date_emprunt=_to_date(d.get("date_emprunt")),
            date_retour_prevue=_to_date(d.get("date_retour_prevue")),
            date_retour_effective=_to_date(d.get("date_retour_effective")),
            statut=StatutEmprunt(d.get("statut", "EN_COURS")),
        )


@dataclass
class Reservation:
    id: int
    usager_id: int
    livre_id: int
    date_reservation: Optional[date] = None
    date_expiration: Optional[date] = None
    statut: StatutReservation = StatutReservation.EN_ATTENTE

    def est_expiree(self, aujourd_hui: Optional[date] = None) -> bool:
        ref = aujourd_hui or date.today()
        return self.date_expiration is not None and ref > self.date_expiration

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "usager_id": self.usager_id,
            "livre_id": self.livre_id,
            "date_reservation": _to_str(self.date_reservation),
            "date_expiration": _to_str(self.date_expiration),
            "statut": self.statut.value,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Reservation":
        return cls(
            id=d["id"],
            usager_id=d["usager_id"],
            livre_id=d["livre_id"],
            date_reservation=_to_date(d.get("date_reservation")),
            date_expiration=_to_date(d.get("date_expiration")),
            statut=StatutReservation(d.get("statut", "EN_ATTENTE")),
        )