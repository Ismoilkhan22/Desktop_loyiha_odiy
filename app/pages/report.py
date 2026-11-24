"""8-qadam: hisobot (guruh va fan bo'yicha filtr) + Excelga eksport."""
from openpyxl import Workbook
from PyQt5.QtWidgets import (QComboBox, QFileDialog, QHBoxLayout, QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from .. import db

HEADERS = ["Talaba", "Guruh", "Fan", "Ball", "Sana"]
SQL = """
SELECT st.last_name || ' ' || st.first_name, g.name, sub.name, gr.score, gr.graded_at
FROM grades gr
JOIN students st ON st.id = gr.student_id
JOIN groups g    ON g.id  = st.group_id
JOIN subjects sub ON sub.id = gr.subject_id
WHERE (%s IS NULL OR g.id = %s) AND (%s IS NULL OR sub.id = %s)
ORDER BY gr.graded_at DESC, 1
"""


class ReportPage(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        bar = QHBoxLayout()
        lay.addLayout(bar)
        self.group = QComboBox()
        self.subject = QComboBox()
        self.group.currentIndexChanged.connect(self.load)
        self.subject.currentIndexChanged.connect(self.load)
        bar.addWidget(self.group)
        bar.addWidget(self.subject)
        bar.addStretch()
        export = QPushButton("Excelga eksport")
        export.clicked.connect(self.export)
        bar.addWidget(export)

        self.table = QTableWidget(0, len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        lay.addWidget(self.table)
        self.rows = []

    def _fill_combo(self, combo, all_text, sql):
        combo.blockSignals(True)
        current = combo.currentData()
        combo.clear()
        combo.addItem(all_text, None)
        for id_, name in db.query(sql):
            combo.addItem(str(name), id_)
        combo.setCurrentIndex(max(combo.findData(current), 0))
        combo.blockSignals(False)

    def refresh(self):
        self._fill_combo(self.group, "Barcha guruhlar", "SELECT id, name FROM groups ORDER BY name")
        self._fill_combo(self.subject, "Barcha fanlar", "SELECT id, name FROM subjects ORDER BY name")
        self.load()

    def load(self):
        g, s = self.group.currentData(), self.subject.currentData()
        self.rows = db.query(SQL, (g, g, s, s))
        self.table.setRowCount(len(self.rows))
        for r, row in enumerate(self.rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Excelga saqlash", "hisobot.xlsx", "Excel (*.xlsx)")
        if path:
            self.save_xlsx(path)
            QMessageBox.information(self, "Tayyor", f"Saqlandi: {path}")

    def save_xlsx(self, path):
        wb = Workbook()
        ws = wb.active
        ws.append(HEADERS)
        for row in self.rows:  # faqat hozir filtrlangan natija yoziladi
            ws.append(list(row))
        wb.save(path)
