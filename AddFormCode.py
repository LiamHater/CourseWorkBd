import sys
from PySide6.QtCore import QObject, QSize, Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel, QDialog, QPushButton,\
    QFileDialog, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox
from Add_form import Ui_Dialog
import os
from dotenv import dotenv_values
import mysql.connector

config = dotenv_values(".env")

class AddWindow(QDialog):
    GoBack = Signal()
    def __init__(self):
        super(AddWindow, self).__init__()
        self.reference_tables = ["фото_зданий","материал_стен","материал_фундамента",
                                 "назначение_помещения","отделка","район"]

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.current_table_name = ""
        self.photo_path = ""
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        self.config = dotenv_values(".env")
        self.previous_table_data = None
        self.column_names = None
        self.current_photo = ""


    def check_table_content(self):
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        if self.current_table_name == "Фото зданий":
            line_edit = self.ui.tableWidget.cellWidget(0, 0)
            if (self.photo_path != "" or self.current_photo!="") and line_edit.text() != "":
                self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            all_cells_filled = True
            for column in range(self.ui.tableWidget.columnCount()):
                widget = self.ui.tableWidget.cellWidget(0, column)
                if isinstance(widget, QLineEdit) and widget.text() == "":
                    all_cells_filled = False
                    break
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(all_cells_filled)


    def ShowAddForm(self, column_names, table_name):
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Добавить")
        self.current_table_name = table_name
        self.column_names = column_names
        self.ui.tableWidget.setColumnCount(len(column_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        self.ui.tableWidget.setRowCount(1)
        table_data_types = self.getDataType()
        column_data = self.getColumns(self.current_table_name)
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        for column in range(self.ui.tableWidget.columnCount()):
            if table_name == "Фото зданий":
                select_photo_button = QPushButton()
                select_photo_button.setText("Выберите фото")
                select_photo_button.clicked.connect(self.SelectPhoto)
                self.ui.tableWidget.setCellWidget(0, 1, select_photo_button)
            if column_data[column][3] == "MUL":
                referenced_table_name, referenced_column_name = self.get_referenced_table_info(column_data[column][0], cursor)
                primary_key_values = self.load_primary_key_values(referenced_table_name, referenced_column_name, cursor, connection)
                keys_box = QComboBox()
                keys_box.addItems([str(i) for i in primary_key_values])
                keys_box.activated.connect(self.check_table_content)
                self.ui.tableWidget.setCellWidget(0, column, keys_box)
            else:
                line = QLineEdit()
                line.setPlaceholderText(table_data_types[column][0])
                line.textChanged.connect(self.check_table_content)
                self.ui.tableWidget.setCellWidget(0, column, line)
        cursor.close()
        connection.close()
        self.show()

    def ShowUpdateForm(self, column_names, table_data, table_name):
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Изменить")
        self.current_table_name = table_name
        self.column_names = column_names
        self.previous_table_data = table_data
        self.ui.tableWidget.setColumnCount(len(column_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        self.ui.tableWidget.setRowCount(1)
        table_data_types = self.getDataType()
        column_data = self.getColumns(self.current_table_name)
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        for column in range(self.ui.tableWidget.columnCount()):
            if table_name == "Фото зданий":
                select_photo_button = QPushButton()
                select_photo_button.setText("Выберите фото")
                select_photo_button.clicked.connect(self.SelectPhoto)
                self.current_photo = table_data[1]
                self.ui.tableWidget.setCellWidget(0, 1, select_photo_button)
            if column_data[column][3] == "MUL":
                referenced_table_name, referenced_column_name = self.get_referenced_table_info(column_data[column][0],
                                                                                               cursor)
                primary_key_values = self.load_primary_key_values(referenced_table_name, referenced_column_name, cursor,
                                                                  connection)
                keys_box = QComboBox()
                keys_box.addItems([str(i) for i in primary_key_values])
                keys_box.activated.connect(self.check_table_content)
                keys_box.setCurrentText(str(table_data[column]))
                self.ui.tableWidget.setCellWidget(0, column, keys_box)
            else:
                line = QLineEdit()
                line.setPlaceholderText(table_data_types[column][0])
                line.setText(str(table_data[column]))
                line.textChanged.connect(self.check_table_content)
                self.ui.tableWidget.setCellWidget(0, column, line)
        prim_key = self.ui.tableWidget.cellWidget(0,0)
        prim_key.setEnabled(False)
        self.check_table_content()
        cursor.close()
        connection.close()
        self.show()

    def get_referenced_table_info(self, column_name, cursor):
        # Выполняем запрос к метаданным, чтобы получить информацию о внешнем ключе
        query = f"SELECT REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME " \
                f"FROM information_schema.KEY_COLUMN_USAGE " \
                f"WHERE TABLE_NAME = '{self.current_table_name.lower().replace(' ','_')}' " \
                f"AND COLUMN_NAME = '{column_name}'"
        cursor.execute(query)
        result = cursor.fetchone()
        referenced_table_name, referenced_column_name = result
        return referenced_table_name, referenced_column_name

    def load_primary_key_values(self, table_name, column_name, cursor, connection):
        # if table_name in self.reference_tables:
        #     column_name = self.getColumns(table_name)[1][0]
        # Выполняем запрос, чтобы получить значения первичного ключа
        if len(column_name.split()) > 1:
            column_name = f"`{column_name}`"
        query = f"SELECT {column_name} FROM {table_name};"
        print(query)
        cursor.execute(query)
        primary_key_values = [row[0] for row in cursor.fetchall()]
        return primary_key_values

    def LoadPrimValue(self, table_name, value, connection, cursor):
        ref_column_name = self.getColumns(table_name)[1][0]
        table_name = table_name.lower().replace(" ","_")
        prim_column_name = self.getColumns(table_name)[0][0]
        query = f"SELECT `{prim_column_name}` FROM {table_name} WHERE `{ref_column_name}` = '{value}'"
        cursor.execute(query)
        prim_value = cursor.fetchone()[0]
        return prim_value


    def SelectPhoto(self):
        self.photo_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Image Files (*.jpg *.jpeg *.png *.bmp *.gif)')
        if self.photo_path != "":
            self.current_photo = ""
        self.check_table_content()

    def getDataType(self):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        table_name_two_words=self.current_table_name.replace(" ","_")
        data_type_query = f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name_two_words}'"
        cursor.execute(data_type_query)
        table_data_type = cursor.fetchall()
        cursor.close()
        connection.close()
        return table_data_type

    def getColumns(self, table_name):
        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        table_name_two_words = table_name.replace(" ", "_")
        columns_query = f"SHOW COLUMNS FROM {table_name_two_words}"
        cursor.execute(columns_query)
        columns = cursor.fetchall()
        cursor.close()
        connection.close()
        return columns

    def accept(self):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        try:
            # Запрос на вставку данных в таблицу
            if self.ui.buttonBox.button(QDialogButtonBox.Ok).text() == "Добавить":
                self.AddData(connection, cursor)

            # Запрос на изменение данных в таблицу
            else:
                self.UpdateData(connection, cursor)

            connection.commit()
        except Exception as ex:
            print(type(ex))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Несоответствие типов данных или некорректный ввод внешних ключей")
            msg.setWindowTitle("Ошибка")
            msg.exec()
        cursor.close()
        connection.close()
        self.ui.tableWidget.clear()
        self.ui.tableWidget.removeCellWidget(0, 1)
        self.photo_path = ""
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.GoBack.emit()
        self.close()

    def reject(self):
        self.ui.tableWidget.clear()
        self.ui.tableWidget.removeCellWidget(0,1)
        self.photo_path = ""
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.GoBack.emit()
        super(AddWindow, self).reject()

    def UpdateData(self, connection, cursor):
        data = []
        query = ""
        if self.current_table_name == "Фото зданий":
            id_data = self.ui.tableWidget.cellWidget(0, 0).text()
            cadastral_data = self.ui.tableWidget.cellWidget(0, 2).currentText()
            if self.photo_path == "":
                image_data = self.previous_table_data[1]
            else:
                image_data = open(self.photo_path, "rb").read()  # Чтение изображения как бинарных данных

            query = f"UPDATE {self.current_table_name.lower().replace(' ', '_')} " \
                    f"SET `{self.column_names[1]}` = %s, " \
                    f"`{self.column_names[2]}` = %s " \
                    f"WHERE `{self.column_names[0]}` = %s"

            cursor.execute(query, (image_data, cadastral_data, id_data))
        else:
            for column in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.cellWidget(0, column)

                if isinstance(item, QComboBox):
                    data.append(item.currentText())
                else:
                    data.append(item.text())
            values = ", ".join(f"`{self.column_names[i]}` = '{data[i]}'" for i in range(len(data)))
            query = f"UPDATE {self.current_table_name.lower().replace(' ', '_')} SET {values} " \
                    f"WHERE `{self.column_names[0]}` = '{data[0]}'"
            print(query)
            cursor.execute(query)

    def AddData(self, connection, cursor):
        data = []
        query = ""
        if self.current_table_name == "Фото зданий":
            # Получаем данные для вставки из таблицы
            id_data = self.ui.tableWidget.cellWidget(0, 0).text()
            cadastral_data = self.ui.tableWidget.cellWidget(0, 2).currentText()

            # Загрузим фото
            image_data = open(self.photo_path, "rb").read()  # Чтение изображения как бинарных данных

            query = f"INSERT INTO {self.current_table_name.lower().replace(' ', '_')} VALUES (%s, %s, %s)"
            cursor.execute(query, (id_data, image_data, cadastral_data))
        else:
            for column in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.cellWidget(0, column)
                if isinstance(item, QComboBox):
                    data.append(item.currentText())
                else:
                    data.append(item.text())
            values = ", ".join(f"'{value}'" for value in data)
            query = f"INSERT INTO {self.current_table_name.lower().replace(' ','_')} VALUES ({values})"
            cursor.execute(query)


