#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/exceptions.py

class BiblioError(Exception):
    """Exception de base pour toutes les erreurs métier."""
    pass


class LivreIndisponible(BiblioError):
    pass


class DejaEmprunte(BiblioError):
    pass


class DejaReserve(BiblioError):
    pass


class AuthentificationEchouee(BiblioError):
    pass


class PermissionRefusee(BiblioError):
    pass


class EntiteIntrouvable(BiblioError):
    pass