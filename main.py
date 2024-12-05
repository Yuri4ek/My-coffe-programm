import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, \
    QLabel, QVBoxLayout

import sqlite3


class CustomDialog(QDialog):
    def __init__(self, coffe):
        super().__init__()

        text = f"Название сорта: {coffe[1]}\n" \
               f"Степень обжарки: {coffe[2]}\n" \
               f"Молотый/в зернах: {coffe[3]}\n" \
               f"Вкус: {coffe[4]}\n" \
               f"Цена: {coffe[5]}\n" \
               f"Обьем упаковки: {coffe[6]}"

        self.setWindowTitle("Coffe")

        layout = QVBoxLayout()
        message = QLabel(text)
        layout.addWidget(message)
        self.setLayout(layout)


class CoffeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        con = sqlite3.connect("coffee.sqlite")

        with con:
            sql = f"""SELECT * FROM coffe"""
            self.coffes = list(con.execute(sql))

        for coffe in self.coffes:
            c_btn = QPushButton(coffe[1])
            c_btn.resize(740, 40)
            c_btn.clicked.connect(self.click_coffe)

            self.verticalLayout.addWidget(c_btn)

    def click_coffe(self):
        name = self.sender().text()

        for coffe in self.coffes:
            if coffe[1] == name:
                CustomDialog(coffe).exec()

                break


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeWindow()
    ex.show()
    sys.exit(app.exec())
