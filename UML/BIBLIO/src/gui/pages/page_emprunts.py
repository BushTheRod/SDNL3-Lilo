#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/page_emprunts.py

from ..qt_compat import (
    Qt, QDialog, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidgetItem
)
from .page_base import PageBase
from ...core.enums import StatutEmprunt
from ...core.exceptions import BiblioError


class DialogEmprunt(QDialog):

    def __init__(self, svc, parent=None):
        super().__init__(parent)
        self.svc = svc
        self.setWindowTitle("Nouvel emprunt")
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
        btn_valider = QPushButton("Créer l'emprunt")
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
            self.svc.creer_emprunt(uid, lid)
            self.accept()
        except BiblioError as e:
            QMessageBox.critical(self, "Erreur", str(e))


class PageEmprunts(PageBase):
    TITRE = "📤 Emprunts"
    COLONNES = ["ID", "Usager", "Livre", "Emprunté le",
                "Retour prévu", "Retour effectif", "Statut"]

    def __init__(self, svc, parent=None):
        super().__init__(svc, parent)

        if svc.session.peut_modifier():
            self.ajouter_bouton("➕ Nouvel emprunt", self._nouveau, "Primary")
            self.ajouter_bouton("📥 Retourner", self._retourner)

        self.rafraichir()

    def rafraichir(self):
        emprunts = self.svc.lister_emprunts()
        self.table.setRowCount(len(emprunts))
        for i, e in enumerate(emprunts):
            try:
                nom_usager = self.svc.trouver_usager(e.usager_id).get_nom_complet()
            except BiblioError:
                nom_usager = f"#{e.usager_id}"
            try:
                titre_livre = self.svc.trouver_livre(e.livre_id).titre
            except BiblioError:
                titre_livre = f"#{e.livre_id}"

            valeurs = [
                str(e.id),
                nom_usager,
                titre_livre,
                e.date_emprunt.isoformat() if e.date_emprunt else "—",
                e.date_retour_prevue.isoformat() if e.date_retour_prevue else "—",
                e.date_retour_effective.isoformat() if e.date_retour_effective else "—",
                e.statut.value,
            ]
            for j, v in enumerate(valeurs):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setData(Qt.ItemDataRole.UserRole, e.id)
                if e.statut == StatutEmprunt.EN_RETARD and j == 6:
                    item.setForeground(Qt.GlobalColor.red)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def _nouveau(self):
        dlg = DialogEmprunt(self.svc, self)
        if dlg.exec():
            self.rafraichir()

    def _retourner(self):
        eid = self.ligne_selectionnee_id()
        if eid is None:
            self._info("Sélectionne un emprunt.")
            return
        if not self._confirm("Marquer cet emprunt comme rendu ?"):
            return
        try:
            self.svc.retourner_emprunt(eid)
            self.rafraichir()
        except BiblioError as e:
            self._erreur(str(e))