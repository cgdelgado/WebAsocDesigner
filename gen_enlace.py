# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Documentos\UNIVERSIDAD\5to 2016-2017\TFG\Interfaz grafica\enlaces.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(729, 443)
        dialog.setMinimumSize(QtCore.QSize(729, 443))
        dialog.setMaximumSize(QtCore.QSize(729, 443))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("plantillas/WA.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
        self.txt_tit_enl = QtWidgets.QTextEdit(dialog)
        self.txt_tit_enl.setEnabled(False)
        self.txt_tit_enl.setGeometry(QtCore.QRect(260, 110, 451, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txt_tit_enl.setFont(font)
        self.txt_tit_enl.setObjectName("txt_tit_enl")
        self.btn_guardEnlace = QtWidgets.QPushButton(dialog)
        self.btn_guardEnlace.setEnabled(False)
        self.btn_guardEnlace.setGeometry(QtCore.QRect(650, 230, 61, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_guardEnlace.setFont(font)
        self.btn_guardEnlace.setObjectName("btn_guardEnlace")
        self.txt_url_enl = QtWidgets.QTextEdit(dialog)
        self.txt_url_enl.setEnabled(False)
        self.txt_url_enl.setGeometry(QtCore.QRect(260, 180, 451, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txt_url_enl.setFont(font)
        self.txt_url_enl.setObjectName("txt_url_enl")
        self.btn_editEnl = QtWidgets.QPushButton(dialog)
        self.btn_editEnl.setEnabled(False)
        self.btn_editEnl.setGeometry(QtCore.QRect(260, 20, 93, 28))
        self.btn_editEnl.setObjectName("btn_editEnl")
        self.listWidget_enl = QtWidgets.QListWidget(dialog)
        self.listWidget_enl.setGeometry(QtCore.QRect(10, 10, 231, 421))
        self.listWidget_enl.setObjectName("listWidget_enl")
        self.btn_deleteEnl = QtWidgets.QPushButton(dialog)
        self.btn_deleteEnl.setEnabled(False)
        self.btn_deleteEnl.setGeometry(QtCore.QRect(630, 410, 93, 28))
        self.btn_deleteEnl.setObjectName("btn_deleteEnl")
        self.btn_cancelEditEnl = QtWidgets.QPushButton(dialog)
        self.btn_cancelEditEnl.setEnabled(False)
        self.btn_cancelEditEnl.setGeometry(QtCore.QRect(360, 20, 111, 28))
        self.btn_cancelEditEnl.setObjectName("btn_cancelEditEnl")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Enlaces"))
        self.txt_tit_enl.setPlaceholderText(_translate("dialog", "Texto"))
        self.btn_guardEnlace.setText(_translate("dialog", "Guardar"))
        self.txt_url_enl.setPlaceholderText(_translate("dialog", "URL"))
        self.btn_editEnl.setText(_translate("dialog", "Editar"))
        self.btn_deleteEnl.setText(_translate("dialog", "Eliminar"))
        self.btn_cancelEditEnl.setText(_translate("dialog", "Cancelar edición"))

