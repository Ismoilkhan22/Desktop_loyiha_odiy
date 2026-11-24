"""9-qadam: asosiy oyna. Chapda menyu, o'ngda sahifalar.
Ishga tushirish:  python -m app.main"""
import sys

import psycopg2
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QMainWindow, QMessageBox, QStackedWidget,
                             QWidget)

from . import db
from .pages import modules
from .pages.crud import CrudPage
from .pages.dashboard import Dashboard
from .pages.report import ReportPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Talabalar boshqaruvi")
        self.resize(1000, 600)

        pages = [("Bosh sahifa", Dashboard())]
        pages += [(m.title, CrudPage(m)) for m in modules.ALL]
        pages.append(("Hisobot", ReportPage()))

        self.menu = QListWidget()
        self.menu.setFixedWidth(170)
        self.stack = QStackedWidget()
        for title, page in pages:
            self.menu.addItem(title)
            self.stack.addWidget(page)

        self.menu.currentRowChanged.connect(self.show_page)
        root = QWidget()
        lay = QHBoxLayout(root)
        lay.addWidget(self.menu)
        lay.addWidget(self.stack)
        self.setCentralWidget(root)
        self.menu.setCurrentRow(0)

    def show_page(self, row):
        self.stack.setCurrentIndex(row)
        self.stack.currentWidget().refresh()  # har ochilganda bazadan yangidan o'qiydi


def main():
    app = QApplication(sys.argv)
    try:
        db.query("SELECT 1")
    except psycopg2.Error as e:
        QMessageBox.critical(None, "Bazaga ulanib bo'lmadi",
                             f"{e}\n\nPostgreSQL ishlayaptimi? 'python -m app.init_db' bajarilganmi?")
        return 1
    win = MainWindow()
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
