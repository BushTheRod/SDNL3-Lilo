#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/page_usagers.py

from ..qt_compat import (
    Qt, QDialog, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidgetItem
)
from .page_base import PageBase
from ...core.exceptions import BiblioError


class DialogUsager(QDialog):

    def __init__(self, svc, usager=None, parent=None):
        super().__init__(parent)
        self.svc = svc
        self.usager = usager

        self.setWindowTitle("Modifier un usager" if usager else "Ajouter un usager")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.champ_nom = QLineEdit(usager.nom if usager else "")
        self.champ_prenom = QLineEdit(usager.prenom if usager else "")
        self.champ_email = QLineEdit(usager.email if usager else "")
        self.champ_tel = QLineEdit(usager.telephone if usager else "")

        form.addRow("Nom *", self.champ_nom)
        form.addRow("Prénom *", self.champ_prenom)
        form.addRow("Email", self.champ_email)
        form.addRow("Téléphone", self.champ_tel)
        layout.addLayout(form)

        boutons = QHBoxLayout()
        boutons.addStretch()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.clicked.connect(self.reject)
        btn_valider = QPushButton("Enregistrer")
        btn_valider.setObjectName("Primary")
        btn_valider.clicked.connect(self._valider)
        boutons.addWidget(btn_annuler)
        boutons.addWidget(btn_valider)
        layout.addLayout(boutons)

    def _valider(self):
        nom = self.champ_nom.text().strip()
        prenom = self.champ_prenom.text().strip()
        if not nom or not prenom:
            QMessageBox.warning(self, "Champs requis", "Nom et prénom requis.")
            return
        try:
            if self.usager:
                self.svc.modifier_livre  # placeholder never reached
            else:
                self.svc.ajouter_usager(
                    nom=nom, prenom=prenom,
                    email=self.champ_email.text().strip(),
                    telephone=self.champ_tel.text().strip(),
                )
            self.accept()
        except BiblioError as e:
            QMessageBox.critical(self, "Erreur", str(e))


class PageUsagers(PageBase):
    TITRE = "👥 Usagers"
    COLONNES = ["ID", "Nom", "Prénom", "Email", "Téléphone", "Inscrit le"]

    def __init__(self, svc, parent=None):
        super().__init__(svc, parent)

        if svc.session.peut_modifier():
            self.ajouter_bouton("➕ Ajouter", self._ajouter, "Primary")
        if svc.session.peut_supprimer():
            self.ajouter_bouton("🗑️ Supprimer", self._supprimer, "Danger")

        self.rafraichir()

    def rafraichir(self):
        usagers = self.svc.lister_usagers()
        self.table.setRowCount(len(usagers))
        for i, u in enumerate(usagers):
            date_str = u.date_inscription.isoformat() if u.date_inscription else "—"
            valeurs = [str(u.id), u.nom, u.prenom, u.email, u.telephone, date_str]
            for j, v in enumerate(valeurs):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setData(Qt.ItemDataRole.UserRole, u.id)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def _ajouter(self):
        dlg = DialogUsager(self.svc, None, self)
        if dlg.exec():
            self.rafraichir()

    def _supprimer(self):
        uid = self.ligne_selectionnee_id()
        if uid is None:
            self._info("Sélectionne un usager.")
            return
        if not self._confirm("Supprimer cet usager ?"):
            return
        try:
            self.svc.supprimer_usager(uid)
            self.rafraichir()
        except BiblioError as e:
            self._erreur(str(e))