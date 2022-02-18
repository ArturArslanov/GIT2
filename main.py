import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, \
    QTableWidget, QDialog, QComboBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        con = sqlite3.connect('coffee.sqlite')
        res = con.cursor().execute(F"""SELECT *  FROM coffee""").fetchall()
        headers = ["ид", 'сорт', 'степень обжарки', 'молотый/в зернах',
                   "вкус", 'цена', "объем упаковки"]
        self.tabl.setRowCount(len(res))
        self.tabl.setColumnCount(len(res[0]))
        for i in range(len(res)):
            for j in range(len(res[i])):
                self.tabl.setItem(i, j, QTableWidgetItem(str(res[i][j])))
        self.tabl.setHorizontalHeaderLabels(headers)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
