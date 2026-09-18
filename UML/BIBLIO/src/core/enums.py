#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/enums.py

from enum import Enum


class TypePersonnel(str, Enum):
    ADMIN = "ADMIN"
    SUPERVISEUR = "SUPERVISEUR"
    GUEST = "GUEST"


class StatutEmprunt(str, Enum):
    EN_COURS = "EN_COURS"
    RENDU = "RENDU"
    EN_RETARD = "EN_RETARD"


class StatutReservation(str, Enum):
    EN_ATTENTE = "EN_ATTENTE"
    DISPONIBLE = "DISPONIBLE"
    ANNULEE = "ANNULEE"
    HONOREE = "HONOREE"