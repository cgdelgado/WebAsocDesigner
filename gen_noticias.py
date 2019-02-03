# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Documentos\UNIVERSIDAD\5to 2016-2017\TFG\Interfaz grafica\noticias.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(742, 487)
        Dialog.setMinimumSize(QtCore.QSize(742, 487))
        Dialog.setMaximumSize(QtCore.QSize(742, 487))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("plantillas/WA.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.btn_deleteNot = QtWidgets.QPushButton(Dialog)
        self.btn_deleteNot.setEnabled(False)
        self.btn_deleteNot.setGeometry(QtCore.QRect(560, 20, 93, 28))
        self.btn_deleteNot.setObjectName("btn_deleteNot")
        self.btn_editNot = QtWidgets.QPushButton(Dialog)
        self.btn_editNot.setEnabled(False)
        self.btn_editNot.setGeometry(QtCore.QRect(290, 20, 93, 28))
        self.btn_editNot.setObjectName("btn_editNot")
        self.listWidget_not = QtWidgets.QListWidget(Dialog)
        self.listWidget_not.setGeometry(QtCore.QRect(10, 10, 261, 451))
        self.listWidget_not.setObjectName("listWidget_not")
        self.btn_cancelEditNot = QtWidgets.QPushButton(Dialog)
        self.btn_cancelEditNot.setEnabled(False)
        self.btn_cancelEditNot.setGeometry(QtCore.QRect(390, 20, 111, 28))
        self.btn_cancelEditNot.setObjectName("btn_cancelEditNot")
        self.txt_desc_not = QtWidgets.QPlainTextEdit(Dialog)
        self.txt_desc_not.setEnabled(False)
        self.txt_desc_not.setGeometry(QtCore.QRect(300, 140, 421, 291))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txt_desc_not.setFont(font)
        self.txt_desc_not.setObjectName("txt_desc_not")
        self.dateEdit_not = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_not.setEnabled(False)
        self.dateEdit_not.setGeometry(QtCore.QRect(450, 440, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dateEdit_not.setFont(font)
        self.dateEdit_not.setObjectName("dateEdit_not")
        self.btn_guard_not = QtWidgets.QPushButton(Dialog)
        self.btn_guard_not.setEnabled(False)
        self.btn_guard_not.setGeometry(QtCore.QRect(650, 440, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_guard_not.setFont(font)
        self.btn_guard_not.setObjectName("btn_guard_not")
        self.txt_titNot = QtWidgets.QTextEdit(Dialog)
        self.txt_titNot.setEnabled(False)
        self.txt_titNot.setGeometry(QtCore.QRect(300, 90, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txt_titNot.setFont(font)
        self.txt_titNot.setObjectName("txt_titNot")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(300, 450, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Noticias"))
        self.btn_deleteNot.setText(_translate("Dialog", "Eliminar"))
        self.btn_editNot.setText(_translate("Dialog", "Editar"))
        self.btn_cancelEditNot.setText(_translate("Dialog", "Cancelar edición"))
        self.txt_desc_not.setPlaceholderText(_translate("Dialog", "Contenido de la noticia"))
        self.btn_guard_not.setText(_translate("Dialog", "Guardar"))
        self.txt_titNot.setPlaceholderText(_translate("Dialog", "Título"))
        self.label_11.setText(_translate("Dialog", "Fecha de publicación: "))

