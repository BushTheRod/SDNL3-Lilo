#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/main.py

"""
Point d'entrée de l'application Biblio.

Lancement : python -m src.main    (depuis la racine du projet)
"""

import sys

from src.core.auth import AuthService
from src.core.database import Database
from src.gui.qt_compat import QApplication, QMessageBox, lib_utilisee
from src.gui.theme_manager import ThemeManager
from src.gui.login_window import LoginWindow
from src.gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Biblio")

    theme_manager = ThemeManager(app, "sombre")

    try:
        db = Database()
        db.charger()
    except Exception as e:
        QMessageBox.critical(None, "Erreur base",
                             f"Impossible de charger la base :\n{e}")
        return 1

    print(f"Qt utilisé : {lib_utilisee()}")

    auth = AuthService(db)
    login = LoginWindow(auth)

    session_holder = {}

    def on_connexion(session):
        session_holder["session"] = session

    login.connexion_reussie.connect(on_connexion)

    if login.exec() != login.DialogCode.Accepted:
        return 0

    session = session_holder.get("session")
    if session is None:
        return 1

    win = MainWindow(db, session, theme_manager)
    win.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())