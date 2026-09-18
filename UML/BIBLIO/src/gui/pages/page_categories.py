#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/page_categories.py

from ..qt_compat import (
    Qt, QInputDialog, QLineEdit, QTableWidgetItem
)
from .page_base import PageBase
from ...core.exceptions import BiblioError


class PageCategories(PageBase):
    TITRE = "🏷️ Catégories"
    COLONNES = ["ID", "Nom"]

    def __init__(self, svc, parent=None):
        super().__init__(svc, parent)

        if svc.session.peut_modifier():
            self.ajouter_bouton("➕ Ajouter", self._ajouter, "Primary")
        if svc.session.peut_supprimer():
            self.ajouter_bouton("🗑️ Supprimer", self._supprimer, "Danger")

        self.rafraichir()

    def rafraichir(self):
        cats = self.svc.lister_categories()
        self.table.setRowCount(len(cats))
        for i, c in enumerate(cats):
            for j, v in enumerate([str(c.id), c.nom]):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setData(Qt.ItemDataRole.UserRole, c.id)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()

    def _ajouter(self):
        nom, ok = QInputDialog.getText(self, "Nouvelle catégorie",
                                       "Nom :", QLineEdit.EchoMode.Normal)
        if ok and nom.strip():
            try:
                self.svc.ajouter_categorie(nom.strip())
                self.rafraichir()
            except BiblioError as e:
                self._erreur(str(e))

    def _supprimer(self):
        cid = self.ligne_selectionnee_id()
        if cid is None:
            self._info("Sélectionne une catégorie.")
            return
        if not self._confirm("Supprimer cette catégorie ?"):
            return
        try:
            self.svc.supprimer_categorie(cid)
            self.rafraichir()
        except BiblioError as e:
            self._erreur(str(e))