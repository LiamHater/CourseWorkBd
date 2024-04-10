import sys
from PySide6.QtCore import QObject, QSize, Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel, QDialog, QPushButton,\
    QFileDialog, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox
from Add_form import Ui_Dialog
from sqlalchemy import create_engine, MetaData, Table, select, insert, update
from sqlalchemy.orm import sessionmaker
import os
from dotenv import dotenv_values
import mysql.connector

from dotenv import dotenv_values, load_dotenv

config = dotenv_values(".env")
load_dotenv(".env")

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

        self.db_user = os.getenv("user")
        self.db_password = os.getenv("password")
        self.db_hostname = os.getenv("host")
        self.db_name = os.getenv("database")
        self.engine = create_engine(f'mysql+mysqlconnector://{self.db_user}:{self.db_password}'
                                    f'@{self.db_hostname}/{self.db_name}')
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(self.engine)
        self.table = None



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
        self.table = Table(table_name.lower().replace(" ","_"), self.metadata, autoload=True, autoload_with=self.engine)
        print(self.table.columns)
        table_data_types = self.table.columns

        for column in range(self.ui.tableWidget.columnCount()):
            if table_name == "Фото зданий":
                select_photo_button = QPushButton()
                select_photo_button.setText("Выберите фото")
                select_photo_button.clicked.connect(self.SelectPhoto)
                self.ui.tableWidget.setCellWidget(0, 1, select_photo_button)
            foreign_keys = self.table.columns[column].foreign_keys

            if foreign_keys:
                for fk in foreign_keys:
                    # Получаем имя таблицы, на которую ссылается внешний ключ
                    parent_table_name = fk.column.table.name

                    # Получаем имя столбца, на который ссылается внешний ключ
                    parent_column_name = fk.column.name

                    # Получаем данные из таблицы, на которую ссылается внешний ключ
                    parent_table = Table(parent_table_name, self.metadata, autoload=True, autoload_with=self.engine)
                    conn = self.engine.connect()
                    stmt = select(parent_table.c[parent_column_name])
                    result = conn.execute(stmt)

                    # Создаем QComboBox и добавляем значения из связанной таблицы
                    keys_box = QComboBox()
                    keys_box.addItems([str(row[0]) for row in result])

                    # Подключаем слот для обработки изменения значения в QComboBox
                    keys_box.activated.connect(self.check_table_content)

                    # Устанавливаем QComboBox в ячейку таблицы
                    self.ui.tableWidget.setCellWidget(0, column, keys_box)

            else:
                line = QLineEdit()
                line.setPlaceholderText(str(table_data_types[column].type))
                line.textChanged.connect(self.check_table_content)
                self.ui.tableWidget.setCellWidget(0, column, line)
        self.show()

    def ShowUpdateForm(self, column_names, table_data, table_name):
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Изменить")
        self.current_table_name = table_name
        self.column_names = column_names
        self.previous_table_data = table_data
        self.ui.tableWidget.setColumnCount(len(column_names))
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        self.ui.tableWidget.setRowCount(1)
        self.table = Table(table_name.lower().replace(" ", "_"), self.metadata, autoload=True,
                           autoload_with=self.engine)
        print(self.table.columns)
        table_data_types = self.table.columns
        for column in range(self.ui.tableWidget.columnCount()):
            if table_name == "Фото зданий":
                select_photo_button = QPushButton()
                select_photo_button.setText("Выберите фото")
                select_photo_button.clicked.connect(self.SelectPhoto)
                self.current_photo = table_data[1]
                self.ui.tableWidget.setCellWidget(0, 1, select_photo_button)
            foreign_keys = self.table.columns[column].foreign_keys

            if foreign_keys:
                for fk in foreign_keys:
                    # Получаем имя таблицы, на которую ссылается внешний ключ
                    parent_table_name = fk.column.table.name

                    # Получаем имя столбца, на который ссылается внешний ключ
                    parent_column_name = fk.column.name

                    # Получаем данные из таблицы, на которую ссылается внешний ключ
                    parent_table = Table(parent_table_name, self.metadata, autoload=True, autoload_with=self.engine)
                    conn = self.engine.connect()
                    stmt = select(parent_table.c[parent_column_name])
                    result = conn.execute(stmt)

                    # Создаем QComboBox и добавляем значения из связанной таблицы
                    keys_box = QComboBox()
                    keys_box.addItems([str(row[0]) for row in result])

                    # Подключаем слот для обработки изменения значения в QComboBox
                    keys_box.activated.connect(self.check_table_content)

                    keys_box.setCurrentText(str(table_data[column]))

                    # Устанавливаем QComboBox в ячейку таблицы
                    self.ui.tableWidget.setCellWidget(0, column, keys_box)

            else:
                line = QLineEdit()
                line.setPlaceholderText(str(table_data_types[column].type))
                line.textChanged.connect(self.check_table_content)
                line.setText(str(table_data[column]))
                self.ui.tableWidget.setCellWidget(0, column, line)

        prim_key = self.ui.tableWidget.cellWidget(0, 0)
        prim_key.setEnabled(False)
        self.check_table_content()
        self.show()

    def SelectPhoto(self):
        self.photo_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File', './',
            'Image Files (*.jpg *.jpeg *.png *.bmp *.gif)')
        if self.photo_path != "":
            self.current_photo = ""
        self.check_table_content()

    def accept(self):

        try:
            # Запрос на вставку данных в таблицу
            if self.ui.buttonBox.button(QDialogButtonBox.Ok).text() == "Добавить":
                self.AddData()

            # Запрос на изменение данных в таблицу
            else:
                self.UpdateData()

        except Exception as ex:
            print(ex)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Несоответствие типов данных или некорректный ввод внешних ключей")
            msg.setWindowTitle("Ошибка")
            msg.exec()

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

    def UpdateData(self):
        data = []
        # Создаем запрос на вставку данных
        update_statement = update(self.table)

        # Создаем список для хранения значений
        values = {}
        query = ""
        if self.current_table_name == "Фото зданий":
            id_data = self.ui.tableWidget.cellWidget(0, 0).text()
            cadastral_data = self.ui.tableWidget.cellWidget(0, 2).currentText()
            if self.photo_path == "":
                image_data = self.previous_table_data[1]
            else:
                image_data = open(self.photo_path, "rb").read()  # Чтение изображения как бинарных данных

            update_statement = update(self.table).values([id_data, image_data, cadastral_data]).\
                where(self.table.c[self.column_names[0]] == id_data)

        else:
            for column in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.cellWidget(0, column)

                if isinstance(item, QComboBox):
                    data.append(item.currentText())
                else:
                    data.append(item.text())
            update_statement = update(self.table).values(data). \
                where(self.table.c[self.column_names[0]] == data[0])

        print(update_statement)
        with self.engine.connect() as conn:
            result = conn.execute(update_statement)
            conn.commit()

    def AddData(self):
        data = []
        # Создаем запрос на вставку данных
        insert_statement = insert(self.table)

        # Создаем список для хранения значений
        values = {}
        if self.current_table_name == "Фото зданий":
            # Получаем данные для вставки из таблицы
            id_data = self.ui.tableWidget.cellWidget(0, 0).text()
            cadastral_data = self.ui.tableWidget.cellWidget(0, 2).currentText()

            # Загрузим фото
            image_data = open(self.photo_path, "rb").read()  # Чтение изображения как бинарных данных

            insert_statement = insert(self.table).values([id_data, image_data, cadastral_data])

        else:
            for column in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.cellWidget(0, column)
                if isinstance(item, QComboBox):
                    data.append(item.currentText())
                else:
                    data.append(item.text())
            insert_statement = insert(self.table).values(data)

        print(insert_statement)
        with self.engine.connect() as conn:
            result = conn.execute(insert_statement)
            conn.commit()



