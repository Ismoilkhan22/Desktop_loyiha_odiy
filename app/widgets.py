"""4-qadam: oddiy ustunli diagramma (QPainter bilan, qo'shimcha kutubxonasiz)."""
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import QWidget


COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444']


class BarChart(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.data = []  # [(yorliq, qiymat), ...]
        self.setMinimumHeight(240)
        self.setObjectName("card")  # style.py dagi oq karta
        self.setAttribute(Qt.WA_StyledBackground)

    def set_data(self, data):
        self.data = [(label, float(value)) for label, value in data]
        self.update()  # qayta chizadi

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QColor("#0f172a"))
        bold = QFont(p.font())
        bold.setBold(True)
        p.setFont(bold)
        p.drawText(18, 30, self.title)
        bold.setBold(False)
        p.setFont(bold)
        p.setPen(QColor("#475569"))
        if not self.data:
            p.drawText(18, 60, "Ma'lumot yo'q")
            return
        top = max(v for _, v in self.data) or 1
        slot = (self.width() - 36) / len(self.data)
        h = self.height() - 110
        for i, (label, v) in enumerate(self.data):
            bar_h = h * v / top
            x = 18 + i * slot
            p.setBrush(QColor(COLORS[i % len(COLORS)]))
            p.setPen(Qt.NoPen)
            p.drawRoundedRect(QRectF(x + slot * 0.2, 60 + h - bar_h, slot * 0.6, bar_h), 6, 6)
            p.setPen(QColor("#475569"))
            p.drawText(QRectF(x, 40 + h - bar_h, slot, 18), Qt.AlignCenter, f"{v:g}")
            p.drawText(QRectF(x, 66 + h, slot, 20), Qt.AlignCenter, str(label))
