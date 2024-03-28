# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BD.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(908, 554)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(170, 40, 721, 461))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 40, 141, 22))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(10, 80, 141, 31))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(10, 120, 141, 31))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(10, 160, 141, 31))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(20, 320, 101, 21))
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(20, 360, 131, 22))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 430, 131, 21))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 280, 101, 31))
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(20, 460, 121, 31))
        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(20, 400, 131, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 908, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u0417\u0434\u0430\u043d\u0438\u0435", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0430", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u0435\u0449\u0435\u043d\u0438\u0435", None))

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0439\u0442\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0431\u043e\u0440 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441 \u043e\u0442\u0431\u043e\u0440\u0430", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("MainWindow", u"=", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("MainWindow", u">", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("MainWindow", u">=", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("MainWindow", u"<", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("MainWindow", u"<=", None))
        self.comboBox_3.setItemText(5, QCoreApplication.translate("MainWindow", u"<>", None))

    # retranslateUi

