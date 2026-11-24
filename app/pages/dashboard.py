"""7-qadam: bosh sahifa. 4 ta hisoblagich COUNT(*) bilan, 2 ta diagramma."""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from .. import db
from ..widgets import BarChart

COUNTERS = [("Talabalar", "students"), ("O'qituvchilar", "teachers"),
            ("Fakultetlar", "faculties"), ("Guruhlar", "student_groups")]


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setSpacing(16)
        lay.setContentsMargins(0, 0, 0, 0)
        cards = QHBoxLayout()
        cards.setSpacing(16)
        lay.addLayout(cards)
        self.numbers = {}
        for title, table in COUNTERS:
            card = QFrame()
            card.setObjectName("card")
            card.setMaximumHeight(120)
            v = QVBoxLayout(card)
            num = QLabel("0")
            num.setAlignment(Qt.AlignCenter)
            num.setObjectName("cardnum")
            v.addWidget(num)
            name = QLabel(title)
            name.setObjectName("cardlabel")
            v.addWidget(name, alignment=Qt.AlignCenter)
            cards.addWidget(card)
            self.numbers[table] = num

        charts = QHBoxLayout()
        charts.setSpacing(16)
        lay.addLayout(charts)
        self.by_group = BarChart("Guruhlardagi talabalar soni")
        self.by_subject = BarChart("Fanlar bo'yicha o'rtacha ball")
        charts.addWidget(self.by_group)
        charts.addWidget(self.by_subject)

    def refresh(self):
        for _, table in COUNTERS:  # table nomi yuqoridagi doimiy ro'yxatdan, foydalanuvchidan emas
            self.numbers[table].setText(str(db.query(f"SELECT COUNT(*) FROM {table}")[0][0]))
        self.by_group.set_data(db.query(
            "SELECT g.name, COUNT(s.id) FROM student_groups g LEFT JOIN students s ON s.group_id = g.id "
            "GROUP BY g.id ORDER BY g.name"))
        self.by_subject.set_data(db.query(
            "SELECT sub.name, ROUND(AVG(gr.score), 1) FROM subjects sub JOIN grades gr ON gr.subject_id = sub.id "
            "GROUP BY sub.id ORDER BY sub.name"))
