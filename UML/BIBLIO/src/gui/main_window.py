#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/main_window.py

from .qt_compat import (
    Qt, QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMessageBox
)
from .sidebar import SideBar
from .pages.page_livres import PageLivres
from .pages.page_usagers import PageUsagers
from .pages.page_emprunts import PageEmprunts
from .pages.page_reservations import PageReservations
from .pages.page_categories import PageCategories
from .pages.page_personnel import PagePersonnel
from ..core.auth import Session
from ..core.database import Database
from ..core.services import BiblioService


class MainWindow(QMainWindow):

    def __init__(self, db: Database, session: Session, theme_manager):
        super().__init__()
        self.db = db
        self.session = session
        self.theme_manager = theme_manager
        self.svc = BiblioService(db, session)

        self.setWindowTitle(f"Biblio — {session.personnel.prenom} "
                            f"({session.type.value})")
        self.resize(1200, 720)

        # ----- Menu latéral -----
        items = ["📖 Livres", "👥 Usagers", "📤 Emprunts",
                 "📌 Réservations", "🏷️ Catégories"]
        if session.peut_gerer_personnel():
            items.append("🔐 Personnel")

        self.sidebar = SideBar(items)
        self.sidebar.page_changee.connect(self._changer_page)
        self.sidebar.theme_toggle.connect(self._toggle_theme)
        self.sidebar.set_session(
            f"{session.personnel.prenom} {session.personnel.nom}\n"
            f"<small>{session.type.value}</small>"
        )
        self.sidebar.set_theme_label(theme_manager.nom_actuel())

        # ----- Pages -----
        self.stack = QStackedWidget()
        self.pages = [
            PageLivres(self.svc),
            PageUsagers(self.svc),
            PageEmprunts(self.svc),
            PageReservations(self.svc),
            PageCategories(self.svc),
        ]
        if session.peut_gerer_personnel():
            self.pages.append(PagePersonnel(self.svc))

        for p in self.pages:
            self.stack.addWidget(p)

        # ----- Layout -----
        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(central)

    def _changer_page(self, index: int):
        self.stack.setCurrentIndex(index)
        page = self.pages[index]
        if hasattr(page, "rafraichir"):
            page.rafraichir()

    def _toggle_theme(self):
        nouveau = self.theme_manager.basculer()
        self.sidebar.set_theme_label(nouveau)