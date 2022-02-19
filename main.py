import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTextEdit
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton, \
    QTableWidget, QDialog, QComboBox

from UI.addEditCoffeeForm import Ui_Form
from UI.mainui import myMain

BASE = 'data/coffee.sqlite'


class MyWidget(QMainWindow, myMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.label_4.hide()
        self.uodate_table()
        self.btn.clicked.connect(self.add1)
        self.btn_2.clicked.connect(self.add2)

    def uodate_table(self):
        con = sqlite3.connect(BASE)
        res = con.cursor().execute(F"""SELECT *  FROM coffee""").fetchall()
        headers = ["ид", 'сорт', 'степень обжарки', 'молотый/в зернах',
                   "вкус", 'цена', "объем упаковки"]
        con.close()
        self.tabl.setRowCount(len(res))
        self.tabl.setColumnCount(len(res[0]))
        for i in range(len(res)):
            for j in range(len(res[i])):
                self.tabl.setItem(i, j, QTableWidgetItem(str(res[i][j])))
        self.tabl.setHorizontalHeaderLabels(headers)

    def add1(self):
        dialog = Dialog1()
        self.hide()
        dialog.exec()
        self.show()
        self.uodate_table()

    def add2(self):
        items = self.tabl.selectedItems()
        if not items:
            self.label_4.show()
            return None
        if len(items) > 1:
            self.label_4.setText('выберите один предмет')
            self.label_4.show()
            return None
        row = items[0].row()
        g1 = self.tabl.item(row, 0).text()
        dialog = Dialog1(g1)
        self.hide()
        dialog.exec()
        self.uodate_table()
        self.show()


class Dialog1(QDialog, Ui_Form):
    def __init__(self, change=None):
        super().__init__()
        self.setupUi(self)
        self.lab_8.setText('добавить')
        self.changes = change

        self.initUI()

    def initUI(self):
        if self.changes:
            self.push.setText('изменить')
            con = sqlite3.connect(BASE)
            res = con.cursor().execute(
                F"""SELECT *  FROM coffee where id = {self.changes}""").fetchone()
            con.close()
            g = (self.textEdit, self.textEdit_3, self.textEdit_4,
                 self.textEdit_5, self.textEdit_6, self.textEdit_7)
            for i in range(len(g)):
                g[i].setPlainText(str(res[i + 1]))
            self.push.clicked.connect(self.change)
        else:
            self.push.clicked.connect(self.run)

    def run(self):
        if not all(x for x in (self.textEdit.toPlainText(),
                               self.textEdit_7.toPlainText(),
                               self.textEdit_3.toPlainText(),
                               self.textEdit_4.toPlainText(),
                               self.textEdit_6.toPlainText(),
                               self.textEdit_5.toPlainText())):
            self.lab_8.setText('укажите все данные')
        else:
            con = sqlite3.connect(BASE)
            con.cursor().execute(
                F"""INSERT INTO coffee(name,fried,ground,tasty,coast,V)
                            Values('{self.textEdit.toPlainText()}',
                                    {self.textEdit_3.toPlainText()},
                                    {self.textEdit_4.toPlainText()},
                                    {self.textEdit_5.toPlainText()}
                                    ,{self.textEdit_6.toPlainText()},
                                    {self.textEdit_7.toPlainText()})""")
            con.commit()
            con.close()
            self.close()

    def change(self):
        con = sqlite3.connect(BASE)
        con.cursor().execute(
            F"""UPDATE coffee SET
            name = '{self.textEdit.toPlainText()}',
            fried='{self.textEdit_3.toPlainText()}',
            ground = '{self.textEdit_4.toPlainText()}',
            tasty = '{self.textEdit_5.toPlainText()}',
            coast = '{self.textEdit_6.toPlainText()}',
            V = '{self.textEdit_7.toPlainText()}' WHERE id ={self.changes}""")
        con.commit()
        con.close()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
