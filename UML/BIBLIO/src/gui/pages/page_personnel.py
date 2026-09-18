#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/page_personnel.py

from ..qt_compat import (
    Qt, QDialog, QLineEdit, QComboBox, QPushButton, QVBoxLayout,
    QHBoxLayout, QFormLayout, QMessageBox, QTableWidgetItem
)
from .page_base import PageBase
from ...core.enums import TypePersonnel
from ...core.exceptions import BiblioError


class DialogPersonnel(QDialog):

    def __init__(self, svc, parent=None):
        super().__init__(parent)
        self.svc = svc
        self.setWindowTitle("Nouveau membre du personnel")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.champ_nom = QLineEdit()
        self.champ_prenom = QLineEdit()
        self.champ_email = QLineEdit()
        self.champ_mdp = QLineEdit()
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.combo_type = QComboBox()
        for t in TypePersonnel:
            self.combo_type.addItem(t.value, t)

        form.addRow("Nom *", self.champ_nom)
        form.addRow("Prénom *", self.champ_prenom)
        form.addRow("Email *", self.champ_email)
        form.addRow("Mot de passe", self.champ_mdp)
        form.addRow("Type", self.combo_type)
        layout.addLayout(form)

        boutons = QHBoxLayout()
        boutons.addStretch()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.clicked.connect(self.reject)
        btn_valider = QPushButton("Créer")
        btn_valider.setObjectName("Primary")
        btn_valider.clicked.connect(self._valider)
        boutons.addWidget(btn_annuler)
        boutons.addWidget(btn_valider)
        layout.addLayout(boutons)

    def _valider(self):
        nom = self.champ_nom.text().strip()
        prenom = self.champ_prenom.text().strip()
        email = self.champ_email.text().strip()
        type_p = self.combo_type.currentData()
        mdp = self.champ_mdp.text().strip() or None

        if not nom or not prenom or not email:
            QMessageBox.warning(self, "Champs requis",
                                "Nom, prénom et email sont obligatoires.")
            return
        if type_p != TypePersonnel.GUEST and not mdp:
            QMessageBox.warning(self, "Mot de passe requis",
                                "Un ADMIN ou SUPERVISEUR doit avoir un mot de passe.")
            return
        if type_p == TypePersonnel.GUEST:
            mdp = None

        try:
            self.svc.ajouter_personnel(nom, prenom, email, mdp, type_p)
            self.accept()
        except BiblioError as e:
            QMessageBox.critical(self, "Erreur", str(e))


class PagePersonnel(PageBase):
    TITRE = "🔐 Personnel"
    COLONNES = ["ID", "Nom", "Prénom", "Email", "Type"]

    def __init__(self, svc, parent=None):
        super().__init__(svc, parent)
        self.ajouter_bouton("➕ Ajouter", self._ajouter, "Primary")
        self.rafraichir()

    def rafraichir(self):
        try:
            personnels = self.svc.lister_personnels()
        except BiblioError as e:
            self._erreur(str(e))
            personnels = []

        self.table.setRowCount(len(personnels))
        for i, p in enumerate(personnels):
            valeurs = [str(p.id), p.nom, p.prenom, p.email, p.type.value]
            for j, v in enumerate(valeurs):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setData(Qt.ItemDataRole.UserRole, p.id)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def _ajouter(self):
        dlg = DialogPersonnel(self.svc, self)
        if dlg.exec():
            self.rafraichir()