import socket
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QTextEdit, QTableWidget, QLabel
import threading
import sys
import pickle


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'MainWindow'
        self.left = 500
        self.top = 500
        self.width = 380
        self.height = 510

        self.thread1 = threading.Thread(target=self.connect)
        self.pushButton = QPushButton(self)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_4 = QPushButton(self)
        self.tableWidget = QTableWidget(self)
        self.textTable = QTextEdit(self)
        self.textTableLabel = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #Кнопка выгрузки таблицы
        self.pushButton.setGeometry(160, 340, 201, 41)
        self.pushButton.setText("Выгрузить таблицу из Базы данных")
        self.pushButton.clicked.connect(self.unload)
        #Кнопка добавления записи
        self.pushButton_2.setGeometry(160, 390, 101, 41)
        self.pushButton_2.setText("Добавить запись")
        self.pushButton_2.clicked.connect(self.Add)
        #Кнопка удаления записи
        self.pushButton_3.setGeometry(260, 390, 101, 41)
        self.pushButton_3.setText("Удалить запись")
        self.pushButton_3.clicked.connect(self.Remove)
        #Кнопка загрузки данных
        self.pushButton_4.setGeometry(20, 450, 341, 51)
        self.pushButton_4.setText("Загрузить данные в Базу данных на сервере")
        self.pushButton_4.clicked.connect(self.Upload)
        #Таблица с записями
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 351, 301))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        #строка
        self.textTableLabel.setText("Введите название таблицы:")
        self.textTableLabel.setGeometry(10, 320, 151, 16)
        #cтрока для ввода названий таблиц
        self.textTable.setGeometry(160, 320, 201, 16)
        self.show()

    def connect(self):
        global result
        global cl
        result = []
        cl = socket.socket()
        cl.connect(("192.168.0.103", 12008))
        r = self.textTable.toPlainText()
        cl.send(r.encode('utf-8'))
        while True:
            data = cl.recv(4098)
            if data:
                result = pickle.loads(data)
                break
        if data:
            if (self.tableWidget.columnCount() > 0 ):
                self.tableWidget.clear()
            self.tableWidget.setRowCount(len(result[0]))
            self.tableWidget.setColumnCount(len(result[1]))
            global rows
            rows = len(result[0])
            global column
            column = len(result[1])
            self.tableWidget.clear()
            if result[1]:
                print(result[1])
                self.tableWidget.setHorizontalHeaderLabels(result[1])
            row = 0
            for tup in result[0]:
                col = 0
                for item in tup:
                    cellinfo = QtWidgets.QTableWidgetItem(str(item))
                    self.tableWidget.setItem(row, col, cellinfo)
                    col += 1
                row += 1

    def unload(self):
        self.thread1.start()

    def Add(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

    def Upload(self):
        dataToChange = []
        for row in range(self.tableWidget.rowCount()):
            dataToChange.append([])
            for column in range(self.tableWidget.columnCount()):
                index = self.tableWidget.item(row, column)
                dataToChange[row].append(index.text())
        dataToChange.append(self.textTable.toPlainText())
        dataToChange.append(result[1])
        cl.sendall(pickle.dumps(dataToChange))
        
    def Remove(self):
        indices = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(indices):
            self.tableWidget.removeRow(index.row())

#Запуск нашей формы
if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    a.exec_()

