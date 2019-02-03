# -*- coding: utf-8 -*-
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from controladorProyectos import ControladorProyecto
from gen_nuevoProyecto import Ui_NuevoProyecto

# Se hereda de la clase QMainDialog y la Interfaz
class NuevoProyectoV(QtWidgets.QDialog, Ui_NuevoProyecto):

    # Se define el constructor de la clase
    def __init__(self, *args, **kwargs):
        super(NuevoProyectoV, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.origen = ""
        # Se conectan las señales con los slots
        self.selec_logo.clicked.connect(self.abrirFicheroImg)
        self.btn_addJuntaDir.clicked.connect(self.addJuntaDirect)
        self.btn_elimJuntadir.clicked.connect(self.elimJuntaDirect)
        self.btn_guardarProy.clicked.connect(self.agregarSitioWeb)


    def abrirFicheroImg(self):
        img_ruta = QFileDialog.getOpenFileName(None, "Buscar imagen", '', "Image files (*.jpg *.png)")
        img_aux = str(img_ruta)
        pos = img_aux.find(",")
        self.origen = str(img_aux[2:pos-1])
        img_nombre = os.path.basename(self.origen)
        self.txt_logo.setText(img_nombre)

    def addJuntaDirect(self):
        miembro_jd = self.txt_juntaDir.toPlainText()
        self.listWidget_juntadir.addItem(miembro_jd)

    def elimJuntaDirect(self):
        items = self.listWidget_juntadir.selectedItems()
        for i in items:
            self.listWidget_juntadir.takeItem(self.listWidget_juntadir.row(i))

    def agregarSitioWeb(self):

        #obtener los valores del formulario
        nomP = self.txt_nombProy.toPlainText()
        nomW = self.txt_nomWeb.toPlainText()
        tlf = self.txt_telef.toPlainText()
        email = self.txt_email.toPlainText()
        dir = self.txt_dir.toPlainText()
        logo = self.txt_logo.toPlainText()
        res = self.txt_resumen.toPlainText()
        info = self.txt_sobrenos.toPlainText()
        hist = self.txt_hist.toPlainText()

        items_jd = []
        for index in range(self.listWidget_juntadir.count()):
            items_jd.append(self.listWidget_juntadir.item(index).text())

        if len(nomP) == 0:
            msg = "El nombre del proyecto es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        elif len(nomW) == 0:
            msg = "El nombre del sitio web es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        elif len(email) == 0:
            msg = "El correo electrónico es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        elif len(tlf) == 0:
            msg = "El teléfono es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        else:
            # Validar y llamar al metodo de agregar sitio web para guardarlos
            c = ControladorProyecto()
            mensajesValidacion = c.obtenerMensajesValidacion(nomP, nomW, logo, res, email, tlf, dir, info, hist, items_jd)

            if len(mensajesValidacion) > 0:
                mensaje = ""
                for m in mensajesValidacion:
                    mensaje = mensaje + "\n" + m

                QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)

            else:
                msgerr = c.agregarSitioWeb(nomP, nomW, logo, res, email, tlf, dir, info, hist, items_jd, self.origen)

                if msgerr is None:
                    #Cerrar la ventana al hacer click en guardar
                    ms = "C:\\Users\\NombreUsuario\\WebAsistDesigner\\Workspace"
                    QMessageBox.information(self, "Proyecto", "El proyecto se ha guardado en \n" + ms, QMessageBox.Ok)
                    NuevoProyectoV.close(self)
                else:
                    QMessageBox.critical(self, "Error", msgerr, QMessageBox.Ok)
