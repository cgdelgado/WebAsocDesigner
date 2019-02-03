# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QMessageBox

from gen_enlace import *
from ControladorEnlaces import *

class Enlaces(QtWidgets.QDialog, Ui_dialog):

    def __init__(self, *args, **kwargs):
        super(Enlaces, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Obtener los enlaces y mostrarlos si existen
        self.controlador = ControladorEnlace()
        self.enlaces = self.controlador.mostrarEnlaces()
        self.mostrarEnlaces()

        # Conectar señales y slots
        self.listWidget_enl.itemClicked.connect(self.mostrarEnlace)
        self.btn_editEnl.clicked.connect(self.editarEnlace)
        self.btn_cancelEditEnl.clicked.connect(self.cancelarEdicion)
        self.btn_guardEnlace.clicked.connect(self.modificarEnlace)
        self.btn_deleteEnl.clicked.connect(self.eliminarEnlace)

    def mostrarEnlaces(self):
        #Mostrar el id de los enlaces existentes en el listWidget
        if len(self.enlaces) > 0:
            for e in self.enlaces:
                if not e['id_enlace'] is None:  # Si existe el id del enlace
                    nom = e['nombre']
                    if nom is None:
                        text = e['id_enlace'] + ": "
                    elif len(nom) > 10:
                        text = e['id_enlace'] + ": " + str(nom[0:10]) + "..."
                    else:
                        text = e['id_enlace'] + ": " + nom

                    self.listWidget_enl.addItem(text)
        else:
            #Si no existen enlaces, deshabilitar los botones de Editar y eliminar
            self.btn_editEnl.setEnabled(False)
            self.btn_deleteEnl.setEnabled(False)

    def mostrarEnlace(self):
        # Obtener el contenido del listwidget del enlace seleccionado
        enlace_sleccionado = self.listWidget_enl.currentItem().text()
        # Buscar ":" en en texto a['id_enlace'] + ": "+ a['nombre'] para obtener solo el id
        pos = enlace_sleccionado.find(":")
        # Obtener la subcadena que representa el id del enlace
        id_enlace_slec = str(enlace_sleccionado[0:pos])

        # Buscar el enlace en el array de enlaces y mostrarlo en los campos del formulario
        if len(self.enlaces) > 0:
            for e in self.enlaces:
                if e['id_enlace'] == id_enlace_slec:
                    self.txt_tit_enl.setText(e['nombre'])
                    self.txt_url_enl.setPlainText(e['url'])

                    self.btn_deleteEnl.setEnabled(True)
                    self.btn_editEnl.setEnabled(True)

    def editarEnlace(self):
        #Deshabilitar el boton "Editar" y "Eliminar"  y habilitar el resto
        self.btn_editEnl.setEnabled(False)
        self.txt_url_enl.setEnabled(True)
        self.btn_cancelEditEnl.setEnabled(True)
        self.btn_guardEnlace.setEnabled(True)
        self.btn_deleteEnl.setEnabled(False)
        self.txt_tit_enl.setEnabled(True)

        # Obtener el id del enlace seleccionado para deshabiliar el campo titulo si  es de redes sociales
        enlace_sleccionado = self.listWidget_enl.currentItem().text()
        pos = enlace_sleccionado.find(":")
        id_enlace_selecc = str(enlace_sleccionado[0:pos])
        for e in self.enlaces:
                if id_enlace_selecc == e['id_enlace']:
                    if (e['nombre'] == 'Facebook') or (e['nombre'] == 'Twitter') or (e['nombre'] == 'Youtube') or (e['nombre'] == 'Pinterest'):
                        self.txt_tit_enl.setEnabled(False)

    def cancelarEdicion(self):
        #Deshabilitar los botones
        self.btn_editEnl.setEnabled(True)
        self.txt_tit_enl.setEnabled(False)
        self.txt_url_enl.setEnabled(False)
        self.btn_cancelEditEnl.setEnabled(False)
        self.btn_guardEnlace.setEnabled(False)

        #Mostrar el contenido del enlace sin cambios
        self.mostrarEnlace()

    def modificarEnlace(self):
        #Obtener el id del enlace sleccionado
        enlace_sleccionado = self.listWidget_enl.currentItem().text()
        pos = enlace_sleccionado.find(":")
        id_enlace_selecc = str(enlace_sleccionado[0:pos])

        #Obtener los valores de los campos del formulario
        nombre = self.txt_tit_enl.toPlainText()
        url = self.txt_url_enl.toPlainText()

        # Validar y pasar datos al controlador
        mensajesValidacion = self.controlador.obtenerMensajesValidacion(nombre, url)

        # Si existen errore de validacion, se muestran, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error de validación", mensaje, QMessageBox.Ok)
        else:

            # Actualizar el enlace con los valores nuevos
            self.controlador.actualizarEnlace(id_enlace_selecc, nombre, url)

            # Deshabilitar botones
            self.txt_tit_enl.setEnabled(False)
            self.txt_url_enl.setEnabled(False)
            self.btn_cancelEditEnl.setEnabled(False)
            self.btn_guardEnlace.setEnabled(False)
            self.btn_editEnl.setEnabled(True)

            # Actualizar contenido de los enlaces
            self.enlaces = self.controlador.mostrarEnlaces()
            if len(nombre) > 10:
                text = id_enlace_selecc + ": " + str(nombre[0:10]) + "..."
            else:
                text = id_enlace_selecc + ": " + nombre

            self.listWidget_enl.takeItem(self.listWidget_enl.row(self.listWidget_enl.currentItem()))
            self.listWidget_enl.addItem(text)

    def eliminarEnlace(self):
        # Obtener el id del enlace sleccionado
        enlace_sleccionado = self.listWidget_enl.currentItem().text()
        pos = enlace_sleccionado.find(":")
        id_enlace_selecc = str(enlace_sleccionado[0:pos])

        # Mostrar mensaje de confirmación de borrado
        mensaje = "¿Está seguro que desea eliminar el enlace?"
        respuesta = QMessageBox.warning(self, "Advertencia", mensaje, QMessageBox.Ok|QMessageBox.Cancel)

        #Si se confirma el borrado, eliminar el enlace y limpiar campos del formulario
        if respuesta == QMessageBox.Ok:
            self.controlador.eliminarEnlace(id_enlace_selecc)
            self.txt_tit_enl.clear()
            self.txt_url_enl.clear()
            self.listWidget_enl.takeItem(self.listWidget_enl.row(self.listWidget_enl.currentItem()))

            #Deshabilitar botones
            self.btn_deleteEnl.setEnabled(False)
            self.btn_editEnl.setEnabled(False)