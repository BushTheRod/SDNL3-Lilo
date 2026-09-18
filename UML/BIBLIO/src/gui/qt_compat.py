#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/qt_compat.py

"""
Abstraction PyQt6 / PySide6.
Importe automatiquement celui qui est disponible.
Priorité : PySide6 (licence LGPL) puis PyQt6.
"""

from __future__ import annotations

_QT_LIB = None

try:
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide6.QtCore import Signal, Slot  # type: ignore
    _QT_LIB = "PySide6"
except ImportError:
    try:
        from PyQt6 import QtCore, QtGui, QtWidgets  # type: ignore
        from PyQt6.QtCore import pyqtSignal as Signal  # type: ignore
        from PyQt6.QtCore import pyqtSlot as Slot  # type: ignore
        _QT_LIB = "PyQt6"
    except ImportError as e:
        raise ImportError(
            "Ni PySide6 ni PyQt6 n'est installé. "
            "Installe l'un des deux : pip install PySide6"
        ) from e


# ---------- Alias unifiés ----------

Qt = QtCore.Qt
QObject = QtCore.QObject
QSize = QtCore.QSize
QTimer = QtCore.QTimer
QDate = QtCore.QDate

QApplication = QtWidgets.QApplication
QWidget = QtWidgets.QWidget
QMainWindow = QtWidgets.QMainWindow
QDialog = QtWidgets.QDialog
QLabel = QtWidgets.QLabel
QPushButton = QtWidgets.QPushButton
QLineEdit = QtWidgets.QLineEdit
QTextEdit = QtWidgets.QTextEdit
QSpinBox = QtWidgets.QSpinBox
QComboBox = QtWidgets.QComboBox
QCheckBox = QtWidgets.QCheckBox
QListWidget = QtWidgets.QListWidget
QListWidgetItem = QtWidgets.QListWidgetItem
QTableWidget = QtWidgets.QTableWidget
QTableWidgetItem = QtWidgets.QTableWidgetItem
QHeaderView = QtWidgets.QHeaderView
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QGridLayout = QtWidgets.QGridLayout
QFormLayout = QtWidgets.QFormLayout
QStackedWidget = QtWidgets.QStackedWidget
QFrame = QtWidgets.QFrame
QScrollArea = QtWidgets.QScrollArea
QMessageBox = QtWidgets.QMessageBox
QFileDialog = QtWidgets.QFileDialog
QInputDialog = QtWidgets.QInputDialog
QSplitter = QtWidgets.QSplitter

QIcon = QtGui.QIcon
QPixmap = QtGui.QPixmap
QFont = QtGui.QFont
QColor = QtGui.QColor
QAction = QtGui.QAction


def lib_utilisee() -> str:
    """Retourne 'PySide6' ou 'PyQt6' — utile pour debug."""
    return _QT_LIB or "inconnue"