"""Tezkor tekshiruv (alohida test bazada). Ishga tushirish:
   DB_NAME=talaba_test python -m app.init_db && DB_NAME=talaba_test python -m tests.smoke_test"""
import os
import tempfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")  # oyna ochmasdan

import mysql.connector
from openpyxl import load_workbook
from PyQt5.QtWidgets import QApplication

from app import db
from app.main import MainWindow
from app.pages import modules
from app.pages.crud import CrudPage
from app.pages.report import ReportPage

app = QApplication([])
count = lambda t: db.query(f"SELECT COUNT(*) FROM {t}")[0][0]

# Butun oyna ochiladi va har bir sahifa bazadan o'qiydi
win = MainWindow()
for i in range(win.menu.count()):
    win.menu.setCurrentRow(i)
assert win.stack.widget(0).numbers["students"].text() == str(count("students"))

# CRUD: qo'shish -> tahrirlash -> o'chirish
page = CrudPage(modules.STUDENTS)
n = count("students")
page.insert(["Test", "Talaba", 1])
assert count("students") == n + 1
new_id = db.query("SELECT MAX(id) FROM students")[0][0]
page.update_row(new_id, ["Test2", "Talaba", 2])
assert db.query("SELECT first_name, group_id FROM students WHERE id=%s", (new_id,))[0] == ("Test2", 2)

# Qidiruv
page.search.setText("test2")
page.refresh()
assert page.table.rowCount() == 1

page.delete(new_id)
assert count("students") == n

# Bazaning o'zi ham xato qiymatni rad etadi
try:
    CrudPage(modules.GRADES).insert([1, 1, 150, "2026-11-01"])
    raise SystemExit("100 dan katta ball qabul qilindi!")
except mysql.connector.Error as e:
    assert e.errno == 3819, e  # CHECK cheklovi buzildi

# Bog'liq yozuv o'chirilmaydi (guruhda talabalar bor)
try:
    CrudPage(modules.GROUPS).delete(1)
    raise SystemExit("Bog'liq guruh o'chib ketdi!")
except mysql.connector.Error as e:
    assert e.errno == 1451, e  # bog'liq yozuv

# Excel eksport
rep = ReportPage()
rep.refresh()
path = os.path.join(tempfile.mkdtemp(), "h.xlsx")
rep.save_xlsx(path)
assert load_workbook(path).active.max_row == 1 + len(rep.rows)

print("Hammasi OK")
