# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox

from gen_noticias import Ui_Dialog
from ControladorNoticias import *


class Noticias(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(Noticias, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Obtener las noticias y mostrarlas si existen
        self.controlador = ControladorNoticia()
        self.noticias = self.controlador.mostrarNoticias()
        self.mostrarNoticias()

        #Conectar señales y slots
        self.listWidget_not.itemClicked.connect(self.mostrarNoticia)
        self.btn_editNot.clicked.connect(self.editarNoticia)
        self.btn_cancelEditNot.clicked.connect(self.cancelarEdicion)
        self.btn_guard_not.clicked.connect(self.modificarNoticia)
        self.btn_deleteNot.clicked.connect(self.eliminarNoticia)
        self.dateEdit_not.setMaximumDate(QDate.currentDate())

    def mostrarNoticias(self):

        #Mostrar el id de las noticias existentes en el listWidget
        if len(self.noticias) > 0:
            for n in self.noticias:
                if not n['id_noticia'] is None:  # Si existe el id de la noticia
                    tit = n['titulo']
                    if tit is None:
                        text = n['id_noticia'] + ": "
                    elif len(tit) > 15:
                        text = n['id_noticia'] + ": " + str(tit[0:15]) + "..."
                    else:
                        text = n['id_noticia'] + ": " + tit

                    self.listWidget_not.addItem(text)
        else:
            #Si no existen noticias, deshabilitar los botones de Editar y eliminar
            self.btn_editNot.setEnabled(False)
            self.btn_deleteNot.setEnabled(False)

    def mostrarNoticia(self):
        #Obtener el contenido del listwidget de la noticia seleccionada
        noticia_sleccionada = self.listWidget_not.currentItem().text()
        #Buscar ":" en en texto del list widget
        pos = noticia_sleccionada.find(":")
        #Obtener la subcadena que representa el id de la noticia
        id_noticia_selecc = str(noticia_sleccionada[0:pos])

        #Buscar la noticia en el array de noticias y mostrarla en los campos del formulario
        if len(self.noticias) > 0:
            for n in self.noticias:
                if n['id_noticia'] == id_noticia_selecc:
                    self.txt_titNot.setText(n['titulo'])
                    self.txt_desc_not.setPlainText(n['descripcion'])
                    self.dateEdit_not.setDate(QDate.fromString(n['fecha'], "dd/MM/yyyy"))
                    self.btn_deleteNot.setEnabled(True)
                    self.btn_editNot.setEnabled(True)

    def editarNoticia(self):
        #Deshabilitar el boton "Editar" y "Eliminar"  y habilitar el resto
        self.btn_editNot.setEnabled(False)
        self.txt_titNot.setEnabled(True)
        self.txt_desc_not.setEnabled(True)
        self.dateEdit_not.setEnabled(True)
        self.btn_cancelEditNot.setEnabled(True)
        self.btn_guard_not.setEnabled(True)
        self.btn_deleteNot.setEnabled(False)

    def cancelarEdicion(self):
        #Deshabilitar los botones
        self.btn_editNot.setEnabled(True)
        self.txt_titNot.setEnabled(False)
        self.txt_desc_not.setEnabled(False)
        self.dateEdit_not.setEnabled(False)
        self.btn_cancelEditNot.setEnabled(False)
        self.btn_guard_not.setEnabled(False)

        #Mostrar el contenido de las noticias sin cambios
        self.mostrarNoticia()

    def modificarNoticia(self):
        #Obtener el id de la noticia seleccionada
        noticia_sleccionada = self.listWidget_not.currentItem().text()
        pos = noticia_sleccionada.find(":")
        id_noticia_selecc = str(noticia_sleccionada[0:pos])

        #Obtener los valores de los campos del formulario
        titulo = self.txt_titNot.toPlainText()
        desc = self.txt_desc_not.toPlainText()
        fecha = self.dateEdit_not.text()

        mensajesValidacion = self.controlador.obtenerMensajesValidacion(titulo, desc)
        # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)
        else:
            #Actualizar la noticia con los valores nuevos
            self.controlador.actualizarNoticia(id_noticia_selecc, titulo, desc, fecha)

            #Deshabilitar botones
            self.txt_titNot.setEnabled(False)
            self.txt_desc_not.setEnabled(False)
            self.dateEdit_not.setEnabled(False)
            self.btn_cancelEditNot.setEnabled(False)
            self.btn_guard_not.setEnabled(False)
            self.btn_editNot.setEnabled(True)

            #Actualizar contenido de las noticias
            self.noticias = self.controlador.mostrarNoticias()
            if len(titulo) > 15:
                text = id_noticia_selecc + ": " + str(titulo[0:15]) + "..."
            else:
                text = id_noticia_selecc + ": " + titulo

            self.listWidget_not.takeItem(self.listWidget_not.row(self.listWidget_not.currentItem()))
            self.listWidget_not.addItem(text)

    def eliminarNoticia(self):

        #Obtener el id de la noticia seleccionada
        noticia_sleccionada = self.listWidget_not.currentItem().text()
        pos = noticia_sleccionada.find(":")
        id_noticia_selecc = str(noticia_sleccionada[0:pos])

        #Mostrar mensaje de confirmación de borrado
        mensaje = "¿Está seguro que desea eliminar la noticia?"
        respuesta = QMessageBox.warning(self, "Error", mensaje, QMessageBox.Ok|QMessageBox.Cancel)

        #Si se confirma el borrado, eliminar la noticia y limpiar campos del formulario
        if respuesta == QMessageBox.Ok:
            self.controlador.eliminarNoticia(id_noticia_selecc)
            self.txt_titNot.clear()
            self.txt_desc_not.clear()
            self.listWidget_not.takeItem(self.listWidget_not.row(self.listWidget_not.currentItem()))

            #Deshabilitar botones
            self.btn_deleteNot.setEnabled(False)
            self.btn_editNot.setEnabled(False)