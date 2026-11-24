"""5-qadam: UNIVERSAL CRUD sahifa. 8 jadvalning hammasi shu bitta klass bilan ishlaydi,
farqi faqat modules.py dagi ta'rifda."""
from dataclasses import dataclass

import psycopg2
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (QComboBox, QDateEdit, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout,
                             QLineEdit, QMessageBox, QPushButton, QSpinBox, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from .. import db


@dataclass
class Field:
    column: str
    label: str
    kind: str = "text"  # text | int | date | fk
    fk_sql: str = ""    # fk uchun: "SELECT id, ko'rinadigan_nom FROM ..."
    lo: int = 0
    hi: int = 1_000_000


@dataclass
class Module:
    title: str
    table: str
    list_sql: str      # jadvalda ko'rinadigan SELECT (birinchi ustun doim id)
    headers: list
    fields: list
    search: tuple = ()      # qidiriladigan ustunlar
    filter_col: str = ""    # filtr ustuni (guruh bo'yicha)
    filter_sql: str = ""


class FormDialog(QDialog):
    """Qo'shish / tahrirlash oynasi. Maydon turiga qarab vidjet tanlanadi."""

    def __init__(self, module, values=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(module.title)
        self.fields = module.fields
        form = QFormLayout(self)
        self.widgets = []
        for i, f in enumerate(self.fields):
            w = self._make(f)
            if values is not None:
                self._set(w, f, values[i])
            self.widgets.append(w)
            form.addRow(f.label, w)
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    @staticmethod
    def _make(f):
        if f.kind == "int":
            w = QSpinBox()
            w.setRange(f.lo, f.hi)
        elif f.kind == "date":
            w = QDateEdit(QDate.currentDate())
            w.setCalendarPopup(True)
            w.setDisplayFormat("yyyy-MM-dd")
        elif f.kind == "fk":
            w = QComboBox()  # ekranda nom, ichida ID
            for id_, name in db.query(f.fk_sql):
                w.addItem(str(name), id_)
        else:
            w = QLineEdit()
        return w

    @staticmethod
    def _set(w, f, v):
        if f.kind == "int":
            w.setValue(v)
        elif f.kind == "date":
            w.setDate(QDate.fromString(str(v), "yyyy-MM-dd"))
        elif f.kind == "fk":
            w.setCurrentIndex(w.findData(v))
        else:
            w.setText(v)

    def values(self):
        out = []
        for f, w in zip(self.fields, self.widgets):
            if f.kind == "int":
                out.append(w.value())
            elif f.kind == "date":
                out.append(w.date().toString("yyyy-MM-dd"))
            elif f.kind == "fk":
                out.append(w.currentData())
            else:
                out.append(w.text().strip())
        return out

    def _accept(self):
        if any(v in ("", None) for v in self.values()):
            QMessageBox.warning(self, "Xato", "Barcha maydonlarni to'ldiring")
            return
        self.accept()


class CrudPage(QWidget):
    def __init__(self, module):
        super().__init__()
        self.m = module
        lay = QVBoxLayout(self)
        bar = QHBoxLayout()
        lay.addLayout(bar)

        self.search = QLineEdit()
        self.filter = QComboBox()
        if module.search:
            self.search.setPlaceholderText("Ism yoki familiya bo'yicha qidirish...")
            self.search.textChanged.connect(self.refresh)
            bar.addWidget(self.search)
        if module.filter_col:
            self.filter.currentIndexChanged.connect(self.refresh)
            bar.addWidget(self.filter)
        bar.addStretch()
        for text, slot in (("Qo'shish", self.on_add), ("Tahrirlash", self.on_edit), ("O'chirish", self.on_delete)):
            b = QPushButton(text)
            b.clicked.connect(slot)
            bar.addWidget(b)

        self.table = QTableWidget(0, len(module.headers))
        self.table.setHorizontalHeaderLabels(module.headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        lay.addWidget(self.table)

    # ---------- bazaga yozish (oynasiz, test qilish oson) ----------
    def insert(self, values):
        cols = [f.column for f in self.m.fields]
        marks = ", ".join(["%s"] * len(cols))
        db.execute(f"INSERT INTO {self.m.table} ({', '.join(cols)}) VALUES ({marks})", values)

    def update(self, id_, values):
        sets = ", ".join(f"{f.column} = %s" for f in self.m.fields)
        db.execute(f"UPDATE {self.m.table} SET {sets} WHERE id = %s", [*values, id_])

    def delete(self, id_):
        db.execute(f"DELETE FROM {self.m.table} WHERE id = %s", (id_,))

    # ---------- jadvalni yangilash ----------
    def refresh(self):
        m = self.m
        if m.filter_col and self.filter.count() == 0:
            self.filter.blockSignals(True)
            self.filter.addItem("Barcha guruhlar", None)
            for id_, name in db.query(m.filter_sql):
                self.filter.addItem(str(name), id_)
            self.filter.blockSignals(False)

        where, params = [], []
        text = self.search.text().strip()
        if m.search and text:
            where.append("(" + " OR ".join(f"{c} ILIKE %s" for c in m.search) + ")")
            params += [f"%{text}%"] * len(m.search)
        if m.filter_col and self.filter.currentData() is not None:
            where.append(f"{m.filter_col} = %s")
            params.append(self.filter.currentData())
        sql = m.list_sql + (" WHERE " + " AND ".join(where) if where else "") + " ORDER BY 1"

        rows = db.query(sql, params)
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    # ---------- tugmalar ----------
    def _selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Eslatma", "Avval jadvaldan qatorni tanlang")
            return None
        return int(self.table.item(row, 0).text())

    def _save(self, action, *args):
        try:
            action(*args)
        except psycopg2.errors.ForeignKeyViolation:
            QMessageBox.warning(self, "Xato", "Bu yozuv boshqa jadvalda ishlatilgan, o'chirib bo'lmaydi")
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Baza xatosi", str(e))
        else:
            self.refresh()

    def on_add(self):
        dlg = FormDialog(self.m, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            self._save(self.insert, dlg.values())

    def on_edit(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        cols = ", ".join(f.column for f in self.m.fields)
        current = db.query(f"SELECT {cols} FROM {self.m.table} WHERE id = %s", (id_,))[0]
        dlg = FormDialog(self.m, current, self)
        if dlg.exec_() == QDialog.Accepted:
            self._save(self.update, id_, dlg.values())

    def on_delete(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        ok = QMessageBox.question(self, "Tasdiqlash", "Rostdan o'chirasizmi?")
        if ok == QMessageBox.Yes:
            self._save(self.delete, id_)
