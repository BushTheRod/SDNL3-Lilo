#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/test_services.py

"""Test rapide des services. À lancer depuis la racine du projet."""

from src.core.auth import AuthService
from src.core.database import Database
from src.core.enums import TypePersonnel
from src.core.services import BiblioService


def main():
    # 1. Base
    db = Database()
    db.charger()

    # 2. Session ADMIN (le compte par défaut créé par _initialiser_vide)
    auth = AuthService(db)
    session = auth.connexion("admin@biblio.local", "admin")
    print(f"Connecté : {session.personnel.prenom} ({session.type.value})")

    # 3. Service
    svc = BiblioService(db, session)

    # 4. Créer un usager
    usager = svc.ajouter_usager("Dupont", "Marie", "marie@example.com")
    print(f"Usager créé : {usager.get_nom_complet()} (id={usager.id})")

    # 5. Emprunt du livre id=1
    livre = svc.trouver_livre(1)
    print(f"Stock avant emprunt : {livre.stock}")
    emprunt = svc.creer_emprunt(usager.id, livre.id)
    print(f"Emprunt créé : id={emprunt.id}, retour prévu={emprunt.date_retour_prevue}")
    print(f"Stock après emprunt : {livre.stock}")

    # 6. Retour
    svc.retourner_emprunt(emprunt.id)
    print(f"Stock après retour : {livre.stock}")

    # 7. Test réservation sur livre en rupture (stock 0)
    livre2 = svc.trouver_livre(2)
    livre2.stock = 0
    usager2 = svc.ajouter_usager("Martin", "Luc")
    resa = svc.reserver(usager2.id, livre2.id)
    print(f"Réservation : id={resa.id}, statut={resa.statut.value}")

    print("\n✅ Tous les tests passent.")


if __name__ == "__main__":
    main()