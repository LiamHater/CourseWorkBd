import sys
from PySide6.QtCore import QObject, QSize, Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView, \
    QLabel, QDialog, QPushButton, QFileDialog, QDialogButtonBox, QMessageBox
from BD import Ui_MainWindow
from AddFormCode import AddWindow
import os
from dotenv import dotenv_values
import mysql.connector


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.comboBox.activated.connect(self.showTableData)
        self.ui.comboBox.activated.connect(self.ui.lineEdit.clear)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.config = dotenv_values(".env")
        self.add_form_window = AddWindow()
        self.add_form_window.GoBack.connect(self.showMainForm)
        self.ui.pushButton.pressed.connect(self.showAddWindow)
        self.ui.tableWidget.itemSelectionChanged.connect(self.check_delete_button)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_2.clicked.connect(self.delete_data)
        self.ui.pushButton_3.clicked.connect(self.ShowUpdateWindow)
        self.search_data = 0
        self.ui.pushButton_4.clicked.connect(self.SearchData)
        self.old_edit_name = ""
        self.ui.pushButton_5.clicked.connect(self.ui.lineEdit.clear)
        self.ui.pushButton_5.clicked.connect(self.RemoveSearchData)

    def RemoveSearchData(self):
        self.search_data = 0
        self.showTableData()

    def SearchData(self):
        self.search_data = 1
        self.showTableData()

    def fill_combo_box(self):
        self.ui.comboBox.addItem("Фото зданий")
        self.ui.comboBox.addItem("Материал стен")
        self.ui.comboBox.addItem("Материал фундамента")
        self.ui.comboBox.addItem("Назначение помещения")
        self.ui.comboBox.addItem("Отделка")
        self.ui.comboBox.addItem("Район")

    def getData(self, comboBoxText):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()

        comboBoxText = comboBoxText.lower().replace(" ","_")

        # Запрос на получение названия колонок
        name_query = f'SHOW COLUMNS FROM {comboBoxText}'
        cursor.execute(name_query)
        column_names = [i[0] for i in cursor.fetchall()]  # Массив, где хранятся имена ()
        data_query = ""

        # Запрос на получение данных таблицы при наличии условия отбора
        if self.search_data == 1:
            data_query = f"SELECT * FROM {comboBoxText} " \
                         f"WHERE `{self.ui.comboBox_2.currentText()}` " \
                         f"{self.ui.comboBox_3.currentText()} '{self.ui.lineEdit.text()}'"
            print(data_query)
            self.old_edit_name = self.ui.comboBox_2.currentText()

        # Запрос на получение данных таблицы
        else:
            data_query = f'SELECT * FROM {comboBoxText}'
        cursor.execute(data_query)
        table_data = cursor.fetchall()#Массив данных
        cursor.close()
        connection.close()
        return column_names, table_data

    def showTableData(self):

        self.ui.pushButton_2.setEnabled(False)
        self.ui.tableWidget.clear()
        # Получаем название таблицы и её данные
        column_names, table_data = self.getData(self.ui.comboBox.currentText())

        #Настраиваем таблицу (Название колонок и размер)
        self.ui.tableWidget.setColumnCount(len(column_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(column_names)
        if self.search_data == 1:
            self.ui.comboBox_2.setCurrentText(self.old_edit_name)
        self.ui.tableWidget.setRowCount(len(table_data))

        #Заполняем данными
        if self.ui.comboBox.currentText() == "Фото зданий":
            self.ui.comboBox_2.removeItem(1)
            for row, (id, photo_data, cadastral_number_id) in enumerate(table_data):
                id_item = QTableWidgetItem(str(id))
                self.ui.tableWidget.setItem(row, 0, id_item)

                #Создаем виджет для хранения нашего изображения
                label = QLabel()
                pix = QPixmap()
                pix.loadFromData(photo_data)
                _size = QSize(200, 100)
                label.setPixmap(pix.scaled(_size, Qt.KeepAspectRatio))

                # Вставляем его в таблицу
                self.ui.tableWidget.setCellWidget(row, 1, label)
                cadastral_number_id_item = QTableWidgetItem(str(cadastral_number_id))
                self.ui.tableWidget.setItem(row, 2, cadastral_number_id_item)

            # Установка размеров ячеек для изображений
            self.ui.tableWidget.setColumnWidth(1, 500)
            self.ui.tableWidget.verticalHeader().setDefaultSectionSize(150)

        else:
            for row, rowData in enumerate(table_data):
                for col, value in enumerate(rowData):
                    item = QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(row, col, item)
                    self.ui.tableWidget.setRowHeight(row, 50)

        self.search_data = 0

    def showAddWindow(self):
        column_names, table_data = self.getData(self.ui.comboBox.currentText())
        self.add_form_window.ShowAddForm(column_names, self.ui.comboBox.currentText())
        self.close()

    def ShowUpdateWindow(self):
        column_names, table_data = self.getData(self.ui.comboBox.currentText())
        self.add_form_window.ShowUpdateForm(column_names, table_data[self.ui.tableWidget.currentRow()], self.ui.comboBox.currentText())
        self.close()

    def showMainForm(self):
        self.showTableData()
        self.show()

    def check_delete_button(self):
        # Проверка что все выбранные элементы находятся в одной строке
        if self.check_selected_elements_in_one_row():
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)

    def check_selected_elements_in_one_row(self):
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        selected_items = self.ui.tableWidget.selectedItems()
        if len(selected_items) > 0:

            # Получаем номер строки первого выбранного элемента
            row = selected_items[0].row()

            # Проверяем, находятся ли все выбранные элементы в этой же строке
            for item in selected_items:
                if item.row() != row:
                    return False

            if len(selected_items) == self.ui.tableWidget.columnCount() or \
                    (len(selected_items) == self.ui.tableWidget.columnCount()-1 and self.ui.comboBox.currentText() == "Фото зданий"):
                return True
        else:
            return False

    def delete_data(self):
        column_names, _ = self.getData(self.ui.comboBox.currentText())

        # Корректировка названия таблицы, если оно состоит из более 1 слова
        if len(column_names[0].split()) > 1:
            delete_column = f"`{column_names[0]}`"
        else:
            delete_column = column_names[0]

        # Запрос на удаление записи
        delete_row_query = f"DELETE FROM {self.ui.comboBox.currentText().lower().replace(' ', '_')}" \
                           f" WHERE {delete_column}=" \
                           f"{int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())}"
        confirm_delete = QMessageBox.question(self, "Подтверждение удаления",
                                              "Вы уверены, что хотите удалить данные?",
                                              QMessageBox.Yes | QMessageBox.No)
        if confirm_delete == QMessageBox.Yes:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor()
            cursor.execute(delete_row_query)
            connection.commit()
            cursor.close()
            connection.close()
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.showTableData()
