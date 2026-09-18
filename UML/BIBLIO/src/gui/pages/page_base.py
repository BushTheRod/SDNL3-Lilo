#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/pages/page_base.py

from ..qt_compat import (
    Qt, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)


class PageBase(QWidget):
    """
    Structure standard :
    - Header (titre + boutons)
    - Tableau
    """

    TITRE = "Page"
    COLONNES: list[str] = []

    def __init__(self, svc, parent=None):
        super().__init__(parent)
        self.svc = svc

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ----- Header -----
        header = QHBoxLayout()
        titre = QLabel(self.TITRE)
        titre.setStyleSheet("font-size: 18pt; font-weight: bold;")
        header.addWidget(titre)
        header.addStretch()

        self.boutons_header = QHBoxLayout()
        header.addLayout(self.boutons_header)
        layout.addLayout(header)

        # ----- Tableau -----
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLONNES))
        self.table.setHorizontalHeaderLabels(self.COLONNES)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive)
        layout.addWidget(self.table, 1)

    def ajouter_bouton(self, texte: str, callback,
                       style: str = "", cote_droite: bool = True):
        btn = QPushButton(texte)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if style:
            btn.setObjectName(style)
        btn.clicked.connect(callback)
        if cote_droite:
            self.boutons_header.addWidget(btn)
        else:
            self.boutons_header.insertWidget(0, btn)
        return btn

    def ligne_selectionnee_id(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return int(item.data(Qt.ItemDataRole.UserRole))

    def rafraichir(self):
        """À surcharger."""
        pass

    def _erreur(self, message: str):
        QMessageBox.critical(self, "Erreur", message)

    def _info(self, message: str):
        QMessageBox.information(self, "Info", message)

    def _confirm(self, message: str) -> bool:
        rep = QMessageBox.question(
            self, "Confirmation", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return rep == QMessageBox.StandardButton.Yes