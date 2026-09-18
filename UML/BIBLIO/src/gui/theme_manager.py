#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/theme_manager.py

from .qt_compat import QApplication
from .theme import get_theme


class ThemeManager:

    def __init__(self, app: QApplication, theme_initial: str = "sombre"):
        self.app = app
        self.theme = theme_initial
        self.appliquer()

    def nom_actuel(self) -> str:
        return self.theme

    def appliquer(self):
        self.app.setStyleSheet(get_theme(self.theme))

    def basculer(self) -> str:
        self.theme = "clair" if self.theme == "sombre" else "sombre"
        self.appliquer()
        return self.theme