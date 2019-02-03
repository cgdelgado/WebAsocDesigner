# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtWidgets import QMessageBox

from gen_actividad import *
from ControladorActividades import *

class Actividades(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(Actividades, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Obtener las actividades y mostrarlas si existen
        self.controlador = ControladorActividad()
        self.actividades = self.controlador.mostrarActividades()
        self.mostrarActividades()

        # Conectar señales y slots
        self.listWidget_act.itemClicked.connect(self.mostrarActividad)
        self.btn_editAct.clicked.connect(self.editarActividad)
        self.btn_cancelEditAct.clicked.connect(self.cancelarEdicion)
        self.btn_guardarAct.clicked.connect(self.modificarActividad)
        self.btn_deleteAct.clicked.connect(self.eliminarActividad)

    def mostrarActividades(self):
        #Mostrar el id de las actividades existentes en el listWidget
        if len(self.actividades) > 0:
            for a in self.actividades:
                if not a['id_actividad'] is None:  # Si existe el id de la actividad
                    nom = a['nombre']
                    if nom is None:
                        text = a['id_enlace'] + ": "
                    elif len(nom) > 10:
                        text = a['id_actividad'] + ": " + str(nom[0:10]) + "..."
                    else:
                        text = a['id_actividad'] + ": " + nom

                    self.listWidget_act.addItem(text)
        else:
            #Si no existen actividades, deshabilitar los botones de Editar y eliminar
            self.btn_editAct.setEnabled(False)
            self.btn_deleteAct.setEnabled(False)

    def mostrarActividad(self):
        # Obtener el contenido del listwidget de la actividad seleccionada
        actividad_sleccionada = self.listWidget_act.currentItem().text()
        # Buscar ":" en en texto a['id_actividad'] + ": "+ a['nombre'] para obtener solo el id
        pos = actividad_sleccionada.find(":")
        # Obtener la subcadena que representa el id de la actividad
        id_actividad_selecc = str(actividad_sleccionada[0:pos])

        # Buscar la actividad en el array de actividades y mostrarlo en los campos del formulario
        if len(self.actividades) > 0:
            for a in self.actividades:
                if a['id_actividad'] == id_actividad_selecc:
                    self.txt_nombAct.setText(a['nombre'])
                    self.txt_descAct.setPlainText(a['descripcion'])
                    self.fecha_act.setDate(QDate.fromString(a['fecha'], "dd/MM/yyyy"))
                    self.hora_acr.setTime(QTime.fromString(a['hora'], "hh:mm"))
                    self.txt_lugarAct.setText(a['lugar'])
                    self.btn_deleteAct.setEnabled(True)
                    self.btn_editAct.setEnabled(True)

    def editarActividad(self):
        #Deshabilitar el boton "Editar" y "Eliminar"  y habilitar el resto
        self.btn_editAct.setEnabled(False)
        self.txt_nombAct.setEnabled(True)
        self.txt_descAct.setEnabled(True)
        self.fecha_act.setEnabled(True)
        self.hora_acr.setEnabled(True)
        self.txt_lugarAct.setEnabled(True)
        self.btn_cancelEditAct.setEnabled(True)
        self.btn_guardarAct.setEnabled(True)
        self.btn_deleteAct.setEnabled(False)

    def cancelarEdicion(self):
        #Deshabilitar los botones
        self.btn_editAct.setEnabled(True)
        self.txt_nombAct.setEnabled(False)
        self.txt_descAct.setEnabled(False)
        self.fecha_act.setEnabled(False)
        self.hora_acr.setEnabled(False)
        self.txt_lugarAct.setEnabled(False)
        self.btn_cancelEditAct.setEnabled(False)
        self.btn_guardarAct.setEnabled(False)

        #Mostrar el contenido de las actividades sin cambios
        self.mostrarActividad()

    def modificarActividad(self):
        #Obtener el id de la actividad seleccionada
        actividad_sleccionada = self.listWidget_act.currentItem().text()
        pos = actividad_sleccionada.find(":")
        id_actividad_selecc = str(actividad_sleccionada[0:pos])

        #Obtener los valores de los campos del formulario
        nombre = self.txt_nombAct.toPlainText()
        desc = self.txt_descAct.toPlainText()
        fecha = self.fecha_act.text()
        hora = self.hora_acr.text()
        lugar = self.txt_lugarAct.toPlainText()

        # Validar datos
        mensajesValidacion = self.controlador.obtenerMensajesValidacion(nombre, desc, lugar)

        # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)
        else:

            #Actualizar la actividad con los valores nuevos
            self.controlador.actualizarActividad(id_actividad_selecc, nombre, desc, fecha, hora, lugar)

            #Deshabilitar botones
            self.txt_nombAct.setEnabled(False)
            self.txt_descAct.setEnabled(False)
            self.fecha_act.setEnabled(False)
            self.hora_acr.setEnabled(False)
            self.txt_lugarAct.setEnabled(False)
            self.btn_cancelEditAct.setEnabled(False)
            self.btn_guardarAct.setEnabled(False)
            self.btn_editAct.setEnabled(True)

            #Actualizar contenido de las actividades
            self.actividades = self.controlador.mostrarActividades()
            if len(nombre) > 10:
                text = id_actividad_selecc + ": " + str(nombre[0:10]) + "..."
            else:
                text = id_actividad_selecc + ": " + nombre

            self.listWidget_act.takeItem(self.listWidget_act.row(self.listWidget_act.currentItem()))
            self.listWidget_act.addItem(text)


    def eliminarActividad(self):
        #Obtener el id de la actividad sleccionada
        actividad_sleccionada = self.listWidget_act.currentItem().text()
        pos = actividad_sleccionada.find(":")
        id_actividad_selecc = str(actividad_sleccionada[0:pos])

        #Mostrar mensaje de confirmación de borrado
        mensaje = "¿Está seguro que desea eliminar la actividad?"
        respuesta = QMessageBox.warning(self, "Advertencia", mensaje, QMessageBox.Ok|QMessageBox.Cancel)

        #Si se confirma el borrado, eliminar la actividad y limpiar campos del formulario
        if respuesta == QMessageBox.Ok:
            self.controlador.eliminarActividad(id_actividad_selecc)
            self.txt_nombAct.clear()
            self.txt_descAct.clear()
            self.txt_lugarAct.clear()
            self.listWidget_act.takeItem(self.listWidget_act.row(self.listWidget_act.currentItem()))

            #Deshabilitar botones
            self.btn_deleteAct.setEnabled(False)
            self.btn_editAct.setEnabled(False)