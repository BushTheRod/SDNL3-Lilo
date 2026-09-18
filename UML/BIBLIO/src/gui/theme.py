#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/theme.py

"""
Thèmes QSS clair et sombre.
"""

THEME_SOMBRE = """
QWidget {
    background-color: #1e1e2e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 10pt;
}

QMainWindow, QDialog {
    background-color: #1e1e2e;
}

/* ---------- Menu latéral ---------- */
#SideBar {
    background-color: #181825;
    border-right: 1px solid #313244;
}
#SideBar QPushButton {
    background-color: transparent;
    color: #cdd6f4;
    border: none;
    padding: 12px 18px;
    text-align: left;
    font-size: 10.5pt;
    border-radius: 6px;
    margin: 2px 8px;
}
#SideBar QPushButton:hover {
    background-color: #313244;
}
#SideBar QPushButton:checked {
    background-color: #45475a;
    color: #f5e0dc;
    font-weight: bold;
}
#Logo {
    color: #f5e0dc;
    font-size: 16pt;
    font-weight: bold;
    padding: 20px 18px;
}

/* ---------- Boutons génériques ---------- */
QPushButton {
    background-color: #313244;
    color: #e0e0e0;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 7px 14px;
}
QPushButton:hover {
    background-color: #45475a;
}
QPushButton:pressed {
    background-color: #585b70;
}
QPushButton:disabled {
    background-color: #252535;
    color: #6c6c80;
}
QPushButton#Primary {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
    font-weight: bold;
}
QPushButton#Primary:hover {
    background-color: #a6c8ff;
}
QPushButton#Danger {
    background-color: #f38ba8;
    color: #1e1e2e;
    border: none;
    font-weight: bold;
}
QPushButton#Danger:hover {
    background-color: #ffa0bd;
}

/* ---------- Champs ---------- */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background-color: #313244;
    color: #e0e0e0;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #89b4fa;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}

/* ---------- Tableaux ---------- */
QTableWidget {
    background-color: #252535;
    alternate-background-color: #2a2a3c;
    gridline-color: #313244;
    border: 1px solid #313244;
    border-radius: 6px;
    selection-background-color: #45475a;
    selection-color: #f5e0dc;
}
QHeaderView::section {
    background-color: #181825;
    color: #cdd6f4;
    padding: 8px;
    border: none;
    border-right: 1px solid #313244;
    font-weight: bold;
}
QTableWidget QTableCornerButton::section {
    background-color: #181825;
}

/* ---------- Barres de défilement ---------- */
QScrollBar:vertical {
    background: #1e1e2e;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #585b70;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ---------- Messages ---------- */
QMessageBox {
    background-color: #1e1e2e;
}
"""


THEME_CLAIR = """
QWidget {
    background-color: #f5f5f7;
    color: #1e1e2e;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 10pt;
}

QMainWindow, QDialog {
    background-color: #f5f5f7;
}

#SideBar {
    background-color: #e8e8ee;
    border-right: 1px solid #d0d0da;
}
#SideBar QPushButton {
    background-color: transparent;
    color: #2a2a3c;
    border: none;
    padding: 12px 18px;
    text-align: left;
    font-size: 10.5pt;
    border-radius: 6px;
    margin: 2px 8px;
}
#SideBar QPushButton:hover {
    background-color: #d8d8e2;
}
#SideBar QPushButton:checked {
    background-color: #c5c5d5;
    color: #1e1e2e;
    font-weight: bold;
}
#Logo {
    color: #2a2a3c;
    font-size: 16pt;
    font-weight: bold;
    padding: 20px 18px;
}

QPushButton {
    background-color: #e0e0e8;
    color: #1e1e2e;
    border: 1px solid #c0c0d0;
    border-radius: 6px;
    padding: 7px 14px;
}
QPushButton:hover {
    background-color: #d0d0da;
}
QPushButton:pressed {
    background-color: #b8b8c8;
}
QPushButton:disabled {
    background-color: #ececec;
    color: #a0a0a8;
}
QPushButton#Primary {
    background-color: #4a7dd6;
    color: #ffffff;
    border: none;
    font-weight: bold;
}
QPushButton#Primary:hover {
    background-color: #5a8de6;
}
QPushButton#Danger {
    background-color: #d64545;
    color: #ffffff;
    border: none;
    font-weight: bold;
}
QPushButton#Danger:hover {
    background-color: #e65555;
}

QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background-color: #ffffff;
    color: #1e1e2e;
    border: 1px solid #c0c0d0;
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: #4a7dd6;
    selection-color: #ffffff;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #4a7dd6;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}

QTableWidget {
    background-color: #ffffff;
    alternate-background-color: #f5f5f7;
    gridline-color: #e0e0e8;
    border: 1px solid #d0d0da;
    border-radius: 6px;
    selection-background-color: #d0e0f8;
    selection-color: #1e1e2e;
}
QHeaderView::section {
    background-color: #e8e8ee;
    color: #2a2a3c;
    padding: 8px;
    border: none;
    border-right: 1px solid #d0d0da;
    font-weight: bold;
}
QTableWidget QTableCornerButton::section {
    background-color: #e8e8ee;
}

QScrollBar:vertical {
    background: #f5f5f7;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #c0c0d0;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #a8a8b8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QMessageBox {
    background-color: #f5f5f7;
}
"""


def get_theme(nom: str) -> str:
    """Retourne la QSS selon 'sombre' ou 'clair'."""
    return THEME_SOMBRE if nom == "sombre" else THEME_CLAIR