# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Documentos\UNIVERSIDAD\5to 2016-2017\TFG\Interfaz grafica\imagenes.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(740, 485)
        Dialog.setMinimumSize(QtCore.QSize(740, 485))
        Dialog.setMaximumSize(QtCore.QSize(740, 485))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("plantillas/WA.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.txt_titImg = QtWidgets.QTextEdit(Dialog)
        self.txt_titImg.setEnabled(False)
        self.txt_titImg.setGeometry(QtCore.QRect(280, 60, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txt_titImg.setFont(font)
        self.txt_titImg.setObjectName("txt_titImg")
        self.btn_guardImg = QtWidgets.QPushButton(Dialog)
        self.btn_guardImg.setEnabled(False)
        self.btn_guardImg.setGeometry(QtCore.QRect(640, 440, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btn_guardImg.setFont(font)
        self.btn_guardImg.setObjectName("btn_guardImg")
        self.btn_editImg = QtWidgets.QPushButton(Dialog)
        self.btn_editImg.setEnabled(False)
        self.btn_editImg.setGeometry(QtCore.QRect(260, 10, 93, 28))
        self.btn_editImg.setObjectName("btn_editImg")
        self.btn_deleteImg = QtWidgets.QPushButton(Dialog)
        self.btn_deleteImg.setEnabled(False)
        self.btn_deleteImg.setGeometry(QtCore.QRect(550, 10, 93, 28))
        self.btn_deleteImg.setObjectName("btn_deleteImg")
        self.btn_cancelEditImg = QtWidgets.QPushButton(Dialog)
        self.btn_cancelEditImg.setEnabled(False)
        self.btn_cancelEditImg.setGeometry(QtCore.QRect(360, 10, 111, 28))
        self.btn_cancelEditImg.setObjectName("btn_cancelEditImg")
        self.listWidget_img = QtWidgets.QListWidget(Dialog)
        self.listWidget_img.setGeometry(QtCore.QRect(10, 10, 231, 461))
        self.listWidget_img.setObjectName("listWidget_img")
        self.lbl_img = QtWidgets.QLabel(Dialog)
        self.lbl_img.setGeometry(QtCore.QRect(280, 110, 421, 321))
        self.lbl_img.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lbl_img.setScaledContents(True)
        self.lbl_img.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_img.setObjectName("lbl_img")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Imágenes"))
        self.txt_titImg.setPlaceholderText(_translate("Dialog", "Título de la imagen"))
        self.btn_guardImg.setText(_translate("Dialog", "Guardar"))
        self.btn_editImg.setText(_translate("Dialog", "Editar"))
        self.btn_deleteImg.setText(_translate("Dialog", "Eliminar"))
        self.btn_cancelEditImg.setText(_translate("Dialog", "Cancelar edición"))
        self.lbl_img.setText(_translate("Dialog", "imagen"))

