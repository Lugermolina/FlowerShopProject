# create an interactive Python program
# Author: Luis Gerardo Molina
"""
Date: Starting on Oct 11, 2026
Algorithm:
Class: Python Teams online class
Inputs: the state of the password, visible or hidden
Processing: drawing of a simple eye, an ellipse with a pupil, crossed by a diagonal
line while the password is hidden
Outputs: the icon displayed on the button beside a password field
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor

EYE_SIZE = 32
EYE_COLOR = '#333333'


def make_eye_icon(password_visible):
    pixmap = QPixmap(EYE_SIZE, EYE_SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(EYE_COLOR))
    pen.setWidth(2)
    painter.setPen(pen)

    painter.drawEllipse(3, 9, 26, 14)
    painter.setBrush(QColor(EYE_COLOR))
    painter.drawEllipse(12, 12, 8, 8)
    if not password_visible:
        painter.drawLine(5, 28, 27, 4)

    painter.end()
    return QIcon(pixmap)
