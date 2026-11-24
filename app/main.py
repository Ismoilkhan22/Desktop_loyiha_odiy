"""9-qadam: asosiy oyna. Chapda menyu, o'ngda sahifalar.
Ishga tushirish:  python -m app.main"""
import sys

import mysql.connector
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QListWidget, QMainWindow, QMessageBox,
                             QStackedWidget, QVBoxLayout, QWidget)

from . import db
from .pages import modules
from .pages.crud import CrudPage
from .pages.dashboard import Dashboard
from .pages.report import ReportPage
from .style import QSS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Talabalar boshqaruvi")
        self.resize(1150, 700)

        pages = [("Bosh sahifa", Dashboard())]
        pages += [(m.title, CrudPage(m)) for m in modules.ALL]
        pages.append(("Hisobot", ReportPage()))

        self.menu = QListWidget()
        self.menu.setObjectName("menu")
        self.stack = QStackedWidget()
        for title, page in pages:
            self.menu.addItem(title)
            self.stack.addWidget(page)

        self.menu.currentRowChanged.connect(self.show_page)
        brand = QLabel("Talabalar\nboshqaruvi")
        brand.setObjectName("brand")
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(0, 0, 0, 0)
        side.addWidget(brand)
        side.addWidget(self.menu)

        self.title = QLabel()
        self.title.setObjectName("title")
        content = QVBoxLayout()
        content.setContentsMargins(24, 20, 24, 24)
        content.setSpacing(14)
        content.addWidget(self.title)
        content.addWidget(self.stack)

        root = QWidget()
        lay = QHBoxLayout(root)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(sidebar)
        lay.addLayout(content)
        self.setCentralWidget(root)
        self.menu.setCurrentRow(0)

    def show_page(self, row):
        self.stack.setCurrentIndex(row)
        self.title.setText(self.menu.item(row).text())
        self.stack.currentWidget().refresh()  # har ochilganda bazadan yangidan o'qiydi


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # hamma tizimda bir xil ko'rinish
    app.setStyleSheet(QSS)
    try:
        db.query("SELECT 1")
    except mysql.connector.Error as e:
        QMessageBox.critical(None, "Bazaga ulanib bo'lmadi",
                             f"{e}\n\nMySQL ishlayaptimi? 'python -m app.init_db' bajarilganmi?")
        return 1
    win = MainWindow()
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
