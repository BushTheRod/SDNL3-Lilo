#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/pages_livres.py

from ..qt_compat import (
    Qt, QPixmap, QLabel, QDialog, QLineEdit, QSpinBox, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
    QFileDialog, QListWidget, QListWidgetItem
)
from .page_base import PageBase
from ...core.exceptions import BiblioError
from ..placeholder import placeholder_livre
from ...utils.paths import dossier_datas
from ..qt_compat import QTableWidgetItem


class DialogLivre(QDialog):
    """Formulaire d'ajout / édition d'un livre."""

    def __init__(self, svc, livre=None, parent=None):
        super().__init__(parent)
        self.svc = svc
        self.livre = livre
        self.image_choisie: str = livre.image if livre else ""

        self.setWindowTitle("Modifier un livre" if livre else "Ajouter un livre")
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.champ_titre = QLineEdit(livre.titre if livre else "")
        self.champ_auteur = QLineEdit(livre.auteur if livre else "")
        self.champ_isbn = QLineEdit(livre.isbn if livre else "")
        self.champ_annee = QSpinBox()
        self.champ_annee.setRange(0, 2100)
        self.champ_annee.setValue(livre.annee_publication or 0)
        self.champ_stock = QSpinBox()
        self.champ_stock.setRange(0, 9999)
        self.champ_stock.setValue(livre.stock if livre else 1)

        form.addRow("Titre *", self.champ_titre)
        form.addRow("Auteur *", self.champ_auteur)
        form.addRow("ISBN", self.champ_isbn)
        form.addRow("Année", self.champ_annee)
        form.addRow("Stock", self.champ_stock)

        # ----- Image -----
        img_layout = QHBoxLayout()
        self.apercu = QLabel()
        self.apercu.setFixedSize(120, 120)
        self.apercu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._maj_apercu()
        img_layout.addWidget(self.apercu)

        img_boutons = QVBoxLayout()
        btn_choisir = QPushButton("Choisir une image…")
        btn_choisir.clicked.connect(self._choisir_image)
        btn_retirer = QPushButton("Retirer")
        btn_retirer.clicked.connect(self._retirer_image)
        img_boutons.addWidget(btn_choisir)
        img_boutons.addWidget(btn_retirer)
        img_boutons.addStretch()
        img_layout.addLayout(img_boutons)
        img_layout.addStretch()

        conteneur_img = QLabel("Image")
        form.addRow(conteneur_img, img_layout)

        # ----- Catégories -----
        self.liste_cats = QListWidget()
        self.liste_cats.setFixedHeight(120)
        cats_livre = set(livre.categories) if livre else set()
        for c in svc.lister_categories():
            item = QListWidgetItem(c.nom)
            item.setData(Qt.ItemDataRole.UserRole, c.id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if c.id in cats_livre
                else Qt.CheckState.Unchecked
            )
            self.liste_cats.addItem(item)
        form.addRow("Catégories", self.liste_cats)

        layout.addLayout(form)

        # ----- Boutons -----
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

    def _maj_apercu(self):
        chemin = dossier_datas() / self.image_choisie if self.image_choisie else None
        if chemin and chemin.exists():
            pix = QPixmap(str(chemin)).scaled(
                120, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            pix = placeholder_livre(self.champ_titre.text() or "?", 120)
        self.apercu.setPixmap(pix)

    def _choisir_image(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self, "Choisir une image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if not chemin:
            return
        # Copie dans datas/
        from pathlib import Path
        import shutil
        src = Path(chemin)
        dest = dossier_datas() / src.name
        try:
            shutil.copy2(src, dest)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Copie impossible : {e}")
            return
        self.image_choisie = src.name
        self._maj_apercu()

    def _retirer_image(self):
        self.image_choisie = ""
        self._maj_apercu()

    def _valider(self):
        titre = self.champ_titre.text().strip()
        auteur = self.champ_auteur.text().strip()
        if not titre or not auteur:
            QMessageBox.warning(self, "Champs requis",
                                "Titre et auteur sont obligatoires.")
            return

        cats = []
        for i in range(self.liste_cats.count()):
            item = self.liste_cats.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                cats.append(item.data(Qt.ItemDataRole.UserRole))

        try:
            if self.livre:
                self.svc.modifier_livre(
                    self.livre.id,
                    titre=titre, auteur=auteur,
                    isbn=self.champ_isbn.text().strip(),
                    annee_publication=self.champ_annee.value() or None,
                    stock=self.champ_stock.value(),
                    image=self.image_choisie,
                    categories=cats,
                )
            else:
                self.svc.ajouter_livre(
                    isbn=self.champ_isbn.text().strip(),
                    titre=titre, auteur=auteur,
                    stock=self.champ_stock.value(),
                    image=self.image_choisie,
                    annee_publication=self.champ_annee.value() or None,
                    categories=cats,
                )
            self.accept()
        except BiblioError as e:
            QMessageBox.critical(self, "Erreur", str(e))


class PageLivres(PageBase):
    TITRE = "📖 Livres"
    COLONNES = ["ID", "Titre", "Auteur", "ISBN", "Année", "Stock", "Image"]

    def __init__(self, svc, parent=None):
        super().__init__(svc, parent)

        if svc.session.peut_modifier():
            self.ajouter_bouton("➕ Ajouter", self._ajouter, "Primary")
            self.ajouter_bouton("✏️ Modifier", self._modifier)
        if svc.session.peut_supprimer():
            self.ajouter_bouton("🗑️ Supprimer", self._supprimer, "Danger")

        self.rafraichir()

    def rafraichir(self):
        livres = self.svc.lister_livres()
        self.table.setRowCount(len(livres))
        for i, l in enumerate(livres):
            valeurs = [
                str(l.id), l.titre, l.auteur, l.isbn,
                str(l.annee_publication or "—"), str(l.stock),
                l.image or "—",
            ]
            for j, v in enumerate(valeurs):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setData(Qt.ItemDataRole.UserRole, l.id)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def _item(self, texte: str):
        from ..qt_compat import QTableWidgetItem
        item = QTableWidgetItem(texte)
        return item

    def _ajouter(self):
        dlg = DialogLivre(self.svc, None, self)
        if dlg.exec():
            self.rafraichir()

    def _modifier(self):
        lid = self.ligne_selectionnee_id()
        if lid is None:
            self._info("Sélectionne un livre.")
            return
        try:
            livre = self.svc.trouver_livre(lid)
        except BiblioError as e:
            self._erreur(str(e))
            return
        dlg = DialogLivre(self.svc, livre, self)
        if dlg.exec():
            self.rafraichir()

    def _supprimer(self):
        lid = self.ligne_selectionnee_id()
        if lid is None:
            self._info("Sélectionne un livre.")
            return
        if not self._confirm("Supprimer ce livre ?"):
            return
        try:
            self.svc.supprimer_livre(lid)
            self.rafraichir()
        except BiblioError as e:
            self._erreur(str(e))