# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QMessageBox

from gen_imagen import *
from ControladorImagenes import *

class Imagenes(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(Imagenes, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Obtener las imagenes y mostrarlas si existen
        self.controlador = ControladorImagen()
        self.imagenes = self.controlador.mostrarImagenes()
        self.mostrarImagenes()

        # Conectar señales y slots
        self.listWidget_img.itemClicked.connect(self.mostrarImagen)
        self.btn_editImg.clicked.connect(self.editarTituloImagen)
        self.btn_cancelEditImg.clicked.connect(self.cancelarEdicion)
        self.btn_guardImg.clicked.connect(self.modificarTituloImagen)
        self.btn_deleteImg.clicked.connect(self.eliminarImagen)

    def mostrarImagenes(self):
        #Mostrar el id de las imagenes existentes en el listWidget
        if len(self.imagenes) > 0:
            for i in self.imagenes:
                if not i['id_imagen'] is None:  # Si existe el id de la imagen
                    nom = i['img_titulo']
                    if nom is None:
                        text = i['id_imagen'] + ": "
                    elif len(nom) > 10:
                        text = i['id_imagen'] + ": " + str(nom[0:10]) + "..."
                    else:
                        text = i['id_imagen'] + ": " + nom

                    self.listWidget_img.addItem(text)
        else:
            # Si no existen imagenes, deshabilitar los botones de Editar y eliminar
            self.btn_editImg.setEnabled(False)
            self.btn_deleteImg.setEnabled(False)

    def mostrarImagen(self):
        # Obtener el contenido del listwidget de la imagen seleccionada
        imagen_sleccionada = self.listWidget_img.currentItem().text()
        # Buscar ":" en el texto i['id_imagen'] + ": "+ nom para obtener solo el id
        pos = imagen_sleccionada.find(":")
        # Obtener la subcadena que representa el id de la imagen
        id_imagen_slec = str(imagen_sleccionada[0:pos])

        # Buscar la imagen en el array de imagenes y mostrarla en los campos del formulario
        if len(self.imagenes) > 0:
            for i in self.imagenes:
                if i['id_imagen'] == id_imagen_slec:
                    self.txt_titImg.setText(i['img_titulo'])
                    #mostrar la imagen
                    pixmap = QtGui.QPixmap(i['img_url'])
                    pixmap4 = pixmap.scaled(421, 321, QtCore.Qt.KeepAspectRatio)
                    self.lbl_img.setPixmap(QtGui.QPixmap(pixmap4))

                    self.btn_deleteImg.setEnabled(True)
                    self.btn_editImg.setEnabled(True)

    def editarTituloImagen(self):
        #Deshabilitar el boton "Editar" y "Eliminar"  y habilitar el resto
        self.btn_editImg.setEnabled(False)
        self.txt_titImg.setEnabled(True)
        self.btn_cancelEditImg.setEnabled(True)
        self.btn_guardImg.setEnabled(True)
        self.btn_deleteImg.setEnabled(False)

    def cancelarEdicion(self):
        #Deshabilitar los botones
        self.btn_editImg.setEnabled(True)
        self.txt_titImg.setEnabled(False)
        self.btn_cancelEditImg.setEnabled(False)
        self.btn_guardImg.setEnabled(False)

        #Mostrar el contenido de la imagen sin cambios
        self.mostrarImagen()

    def modificarTituloImagen(self):
        # Obtener el id de la imagen seleccionada
        imagen_sleccionada = self.listWidget_img.currentItem().text()
        pos = imagen_sleccionada.find(":")
        id_imagen_selecc = str(imagen_sleccionada[0:pos])

        # Obtener los valores de los campos del formulario
        titulo = self.txt_titImg.toPlainText()

        # Validar titulo
        mensajesValidacion = self.controlador.obtenerMensajesValidacion(titulo)

        # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)
        else:
            # Actualizar el titulo de la imagen
            self.controlador.actualizarTituloImagen(id_imagen_selecc, titulo)

            # Deshabilitar botones
            self.txt_titImg.setEnabled(False)
            self.btn_cancelEditImg.setEnabled(False)
            self.btn_guardImg.setEnabled(False)
            self.btn_editImg.setEnabled(True)

            # Actualizar contenido
            self.imagenes = self.controlador.mostrarImagenes()
            if len(titulo) > 10:
                text = id_imagen_selecc + ": " + str(titulo[0:10]) + "..."
            else:
                text = id_imagen_selecc + ": " + titulo

            self.listWidget_img.takeItem(self.listWidget_img.row(self.listWidget_img.currentItem()))
            self.listWidget_img.addItem(text)

    def eliminarImagen(self):

        #Obtener el id de la imagen sleccionada
        imagen_sleccionada = self.listWidget_img.currentItem().text()
        pos = imagen_sleccionada.find(":")
        id_imagen_selecc = str(imagen_sleccionada[0:pos])

        #Mostrar mensaje de confirmación de borrado
        mensaje = "¿Está seguro que desea eliminar la imagen?"
        respuesta = QMessageBox.warning(self, "Advertencia", mensaje, QMessageBox.Ok|QMessageBox.Cancel)

        #Si se confirma el borrado, eliminar el enlace y limpiar campos del formulario
        if respuesta == QMessageBox.Ok:
            self.controlador.eliminarImagen(id_imagen_selecc)
            self.txt_titImg.clear()
            self.lbl_img.clear()
            self.listWidget_img.takeItem(self.listWidget_img.row(self.listWidget_img.currentItem()))

            #Deshabilitar botones
            self.btn_deleteImg.setEnabled(False)
            self.btn_editImg.setEnabled(False)