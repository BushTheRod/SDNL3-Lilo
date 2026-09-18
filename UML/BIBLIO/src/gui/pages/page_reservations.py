#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/page_reservations.py

from ..qt_compat import (
    Qt, QDialog, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidgetItem
)
from .page_base import PageBase
from ...core.exceptions import BiblioError


class DialogReservation(QDialog):

    def __init__(self, svc, parent=None):
        super().__init__(parent)
        self.svc = svc
        self.setWindowTitle("Nouvelle réservation")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.combo_usager = QComboBox()
        for u in svc.lister_usagers():
            self.combo_usager.addItem(f"{u.get_nom_complet()} (#{u.id})", u.id)

        self.combo_livre = QComboBox()
        for l in svc.lister_livres():
            self.combo_livre.addItem(
                f"{l.titre} — stock {l.stock} (#{l.id})", l.id
            )

        form.addRow("Usager", self.combo_usager)
        form.addRow("Livre", self.combo_livre)
        layout.addLayout(form)

        boutons = QHBoxLayout()
        boutons.addStretch()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.clicked.connect(self.reject)
        btn_valider = QPushButton("Réserver")
        btn_valider.setObjectName("Primary")
        btn_valider.clicked.connect(self._valider)
        boutons.addWidget(btn_annuler)
        boutons.addWidget(btn_valider)
        layout.addLayout(boutons)

    def _valider(self):
        if self.combo_usager.count() == 0 or self.combo_livre.count() == 0:
            QMessageBox.warning(self, "Impossible",
                                "Il faut au moins un usager et un livre.")
            return
        uid = self.combo_usager.currentData()
        lid = self.combo_livre.currentData()
        try:
            self.svc.reserver(uid, lid)
            self.accept()
        except BiblioError as e:
            QMessageBox.critical(self, "Erreur", str(e))


class PageReservations(PageBase):
    TITRE = "📌 Réservations"
    COLONNES = ["ID", "Usager", "Livre", "Réservé le",
                "Expire le", "Statut"]

    def __init__(self, svc, parent=None):
        super().__init__(svc, parent)

        if svc.session.peut_modifier():
            self.ajouter_bouton("➕ Réserver", self._nouvelle, "Primary")
            self.ajouter_bouton("❌ Annuler", self._annuler)

        self.rafraichir()

    def rafraichir(self):
        resas = self.svc.lister_reservations()
        self.table.setRowCount(len(resas))
        for i, r in enumerate(resas):
            try:
                nom_usager = self.svc.trouver_usager(r.usager_id).get_nom_complet()
            except BiblioError:
                nom_usager = f"#{r.usager_id}"
            try:
                titre_livre = self.svc.trouver_livre(r.livre_id).titre
            except BiblioError:
                titre_livre = f"#{r.livre_id}"

            valeurs = [
                str(r.id),
                nom_usager,
                titre_livre,
                r.date_reservation.isoformat() if r.date_reservation else "—",
                r.date_expiration.isoformat() if r.date_expiration else "—",
                r.statut.value,
            ]
            for j, v in enumerate(valeurs):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setData(Qt.ItemDataRole.UserRole, r.id)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def _nouvelle(self):
        dlg = DialogReservation(self.svc, self)
        if dlg.exec():
            self.rafraichir()

    def _annuler(self):
        rid = self.ligne_selectionnee_id()
        if rid is None:
            self._info("Sélectionne une réservation.")
            return
        if not self._confirm("Annuler cette réservation ?"):
            return
        try:
            self.svc.annuler_reservation(rid)
            self.rafraichir()
        except BiblioError as e:
            self._erreur(str(e))