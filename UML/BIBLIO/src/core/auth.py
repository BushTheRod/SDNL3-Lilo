#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/auth.py

"""
Authentification du personnel.
"""

from __future__ import annotations

from typing import Optional

from .database import Database
from .enums import TypePersonnel
from .exceptions import AuthentificationEchouee
from .models import Personnel


class Session:
    """
    Représente l'utilisateur actuellement connecté.
    GUEST est toujours connecté sans mot de passe (accès lecture seule).
    """

    def __init__(self, personnel: Personnel):
        self.personnel = personnel

    @property
    def type(self) -> TypePersonnel:
        return self.personnel.type

    def est_admin(self) -> bool:
        return self.type == TypePersonnel.ADMIN

    def est_superviseur(self) -> bool:
        return self.type == TypePersonnel.SUPERVISEUR

    def est_guest(self) -> bool:
        return self.type == TypePersonnel.GUEST

    def peut_modifier(self) -> bool:
        """ADMIN et SUPERVISEUR peuvent modifier, GUEST non."""
        return self.type in (TypePersonnel.ADMIN, TypePersonnel.SUPERVISEUR)

    def peut_supprimer(self) -> bool:
        """Seul ADMIN peut supprimer."""
        return self.type == TypePersonnel.ADMIN

    def peut_gerer_personnel(self) -> bool:
        """Seul ADMIN gère les comptes du personnel."""
        return self.type == TypePersonnel.ADMIN


class AuthService:

    def __init__(self, db: Database):
        self.db = db

    def connexion_guest(self) -> Session:
        """Crée une session GUEST à la volée (pas de compte requis)."""
        guest = Personnel(
            id=0,
            nom="Invité",
            prenom="",
            type=TypePersonnel.GUEST,
        )
        return Session(guest)

    def connexion(self, email: str, mot_de_passe: str) -> Session:
        """Connexion ADMIN ou SUPERVISEUR."""
        for p in self.db.personnels:
            if p.email.lower() == email.lower():
                if not p.a_mot_de_passe():
                    raise AuthentificationEchoue(
                        "Ce compte n'a pas de mot de passe (GUEST)."
                    )
                if p.authentifier(mot_de_passe):
                    return Session(p)
                raise AuthentificationEchoue("Mot de passe incorrect.")
        raise AuthentificationEchoue("Aucun compte ne correspond à cet email.")

    def lister_personnels(self) -> list[Personnel]:
        return list(self.db.personnels)