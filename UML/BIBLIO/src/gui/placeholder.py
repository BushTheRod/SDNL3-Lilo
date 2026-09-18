#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# src/gui/placeholder.py

"""
Génère un QPixmap placeholder (livre stylisé avec ses initiales).
"""

from .qt_compat import Qt, QtCore, QtGui, QPixmap, QColor, QFont


def placeholder_livre(titre: str = "?", taille: int = 120) -> QPixmap:
    """
    Crée un QPixmap carré avec les initiales du titre.
    """
    pix = QPixmap(taille, taille)
    pix.fill(QColor("#45475a"))

    peintre = QtGui.QPainter(pix)
    try:
        peintre.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Bordure intérieure
        pen = QtGui.QPen(QColor("#89b4fa"))
        pen.setWidth(2)
        peintre.setPen(pen)
        peintre.drawRect(4, 4, taille - 8, taille - 8)

        # Initiales
        mots = [m for m in titre.split() if m]
        initiales = "".join(m[0].upper() for m in mots[:2]) or "?"
        police = QFont("Segoe UI", int(taille / 3))
        police.setBold(True)
        peintre.setFont(police)
        peintre.setPen(QColor("#cdd6f4"))
        peintre.drawText(pix.rect(),
                         Qt.AlignmentFlag.AlignCenter, initiales)
    finally:
        peintre.end()

    return pix