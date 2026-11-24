"""4-qadam: oddiy ustunli diagramma (QPainter bilan, qo'shimcha kutubxonasiz)."""
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget


class BarChart(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.data = []  # [(yorliq, qiymat), ...]
        self.setMinimumHeight(220)

    def set_data(self, data):
        self.data = [(label, float(value)) for label, value in data]
        self.update()  # qayta chizadi

    def paintEvent(self, _):
        p = QPainter(self)
        p.drawText(10, 20, self.title)
        if not self.data:
            p.drawText(10, 50, "Ma'lumot yo'q")
            return
        top = max(v for _, v in self.data) or 1
        slot = (self.width() - 20) / len(self.data)
        h = self.height() - 80
        for i, (label, v) in enumerate(self.data):
            bar_h = h * v / top
            x = 10 + i * slot
            p.fillRect(QRectF(x + slot * 0.15, 50 + h - bar_h, slot * 0.7, bar_h), QColor("#3b82f6"))
            p.drawText(QRectF(x, 30 + h - bar_h, slot, 18), Qt.AlignCenter, f"{v:g}")
            p.drawText(QRectF(x, 54 + h, slot, 20), Qt.AlignCenter, str(label))
