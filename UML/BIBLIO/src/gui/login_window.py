#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/login_window.py

from .qt_compat import (
    Qt, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QFrame, Signal
)
from ..core.auth import AuthService
from src.core.exceptions import AuthentificationEchouee


class LoginWindow(QDialog):
    """
    Fenêtre de connexion.
    - Email + mot de passe → ADMIN / SUPERVISEUR
    - Bouton "Accès invité" → GUEST
    """

    connexion_reussie = Signal(object)  # Session

    def __init__(self, auth: AuthService, parent=None):
        super().__init__(parent)
        self.auth = auth

        self.setWindowTitle("Biblio — Connexion")
        self.setFixedSize(400, 340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(14)

        # Titre
        titre = QLabel("📚 Biblio")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet("font-size: 22pt; font-weight: bold;")
        layout.addWidget(titre)

        sous_titre = QLabel("Gestion de bibliothèque")
        sous_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sous_titre.setStyleSheet("color: #888; margin-bottom: 15px;")
        layout.addWidget(sous_titre)

        # Champs
        self.champ_email = QLineEdit()
        self.champ_email.setPlaceholderText("Email")
        layout.addWidget(self.champ_email)

        self.champ_mdp = QLineEdit()
        self.champ_mdp.setPlaceholderText("Mot de passe")
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.champ_mdp.returnPressed.connect(self._connexion)
        layout.addWidget(self.champ_mdp)

        layout.addSpacing(10)

        # Boutons
        self.btn_connexion = QPushButton("Se connecter")
        self.btn_connexion.setObjectName("Primary")
        self.btn_connexion.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_connexion.clicked.connect(self._connexion)
        layout.addWidget(self.btn_connexion)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #45475a;")
        layout.addWidget(sep)

        self.btn_guest = QPushButton("👤 Accès invité (lecture seule)")
        self.btn_guest.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_guest.clicked.connect(self._connexion_guest)
        layout.addWidget(self.btn_guest)

        layout.addStretch()

    def _connexion(self):
        email = self.champ_email.text().strip()
        mdp = self.champ_mdp.text()

        if not email or not mdp:
            QMessageBox.warning(self, "Champs vides",
                                "Renseigne email et mot de passe.")
            return

        try:
            session = self.auth.connexion(email, mdp)
            self.connexion_reussie.emit(session)
            self.accept()
        except AuthentificationEchoue as e:
            QMessageBox.critical(self, "Échec", str(e))

    def _connexion_guest(self):
        session = self.auth.connexion_guest()
        self.connexion_reussie.emit(session)
        self.accept()