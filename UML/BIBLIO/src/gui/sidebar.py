#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/sidebar.py

from .qt_compat import (
    Qt, QWidget, QLabel, QPushButton, QVBoxLayout, QFrame,
    QSize, Signal
)


class SideBar(QFrame):
    """
    Menu latéral avec boutons exclusifs.
    Émet `page_changee(index)` quand on clique.
    """

    page_changee = Signal(int)
    theme_toggle = Signal()

    def __init__(self, items: list[str], parent=None):
        super().__init__(parent)
        self.setObjectName("SideBar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Logo
        logo = QLabel("📚 Biblio")
        logo.setObjectName("Logo")
        layout.addWidget(logo)

        # Boutons de navigation
        self.boutons: list[QPushButton] = []
        for i, texte in enumerate(items):
            btn = QPushButton(texte)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=i: self._clic(idx))
            layout.addWidget(btn)
            self.boutons.append(btn)

        # Marque le premier actif
        if self.boutons:
            self.boutons[0].setChecked(True)

        layout.addStretch()

        # Bouton thème
        self.btn_theme = QPushButton("🌙 Thème sombre")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.clicked.connect(self.theme_toggle.emit)
        layout.addWidget(self.btn_theme)

        # Info session
        self.label_session = QLabel("—")
        self.label_session.setContentsMargins(18, 6, 18, 18)
        layout.addWidget(self.label_session)

    def _clic(self, index: int):
        for i, b in enumerate(self.boutons):
            b.setChecked(i == index)
        self.page_changee.emit(index)

    def set_session(self, texte: str):
        self.label_session.setText(texte)

    def set_theme_label(self, nom_theme: str):
        if nom_theme == "sombre":
            self.btn_theme.setText("☀️ Thème clair")
        else:
            self.btn_theme.setText("🌙 Thème sombre")

    def activer(self, index: int):
        """Sélectionne un onglet programmatiquement."""
        self._clic(index)