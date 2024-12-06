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


class Coffe_add_replace(QDialog):
    def __init__(self, command, name):
        self.command = command
        self.name = name

        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)

        self.add_replace.setText(command)

        self.add_replace.clicked.connect(self.run)

    def run(self):
        con = sqlite3.connect("coffee.sqlite")

        a = self.lineEdit.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        e = self.lineEdit_5.text()
        f = self.lineEdit_6.text()

        if a != "" and b != "" and c != "" and d != "" and e != "" and f != "":
            if self.command == "add":
                data = (a, b, c, d, e, f,)
                sql = """
                        INSERT INTO coffe
                        (nameVariety, degreeRoasting, groundGrains,
                        descriptionTaste, price, packingVolume) 
                        values(?, ?, ?, ?, ?, ?)
                    """
            else:
                data = (a, b, c, d, e, f, self.name,)
                sql = """
                        UPDATE coffe 
                        SET nameVariety=?, degreeRoasting=?, groundGrains=?, 
                        descriptionTaste=?, price=?, packingVolume=?
                        WHERE nameVariety = ?
                    """

            with con:
                con.execute(sql, data)

            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_3.setText("")


class CoffeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        con = sqlite3.connect("coffee.sqlite")

        with con:
            sql = f"""SELECT * FROM coffe"""
            self.coffes = list(con.execute(sql))

        self.btns = []
        for coffe in self.coffes:
            c_btn = QPushButton(coffe[1])
            c_btn.resize(740, 40)

            self.btns.append(c_btn)

            c_btn.clicked.connect(self.click_coffe)

            self.verticalLayout.addWidget(c_btn)

        self.add_coffe.clicked.connect(self.add_coffee)

    def add_coffee(self):
        command = "add"

        Coffe_add_replace(command, None).exec()

        con = sqlite3.connect("coffee.sqlite")

        with con:
            sql = f"""SELECT * FROM coffe"""
            new_coffes = list(con.execute(sql))

        coffe = set(new_coffes) - set(self.coffes)

        if len(coffe) != 0:
            coffe = coffe.pop()

            c_btn = QPushButton(coffe[1])
            c_btn.resize(740, 40)

            self.btns.append(c_btn)

            c_btn.clicked.connect(self.click_coffe)

            self.verticalLayout.addWidget(c_btn)

            self.coffes = new_coffes

    def click_coffe(self):
        command = "replace"

        name = self.sender().text()

        for coffe in self.coffes:
            if coffe[1] == name:
                CustomDialog(coffe).exec()

                Coffe_add_replace(command, name).exec()

                for c_btn in self.btns:
                    c_btn.hide()

                self.btns = []

                con = sqlite3.connect("coffee.sqlite")

                with con:
                    sql = f"""SELECT * FROM coffe"""
                    self.coffes = list(con.execute(sql))

                for coffe in self.coffes:
                    c_btn = QPushButton(coffe[1])
                    c_btn.resize(740, 40)

                    self.btns.append(c_btn)

                    c_btn.clicked.connect(self.click_coffe)

                    self.verticalLayout.addWidget(c_btn)

                break


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeWindow()
    ex.show()
    sys.exit(app.exec())
