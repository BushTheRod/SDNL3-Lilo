#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/core/services.py

"""
Services métier : emprunts, réservations, CRUD, notifications.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional

from .database import Database
from .enums import StatutEmprunt, StatutReservation
from .exceptions import (
    DejaEmprunte,
    DejaReserve,
    EntiteIntrouvable,
    LivreIndisponible,
    PermissionRefusee,
)
from .auth import Session
from .models import (
    Categorie,
    Emprunt,
    Livre,
    Personnel,
    Reservation,
    Usager,
)


# ---------- Constantes métier ----------

DUREE_EMPRUNT_JOURS = 14       # durée standard d'un prêt
DUREE_RESERVATION_JOURS = 3    # délai pour venir chercher un livre réservé


# ============================================================
#  Service Livres / Catégories / Usagers / Personnel (CRUD)
# ============================================================

class BiblioService:
    """
    Point d'entrée unique pour toutes les opérations métier.
    Contrôle les permissions via la Session.
    """

    def __init__(self, db: Database, session: Session):
        self.db = db
        self.session = session

    # ----------------------------------------------------------
    #  Permissions
    # ----------------------------------------------------------

    def _verifier_ecriture(self):
        if not self.session.peut_modifier():
            raise PermissionRefusee(
                "Votre profil (GUEST) ne permet pas de modifier les données."
            )

    def _verifier_suppression(self):
        if not self.session.peut_supprimer():
            raise PermissionRefusee(
                "Seul un ADMIN peut supprimer des données."
            )

    # ----------------------------------------------------------
    #  LIVRES
    # ----------------------------------------------------------

    def lister_livres(self) -> list[Livre]:
        return list(self.db.livres)

    def trouver_livre(self, livre_id: int) -> Livre:
        for l in self.db.livres:
            if l.id == livre_id:
                return l
        raise EntiteIntrouvable(f"Livre id={livre_id} introuvable.")

    def ajouter_livre(self, isbn: str, titre: str, auteur: str,
                      stock: int = 1, image: str = "",
                      annee_publication: Optional[int] = None,
                      categories: Optional[list[int]] = None) -> Livre:
        self._verifier_ecriture()
        livre = Livre(
            id=self.db.prochain_id("livres"),
            isbn=isbn, titre=titre, auteur=auteur,
            image=image, stock=stock,
            annee_publication=annee_publication,
            categories=categories or [],
        )
        self.db.livres.append(livre)
        self.db.sauvegarder()
        return livre

    def modifier_livre(self, livre_id: int, **champs) -> Livre:
        self._verifier_ecriture()
        livre = self.trouver_livre(livre_id)
        for cle, valeur in champs.items():
            if hasattr(livre, cle):
                setattr(livre, cle, valeur)
        self.db.sauvegarder()
        return livre

    def supprimer_livre(self, livre_id: int) -> None:
        self._verifier_suppression()
        # Refus si emprunts en cours
        for e in self.db.emprunts:
            if e.livre_id == livre_id and e.statut == StatutEmprunt.EN_COURS:
                raise PermissionRefusee(
                    "Impossible de supprimer : ce livre est en cours d'emprunt."
                )
        self.db.livres = [l for l in self.db.livres if l.id != livre_id]
        self.db.sauvegarder()

    # ----------------------------------------------------------
    #  CATEGORIES
    # ----------------------------------------------------------

    def lister_categories(self) -> list[Categorie]:
        return list(self.db.categories)

    def trouver_categorie(self, cat_id: int) -> Categorie:
        for c in self.db.categories:
            if c.id == cat_id:
                return c
        raise EntiteIntrouvable(f"Catégorie id={cat_id} introuvable.")

    def ajouter_categorie(self, nom: str) -> Categorie:
        self._verifier_ecriture()
        cat = Categorie(id=self.db.prochain_id("categories"), nom=nom)
        self.db.categories.append(cat)
        self.db.sauvegarder()
        return cat

    def supprimer_categorie(self, cat_id: int) -> None:
        self._verifier_suppression()
        self.db.categories = [c for c in self.db.categories if c.id != cat_id]
        # Retire la catégorie des livres
        for l in self.db.livres:
            if cat_id in l.categories:
                l.categories.remove(cat_id)
        self.db.sauvegarder()

    # ----------------------------------------------------------
    #  USAGERS
    # ----------------------------------------------------------

    def lister_usagers(self) -> list[Usager]:
        return list(self.db.usagers)

    def trouver_usager(self, usager_id: int) -> Usager:
        for u in self.db.usagers:
            if u.id == usager_id:
                return u
        raise EntiteIntrouvable(f"Usager id={usager_id} introuvable.")

    def ajouter_usager(self, nom: str, prenom: str, email: str = "",
                       telephone: str = "") -> Usager:
        self._verifier_ecriture()
        u = Usager(
            id=self.db.prochain_id("usagers"),
            nom=nom, prenom=prenom, email=email, telephone=telephone,
            date_inscription=date.today(),
        )
        self.db.usagers.append(u)
        self.db.sauvegarder()
        return u

    def supprimer_usager(self, usager_id: int) -> None:
        self._verifier_suppression()
        for e in self.db.emprunts:
            if e.usager_id == usager_id and e.statut == StatutEmprunt.EN_COURS:
                raise PermissionRefusee(
                    "Impossible de supprimer : cet usager a un emprunt en cours."
                )
        self.db.usagers = [u for u in self.db.usagers if u.id != usager_id]
        self.db.sauvegarder()

    # ----------------------------------------------------------
    #  PERSONNEL (ADMIN seulement)
    # ----------------------------------------------------------

    def lister_personnels(self) -> list[Personnel]:
        if not self.session.peut_gerer_personnel():
            raise PermissionRefusee("Réservé à l'ADMIN.")
        return list(self.db.personnels)

    def ajouter_personnel(self, nom: str, prenom: str, email: str,
                          mot_de_passe: Optional[str],
                          type_personnel) -> Personnel:
        if not self.session.peut_gerer_personnel():
            raise PermissionRefusee("Réservé à l'ADMIN.")
        p = Personnel(
            id=self.db.prochain_id("personnels"),
            nom=nom, prenom=prenom, email=email,
            mot_de_passe=mot_de_passe, type=type_personnel,
        )
        self.db.personnels.append(p)
        self.db.sauvegarder()
        return p

    # ==========================================================
    #  EMPRUNTS
    # ==========================================================

    def creer_emprunt(self, usager_id: int, livre_id: int) -> Emprunt:
        self._verifier_ecriture()
        usager = self.trouver_usager(usager_id)
        livre = self.trouver_livre(livre_id)

        # Un usager ne peut pas emprunter 2x le même livre en cours
        for e in self.db.emprunts:
            if (e.usager_id == usager_id
                    and e.livre_id == livre_id
                    and e.statut == StatutEmprunt.EN_COURS):
                raise DejaEmprunte(
                    f"{usager.get_nom_complet()} a déjà ce livre en cours."
                )

        # Réservation prioritaire ?
        resa = self._premiere_reservation_active(livre_id)
        if resa and resa.usager_id != usager_id:
            raise LivreIndisponible(
                "Ce livre est réservé par un autre usager en priorité."
            )

        if not livre.est_disponible():
            raise LivreIndisponible(
                f"'{livre.titre}' n'a plus de stock disponible."
            )

        # Création de l'emprunt
        aujourd_hui = date.today()
        emprunt = Emprunt(
            id=self.db.prochain_id("emprunts"),
            usager_id=usager_id,
            livre_id=livre_id,
            personnel_id=self.session.personnel.id if self.session.personnel.id else None,
            date_emprunt=aujourd_hui,
            date_retour_prevue=aujourd_hui + timedelta(days=DUREE_EMPRUNT_JOURS),
            statut=StatutEmprunt.EN_COURS,
        )
        self.db.emprunts.append(emprunt)
        livre.stock -= 1

        # Si une réservation de CET usager existait, on l'honore
        if resa and resa.usager_id == usager_id:
            resa.statut = StatutReservation.HONOREE

        self.db.sauvegarder()
        return emprunt

    def retourner_emprunt(self, emprunt_id: int) -> Emprunt:
        self._verifier_ecriture()
        emprunt = self._trouver_emprunt(emprunt_id)
        if emprunt.statut == StatutEmprunt.RENDU:
            raise PermissionRefusee("Cet emprunt est déjà rendu.")

        emprunt.date_retour_effective = date.today()
        emprunt.statut = StatutEmprunt.RENDU

        livre = self.trouver_livre(emprunt.livre_id)
        livre.stock += 1

        # Notifier le prochain réservant
        self._notifier_prochain_reservant(livre.id)

        self.db.sauvegarder()
        return emprunt

    def lister_emprunts(self, en_cours_seulement: bool = False) -> list[Emprunt]:
        self._rafraichir_retards()
        if en_cours_seulement:
            return [e for e in self.db.emprunts if e.statut != StatutEmprunt.RENDU]
        return list(self.db.emprunts)

    def _trouver_emprunt(self, emprunt_id: int) -> Emprunt:
        for e in self.db.emprunts:
            if e.id == emprunt_id:
                return e
        raise EntiteIntrouvable(f"Emprunt id={emprunt_id} introuvable.")

    def _rafraichir_retards(self) -> None:
        """Marque automatiquement les emprunts en retard."""
        modifie = False
        for e in self.db.emprunts:
            if e.statut == StatutEmprunt.EN_COURS and e.est_en_retard():
                e.statut = StatutEmprunt.EN_RETARD
                modifie = True
        if modifie:
            self.db.sauvegarder()

    # ==========================================================
    #  RESERVATIONS
    # ==========================================================

    def reserver(self, usager_id: int, livre_id: int) -> Reservation:
        self._verifier_ecriture()
        usager = self.trouver_usager(usager_id)
        livre = self.trouver_livre(livre_id)

        # Pas de doublon
        for r in self.db.reservations:
            if (r.usager_id == usager_id
                    and r.livre_id == livre_id
                    and r.statut in (StatutReservation.EN_ATTENTE,
                                     StatutReservation.DISPONIBLE)):
                raise DejaReserve(
                    f"{usager.get_nom_complet()} a déjà une réservation active."
                )

        # Livre dispo → réservation immédiate DISPONIBLE (à venir chercher)
        # Livre indispo → EN_ATTENTE
        statut = (StatutReservation.DISPONIBLE
                  if livre.est_disponible()
                  else StatutReservation.EN_ATTENTE)

        # Réservation = blocage du stock
        if statut == StatutReservation.DISPONIBLE:
            livre.stock -= 1

        aujourd_hui = date.today()
        resa = Reservation(
            id=self.db.prochain_id("reservations"),
            usager_id=usager_id,
            livre_id=livre_id,
            date_reservation=aujourd_hui,
            date_expiration=(aujourd_hui + timedelta(days=DUREE_RESERVATION_JOURS)
                             if statut == StatutReservation.DISPONIBLE
                             else None),
            statut=statut,
        )
        self.db.reservations.append(resa)
        self.db.sauvegarder()
        return resa

    def annuler_reservation(self, reservation_id: int) -> Reservation:
        self._verifier_ecriture()
        resa = self._trouver_reservation(reservation_id)
        if resa.statut in (StatutReservation.ANNULEE, StatutReservation.HONOREE):
            return resa

        # Si elle bloquait le stock, on le libère
        if resa.statut == StatutReservation.DISPONIBLE:
            livre = self.trouver_livre(resa.livre_id)
            livre.stock += 1
            self._notifier_prochain_reservant(livre.id)

        resa.statut = StatutReservation.ANNULEE
        self.db.sauvegarder()
        return resa

    def lister_reservations(self) -> list[Reservation]:
        self._rafraichir_reservations()
        return list(self.db.reservations)

    def _trouver_reservation(self, resa_id: int) -> Reservation:
        for r in self.db.reservations:
            if r.id == resa_id:
                return r
        raise EntiteIntrouvable(f"Réservation id={resa_id} introuvable.")

    def _rafraichir_reservations(self) -> None:
        """Passe les réservations DISPONIBLE expirées en ANNULEE."""
        modifie = False
        for r in self.db.reservations:
            if (r.statut == StatutReservation.DISPONIBLE
                    and r.est_expiree()):
                r.statut = StatutReservation.ANNULEE
                livre = self.trouver_livre(r.livre_id)
                livre.stock += 1
                self._notifier_prochain_reservant(livre.id)
                modifie = True
        if modifie:
            self.db.sauvegarder()

    def _premiere_reservation_active(self, livre_id: int) -> Optional[Reservation]:
        """Première réservation DISPONIBLE ou EN_ATTENTE pour un livre."""
        for r in sorted(self.db.reservations, key=lambda x: x.id):
            if r.livre_id == livre_id and r.statut in (
                    StatutReservation.EN_ATTENTE,
                    StatutReservation.DISPONIBLE):
                return r
        return None

    def _notifier_prochain_reservant(self, livre_id: int) -> Optional[Reservation]:
        """
        Passe la première réservation EN_ATTENTE en DISPONIBLE
        et bloque le stock. Appelée quand un livre redevient dispo.
        """
        for r in sorted(self.db.reservations, key=lambda x: x.id):
            if (r.livre_id == livre_id
                    and r.statut == StatutReservation.EN_ATTENTE):
                livre = self.trouver_livre(livre_id)
                if livre.stock > 0:
                    livre.stock -= 1
                    r.statut = StatutReservation.DISPONIBLE
                    r.date_expiration = (date.today()
                                         + timedelta(days=DUREE_RESERVATION_JOURS))
                    return r
        return None