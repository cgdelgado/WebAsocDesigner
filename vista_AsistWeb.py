# -*- coding: utf-8 -*-
import sys

import os
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from gen_AsistWeb import Ui_MainWindow
from vista_NuevoProyecto import NuevoProyectoV
from vista_noticias import Noticias
from vista_actividades import Actividades
from vista_enlaces import Enlaces
from vista_imagenes import Imagenes
from vista_estilos import Estilo
from controladorProyectos import ControladorProyecto
from ControladorPlantillas import ControladorPlantilla
from ControladorNoticias import ControladorNoticia
from ControladorActividades import ControladorActividad
from ControladorEnlaces import ControladorEnlace
from ControladorImagenes import ControladorImagen

# Se hereda de la clase QMainWindow y de la clase Ui_MainWindow con la interfaz grafica
class AsistenteWeb(QtWidgets.QMainWindow, Ui_MainWindow):

    # Se define el constructor de la clase
    def __init__(self, *args, **kwargs):
        super(AsistenteWeb, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.origen = ""  # Ruta origen de las imagenes seleccionadas

        # Se conectan las señales con los slots
        self.actionNuevo_proyecto.triggered.connect(self.crearProyecto)
        self.actionAbrir_proyecto.triggered.connect(self.abrirProyecto)
        self.btn_editWeb.clicked.connect(self.editarSitioWeb)
        self.btn_cancelEdit.clicked.connect(self.cancelarEdicion)
        self.btn_selec_logo.clicked.connect(self.abrirFicheroImg)
        self.btn_guardWeb.clicked.connect(self.actualizarSitioWeb)
        self.btn_agregarJuntDir.clicked.connect(self.addJuntaDirect)
        self.btn_elimJuntDir.clicked.connect(self.elimJuntaDirect)
        self.actionCerrar_proyecto.triggered.connect(self.cerrarProyecto)
        self.btn_guardarPlant.clicked.connect(self.guardarPlantilla)
        self.btn_mostrarPlant.clicked.connect(self.mostrarPlantilla)
        self.btn_editEstilo.clicked.connect(self.editarEstilo)
        self.btn_prev.clicked.connect(self.previsualizar)
        self.actionPrevisualizar_sitio_web.triggered.connect(self.previsualizar)
        self.btnPublicar.clicked.connect(self.publicar)
        self.actionManual_de_usuario.triggered.connect(self.consultarManual)

        pixmaplogo = QtGui.QPixmap('plantillas\\logo.png')
        pixmapscaled = pixmaplogo.scaled(481, 441, QtCore.Qt.KeepAspectRatio)
        self.lbl_logoimg.setPixmap(QtGui.QPixmap(pixmapscaled))

        # Modulo de contenidos: NOTICIAS
        self.btn_addNoticia.clicked.connect(self.agregarNoticia)
        self.btn_verNotic.clicked.connect(self.verNoticias)
        self.btn_elimTodasNotic.clicked.connect(self.eliminarTodasLasNoticias)
        self.dateEdit_noticia.setMaximumDate(QDate.currentDate())
        self.dateEdit_noticia.setDate(QDate.currentDate())

        # Modulo de contenidos: ACTIVIDADES
        self.btn_addAct.clicked.connect(self.agregarActividad)
        self.btn_verAct.clicked.connect(self.verActividades)
        self.btn_elimTodasAct.clicked.connect(self.eliminarTodasLasActividades)
        self.dateEdit_actividad.setMinimumDate(QDate.currentDate())
        self.dateEdit_actividad.setDate(QDate.currentDate())

        # Modulo de contenidos: ENLACES
        self.btn_addEnlace.clicked.connect(self.agregarEnlace)
        self.btn_verEnlaces.clicked.connect(self.verEnlaces)
        self.btn_elimTodosEnl.clicked.connect(self.eliminarTodosLosEnlaces)
        self.radioBtnOtro.clicked.connect(self.activarTextoEnlace)
        self.radioBtnYt.clicked.connect(self.seleccionarYoutube)
        self.radioBtnTw.clicked.connect(self.seleccionarTwitter)
        self.radioBtnFB.clicked.connect(self.seleccionarFacebook)
        self.radioBtnPnt.clicked.connect(self.seleccionarPinterest)

        # Modulo de contenidos: GALERIA DE IMAGENES
        self.btn_selec_img.clicked.connect(self.seleccionarImg)
        self.btn_addImg.clicked.connect(self.agregarImagen)
        self.btn_verImg.clicked.connect(self.verImagenes)
        self.btn_elimTodasImg.clicked.connect(self.eliminarTodasLasImagenes)


    # Abrir la ventana de nuevo proyecto desde el menu nuevo
    def crearProyecto(self):
        self.window = NuevoProyectoV()
        self.window.show()

    # Abrir un dialogo para seleccionar la imagen
    def abrirFicheroImg(self):
        img_ruta = QFileDialog.getOpenFileName(None, "Buscar imagen", '', "Image files (*.jpg *.png)")
        img_aux = str(img_ruta)
        pos = img_aux.find(",")
        self.origen = str(img_aux[2:pos-1])
        img_nombre = os.path.basename(self.origen)
        self.txt_logo.setText(img_nombre)

    # Agregar miembros de la junta directiva a la lista
    def addJuntaDirect(self):
        miembro_jd = self.txt_juntaDir.toPlainText()
        self.listWidget_juntaDir.addItem(miembro_jd)
        self.txt_juntaDir.clear()

    # Eliminar miembros de la junta directiva de la lista
    def elimJuntaDirect(self):
        items = self.listWidget_juntaDir.selectedItems()
        for i in items:
            self.listWidget_juntaDir.takeItem(self.listWidget_juntaDir.row(i))

    # Obtener los datos del proyecto y los muestra
    def consultarSitioWeb(self):

        controladorP = ControladorProyecto()
        proyecto = controladorP.consultarSitioWeb()
        # Si no existe proyecto, se muestra un mensaje de error
        if proyecto is None:
            reply = QMessageBox.critical(self, "Error",
                                    "Proyecto no encontrado",
                                    QMessageBox.Ok)

            if reply == QMessageBox.Ok:
                self.limpiarCampos()
                self.controlErrores = True
        else:
            self.controlErrores = False
            self.txt_nombProy.setText(proyecto.__getattribute__("nombre_proyecto"))

            if len(proyecto.__getattribute__("nombre_web")) > 0:
                self.txt_nomWeb.setText(proyecto.__getattribute__("nombre_web"))

            if len(proyecto.__getattribute__("logo")) > 0:
                self.txt_logo.setText(proyecto.__getattribute__("logo"))

            if len(proyecto.__getattribute__("telefono")) > 0:
                self.txt_telef.setText(proyecto.__getattribute__("telefono"))

            if len(proyecto.__getattribute__("email")) > 0:
                self.txt_email.setText(proyecto.__getattribute__("email"))

            if len(proyecto.__getattribute__("direccion")) > 0:
                self.txt_dir.setText(proyecto.__getattribute__("direccion"))

            if len(proyecto.__getattribute__("resumen")) > 0:
                self.txt_resum.setPlainText(proyecto.__getattribute__("resumen"))

            if len(proyecto.__getattribute__("sobrenosotros")) > 0:
                self.txt_sobrenos.setPlainText(proyecto.__getattribute__("sobrenosotros"))

            if len(proyecto.__getattribute__("historia")) > 0:
                self.txt_hist.setPlainText(proyecto.__getattribute__("historia"))

            self.listWidget_juntaDir.clear()
            if len(proyecto.__getattribute__("junta_directiva")) > 0:
                for jd in proyecto.__getattribute__("junta_directiva"):
                    self.listWidget_juntaDir.addItem(jd)

    # Cargar los datos de un proyecto existente en la aplicacion
    def abrirProyecto(self):
        # Seleccionar el proyecto que desea abrir
        directorio = str(QFileDialog.getExistingDirectory(self, "Abrir proyecto", "C:\\Users"))
        new_dir = directorio.replace('/', '\\')

        # Si existe un directorio seleccionado se obtienen los datos y se muestran
        if len(new_dir) > 0:
            nomP = os.path.basename(new_dir)
            c = ControladorProyecto()
            msgAbrirProy = c.abrirProyecto(nomP, new_dir)
            if msgAbrirProy is None:
                #Obtener datos
                self.consultarSitioWeb()

                # Si no existen errores en la obtencion de datos, se muestran en la aplicacion
                if self.controlErrores != True:

                    # Se habilitan los botones y campos de formulario para realizar las acciones una vez abierto el proyecto
                    self.btn_editWeb.setEnabled(True)
                    self.btn_mostrarPlant.setEnabled(True)
                    self.mostrarPlantillaActual()
                    self.actionCerrar_proyecto.setEnabled(True)
                    self.actionAbrir_proyecto.setEnabled(False)
                    self.actionNuevo_proyecto.setEnabled(False)

                    self.btn_addNoticia.setEnabled(True)
                    self.btn_elimTodasNotic.setEnabled(True)
                    self.btn_verNotic.setEnabled(True)
                    self.txt_tituloNotic.setEnabled(True)
                    self.txt_descripNoticia.setEnabled(True)
                    self.dateEdit_noticia.setEnabled(True)

                    self.btn_addAct.setEnabled(True)
                    self.btn_elimTodasAct.setEnabled(True)
                    self.btn_verAct.setEnabled(True)
                    self.txt_nomAct.setEnabled(True)
                    self.txt_descripAct.setEnabled(True)
                    self.txt_lugarAct.setEnabled(True)
                    self.dateEdit_actividad.setEnabled(True)
                    self.timeEdit_act.setEnabled(True)

                    self.txt_urlEnl.setEnabled(True)
                    self.btn_addEnlace.setEnabled(True)
                    self.btn_elimTodosEnl.setEnabled(True)
                    self.btn_verEnlaces.setEnabled(True)
                    self.radioBtnFB.setEnabled(True)
                    self.radioBtnOtro.setEnabled(True)
                    self.radioBtnPnt.setEnabled(True)
                    self.radioBtnTw.setEnabled(True)
                    self.radioBtnYt.setEnabled(True)

                    self.txt_tituloImg.setEnabled(True)
                    self.btn_addImg.setEnabled(True)
                    self.btn_elimTodasImg.setEnabled(True)
                    self.btn_verImg.setEnabled(True)
                    self.btn_selec_img.setEnabled(True)

                    self.lineEdit_host.setEnabled(True)
                    self.lineEdit_usr.setEnabled(True)
                    self.lineEdit_psw.setEnabled(True)
                    self.lineEdit_puerto.setEnabled(True)
                    self.btnPublicar.setEnabled(True)
            else:
                QMessageBox.critical(self, "Error",msgAbrirProy,
                                             QMessageBox.Ok)

    # Deshabilitar los botones y mostrar el contenido del proyecto antes de activar la edicion
    def cancelarEdicion(self):
        self.btn_guardWeb.setEnabled(False)
        self.btn_cancelEdit.setEnabled(False)
        self.btn_editWeb.setEnabled(True)

        self.habilitar_deshabilitar_campos(False)
        self.consultarSitioWeb()

    # habilitacion/deshabilitacion de campos de los datos del proyecto
    def habilitar_deshabilitar_campos(self,valor):
        self.txt_hist.setEnabled(valor)
        self.txt_nomWeb.setEnabled(valor)
        self.txt_sobrenos.setEnabled(valor)
        self.txt_resum.setEnabled(valor)
        self.txt_dir.setEnabled(valor)
        self.txt_email.setEnabled(valor)
        self.txt_telef.setEnabled(valor)
        self.txt_juntaDir.setEnabled(valor)
        self.btn_selec_logo.setEnabled(valor)
        self.btn_agregarJuntDir.setEnabled(valor)
        self.btn_elimJuntDir.setEnabled(valor)
        self.listWidget_juntaDir.setEnabled(valor)

    #Habilitacion de los campos del formulario de edicion
    def editarSitioWeb(self):
        self.btn_cancelEdit.setEnabled(True)
        self.btn_guardWeb.setEnabled(True)
        self.btn_editWeb.setEnabled(False)
        self.habilitar_deshabilitar_campos(True)

    # Obtener los datos del formulario de edicion del sitio web y pasarlos al controlador
    def actualizarSitioWeb(self):
        # obtener los valores del formulario
        nomP = self.txt_nombProy.toPlainText()
        nomW = self.txt_nomWeb.toPlainText()
        tlf = self.txt_telef.toPlainText()
        email = self.txt_email.toPlainText()
        dir = self.txt_dir.toPlainText()
        logo = self.txt_logo.toPlainText()
        res = self.txt_resum.toPlainText()
        info = self.txt_sobrenos.toPlainText()
        hist = self.txt_hist.toPlainText()

        items_jd = []
        for index in range(self.listWidget_juntaDir.count()):
            items_jd.append(self.listWidget_juntaDir.item(index).text())

        if len(nomW) == 0:
            msg = "El nombre del sitio web es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        elif len(email) == 0:
            msg = "El correo electrónico es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        elif len(tlf) == 0:
            msg = "El teléfono es obligatorio"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        else:
            # Validar datos antes de enviarlos al controlador para guardarlos en el XML
            c = ControladorProyecto()
            mensajesValidacion = c.obtenerMensajesValidacion(nomP, nomW, logo, res, email, tlf, dir, info, hist, items_jd)

            # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
            if len(mensajesValidacion) > 0:
                mensaje = ""
                for m in mensajesValidacion:
                    mensaje = mensaje + "\n" + m

                QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)

            else:
                c.editarSitioWeb(nomP, nomW, logo, res, email, tlf, dir, info, hist, items_jd, self.origen)
                self.cancelarEdicion()

    # Cerrar proyecto, limpiar campos y deshabilitar botones
    def cerrarProyecto(self):
        msg = "¿Está seguro que desea cerrar? Los cambios no guardados se perderán."
        reply = QMessageBox.warning(self, "Cerrar proyecto",
                                     msg,
                                     QMessageBox.No | QMessageBox.Ok)
        if reply == QMessageBox.Ok:
            self.limpiarCampos()
            self.actionNuevo_proyecto.setEnabled(True)

    # Set enablesd a False y quitar texto de los campos de formulario
    def limpiarCampos(self):
        self.txt_nombProy.clear()
        self.txt_nomWeb.clear()
        self.txt_juntaDir.clear()
        self.txt_sobrenos.clear()
        self.txt_hist.clear()
        self.txt_resum.clear()
        self.txt_logo.clear()
        self.txt_telef.clear()
        self.txt_email.clear()
        self.txt_dir.clear()
        self.listWidget_juntaDir.clear()
        self.lbl_img_plSelec.clear()
        self.lbl_img_plActual.clear()
        self.lineEdit_host.clear()
        self.lineEdit_usr.clear()
        self.lineEdit_psw.clear()
        self.lineEdit_puerto.clear()

        self.btn_editWeb.setEnabled(False)

        self.actionPrevisualizar_sitio_web.setEnabled(False)
        self.actionCerrar_proyecto.setEnabled(False)
        self.actionAbrir_proyecto.setEnabled(True)

        self.btn_guardarPlant.setEnabled(False)

        self.btn_editEstilo.setEnabled(False)
        self.btn_prev.setEnabled(False)
        self.btn_mostrarPlant.setEnabled(False)

        self.btn_addNoticia.setEnabled(False)
        self.btn_elimTodasNotic.setEnabled(False)
        self.btn_verNotic.setEnabled(False)
        self.txt_tituloNotic.setEnabled(False)
        self.txt_descripNoticia.setEnabled(False)
        self.dateEdit_noticia.setEnabled(False)

        self.btn_addAct.setEnabled(False)
        self.btn_elimTodasAct.setEnabled(False)
        self.btn_verAct.setEnabled(False)
        self.txt_nomAct.setEnabled(False)
        self.txt_descripAct.setEnabled(False)
        self.txt_lugarAct.setEnabled(False)
        self.dateEdit_actividad.setEnabled(False)
        self.timeEdit_act.setEnabled(False)

        self.txt_tituloEnl.setEnabled(False)
        self.txt_urlEnl.setEnabled(False)
        self.btn_addEnlace.setEnabled(False)
        self.btn_elimTodosEnl.setEnabled(False)
        self.btn_verEnlaces.setEnabled(False)
        self.radioBtnFB.setEnabled(False)
        self.radioBtnOtro.setEnabled(False)
        self.radioBtnPnt.setEnabled(False)
        self.radioBtnTw.setEnabled(False)
        self.radioBtnYt.setEnabled(False)

        self.txt_tituloImg.setEnabled(False)
        self.btn_addImg.setEnabled(False)
        self.btn_elimTodasImg.setEnabled(False)
        self.btn_verImg.setEnabled(False)
        self.btn_selec_img.setEnabled(False)

        self.lineEdit_host.setEnabled(False)
        self.lineEdit_usr.setEnabled(False)
        self.lineEdit_psw.setEnabled(False)
        self.lineEdit_puerto.setEnabled(False)
        self.btnPublicar.setEnabled(False)

    # Mostrar una imagen de la plantilla seleccionada
    def mostrarPlantilla(self):
        text = str(self.comboBox_plantillas.currentText())
        if text == "Plantilla_1":
            pixmap = QtGui.QPixmap(".\\plantillas\\p1\\Plantilla_1.png")
            self.pixmap4 = pixmap.scaled(301, 511, QtCore.Qt.KeepAspectRatio)
            self.lbl_img_plSelec.setPixmap(QtGui.QPixmap(self.pixmap4))
        elif text == "Plantilla_2":
            pixmap = QtGui.QPixmap(".\\plantillas\\p2\\Plantilla_2.png")
            self.pixmap4 = pixmap.scaled(301, 511, QtCore.Qt.KeepAspectRatio)
            self.lbl_img_plSelec.setPixmap(QtGui.QPixmap(self.pixmap4))

        self.btn_guardarPlant.setEnabled(True)

    # Guardar la plantilla seleccionada
    def guardarPlantilla(self):

        msg = "Si cambia de plantilla los cambios de estilo realizados en la plantilla actual (si tiene una guardada previamente) se perderán. Si desea conservarlos, cree un nuevo proyecto.¿Desea continuar?"
        reply = QMessageBox.warning(self, "Guardar plantilla",
                                     msg,
                                     QMessageBox.No | QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            self.lbl_img_plActual.setPixmap(QtGui.QPixmap(self.pixmap4))
            c = ControladorPlantilla()
            txt = str(self.comboBox_plantillas.currentText())
            c.guardarPlantilla(txt)
            self.btn_editEstilo.setEnabled(True)
            self.btn_prev.setEnabled(True)
            self.actionPrevisualizar_sitio_web.setEnabled(True)


    # Mostrar una imagen previa de la plantilla seleccionada actualmente
    def mostrarPlantillaActual(self):
        c = ControladorPlantilla()
        ruta = c.obtenerPlantillaActual()
        id = c.obtenerIdPlantilla()
        if (not ruta is None) and (len(id) > 0):
            plantilla = ruta + "\\" + id + ".png"
            pixmap = QtGui.QPixmap(plantilla)
            self.pixmap4 = pixmap.scaled(301, 511, QtCore.Qt.KeepAspectRatio)
            self.lbl_img_plActual.setPixmap(QtGui.QPixmap(self.pixmap4))
            self.btn_editEstilo.setEnabled(True)
            self.btn_prev.setEnabled(True)
            self.actionPrevisualizar_sitio_web.setEnabled(True)


    # Abrir ventana de edicion de estilo
    def editarEstilo(self):
        self.ventana = Estilo()
        self.ventana.show()

    # Previsualizar el fichero html llamando al controlador del proyecto
    def previsualizar(self):

        c = ControladorProyecto()
        msg = c.renderizar()

        if msg != None:
            QMessageBox.critical(self, "Previsualizar",
                                msg,
                                QMessageBox.Ok)

        msgNav = c.abrirNavegador()
        if msgNav != None:
            QMessageBox.critical(self, "Previsualizar",
                                msgNav,
                                QMessageBox.Ok)


    # Modulo de noticias
    def agregarNoticia(self):

        #Obtener datos del formulario
        titulo = self.txt_tituloNotic.toPlainText()
        descripcion = self.txt_descripNoticia.toPlainText()
        fecha = self.dateEdit_noticia.text()

        # Pasar los datos al controlador
        c = ControladorNoticia()
        mensajesValidacion = c.obtenerMensajesValidacion(titulo, descripcion)

        # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)
        else:

            c.agregarNoticia(titulo, descripcion, fecha)

            # Limpiar los campos del formulario
            self.txt_tituloNotic.clear()
            self.txt_descripNoticia.clear()

    # Abrir ventana de Noticias
    def verNoticias(self):
        self.ventana = Noticias()
        self.ventana.show()

    def eliminarTodasLasNoticias(self):
        mensaje = "¿Está seguro que desea eliminar todas las noticias?"
        respuesta = QMessageBox.warning(self, "Error", mensaje, QMessageBox.Ok | QMessageBox.No)

        if respuesta == QMessageBox.Ok:
            controlador = ControladorNoticia()
            controlador.eliminarTodasLasNoticias()

    # Modulo de actividades
    def agregarActividad(self):
        #Obtener datos del formulario
        nombre = self.txt_nomAct.toPlainText()
        descripcion = self.txt_descripAct.toPlainText()
        fecha = self.dateEdit_actividad.text()
        hora = self.timeEdit_act.text()
        lugar = self.txt_lugarAct.toPlainText()

        # Pasar los datos al controlador
        c = ControladorActividad()
        mensajesValidacion = c.obtenerMensajesValidacion(nombre, descripcion, lugar)

        # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)
        else:
            c.agregarActividad(nombre, descripcion, fecha, hora, lugar)

            # Limpiar los campos del formulario
            self.txt_nomAct.clear()
            self.txt_descripAct.clear()
            self.txt_lugarAct.clear()

    # Abrir ventana de actividades
    def verActividades(self):
        self.ventana = Actividades()
        self.ventana.show()

    def eliminarTodasLasActividades(self):
        mensaje = "¿Está seguro que desea eliminar todas las actividades?"
        respuesta = QMessageBox.warning(self, "Advertencia", mensaje, QMessageBox.Ok | QMessageBox.No)

        if respuesta == QMessageBox.Ok:
            controlador = ControladorActividad()
            controlador.eliminarTodasLasActividades()

    # Modulo de enlaces
    def activarTextoEnlace(self):
        self.txt_tituloEnl.setEnabled(True)
        self.txt_tituloEnl.clear()

    def seleccionarFacebook(self):
        self.txt_tituloEnl.setText(self.radioBtnFB.text())
        self.txt_tituloEnl.setEnabled(False)

    def seleccionarTwitter(self):
        self.txt_tituloEnl.setText(self.radioBtnTw.text())
        self.txt_tituloEnl.setEnabled(False)

    def seleccionarYoutube(self):
        self.txt_tituloEnl.setText(self.radioBtnYt.text())
        self.txt_tituloEnl.setEnabled(False)

    def seleccionarPinterest(self):
        self.txt_tituloEnl.setText(self.radioBtnPnt.text())
        self.txt_tituloEnl.setEnabled(False)

    def agregarEnlace(self):
        # Obtener datos del formulario
        texto = self.txt_tituloEnl.toPlainText()
        url = self.txt_urlEnl.toPlainText()

        # Validar y pasar los datos al controlador
        c = ControladorEnlace()
        mensajesValidacion = c.obtenerMensajesValidacion(texto, url)

        # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
        if len(mensajesValidacion) > 0:
            mensaje = ""
            for m in mensajesValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Error de validación", mensaje, QMessageBox.Ok)
        else:
            c.agregarEnlace(texto, url)

            # Limpiar los campos del formulario
            self.txt_tituloEnl.clear()
            self.txt_urlEnl.clear()

    # Abrir ventana de enlaces
    def verEnlaces(self):
        self.ventana = Enlaces()
        self.ventana.show()

    def eliminarTodosLosEnlaces(self):
        mensaje = "¿Está seguro que desea eliminar todos los enlaces?"
        respuesta = QMessageBox.warning(self, "Advertencia", mensaje, QMessageBox.Ok | QMessageBox.No)

        if respuesta == QMessageBox.Ok:
            controlador = ControladorEnlace()
            controlador.eliminarTodosLosEnlaces()

    # Modulo de imagenes
    # Selecciona la imagen para agregar a la galeria
    def seleccionarImg(self):
        img_ruta = QFileDialog.getOpenFileName(None, "Buscar imagen", '', "Image files (*.jpg *.png)")
        img_aux = str(img_ruta)
        pos = img_aux.find(",")
        self.origen = str(img_aux[2:pos - 1])
        img_nombre = os.path.basename(self.origen)
        self.txt_url_img.setText(img_nombre)

    def agregarImagen(self):
        # Obtener datos del formulario
        titulo = self.txt_tituloImg.toPlainText()
        nombre_img =  self.txt_url_img.toPlainText()
        # Pasar los datos al controlador
        c = ControladorImagen()

        if (len(nombre_img) == 0) or (len(self.origen) == 0):
            msg = "Seleccione una imagen"
            QMessageBox.critical(self, "Error", msg, QMessageBox.Ok)
        else:
            mensajesValidacion = c.obtenerMensajesValidacion(titulo)

            # Si existen errore de validacion, se muestrasn, sino se envian los datos al controlador
            if len(mensajesValidacion) > 0:
                mensaje = ""
                for m in mensajesValidacion:
                    mensaje = mensaje + "\n" + m

                QMessageBox.critical(self, "Error", mensaje, QMessageBox.Ok)
            else:
                resultado = c.agregarImagen(titulo, nombre_img, self.origen)

                if resultado != None:
                    QMessageBox.critical(self, "Error", resultado, QMessageBox.Ok)

                # Limpiar los campos del formulario
                self.txt_tituloImg.clear()
                self.txt_url_img.clear()

    # Abrir ventana de Imagenes
    def verImagenes(self):
        self.ventana = Imagenes()
        self.ventana.show()

    def eliminarTodasLasImagenes(self):
        mensaje = "¿Está seguro que desea eliminar todas las imágenes?"
        respuesta = QMessageBox.warning(self, "Advertencia", mensaje, QMessageBox.Ok | QMessageBox.No)

        if respuesta == QMessageBox.Ok:
            controlador = ControladorImagen()
            controlador.eliminarTodasLasImagenes()

    # Publicar sitio web
    def publicar(self):

        # Obtener los campos del formulario
        host = self.lineEdit_host.text()
        usr = self.lineEdit_usr.text()
        psw = self.lineEdit_psw.text()
        puerto = self.lineEdit_puerto.text()
        self.btnPublicar.setEnabled(False)

        # Pasar datos al controlador
        c = ControladorProyecto()
        msgValidacion = c.validarPublicacion(host, usr, psw, puerto)
        if len(msgValidacion) > 0:
            mensaje = ""
            for m in msgValidacion:
                mensaje = mensaje + "\n" + m

            QMessageBox.critical(self, "Publicar sitio web", mensaje, QMessageBox.Ok)
            self.btnPublicar.setEnabled(True)
        else:

            resultado = c.publicar(host, usr, psw, puerto)

            if resultado is None:
                QMessageBox.information(self, "Publicar sitio web",
                                    "El sitio web ha sido publicado con éxito",
                                    QMessageBox.Ok)

                self.lineEdit_host.clear()
                self.lineEdit_usr.clear()
                self.lineEdit_psw.clear()
                self.lineEdit_puerto.clear()
                self.btnPublicar.setEnabled(True)
            else:
                QMessageBox.critical(self, "Publicar sitio web",
                                            resultado,
                                            QMessageBox.Ok)
                self.btnPublicar.setEnabled(True)

    # Consultar manual de usuario
    def consultarManual(self):
        controlador = ControladorProyecto()
        controlador.consultarManualUsuario()


if __name__ == "__main__":
    # Ejecutar la aplicacion
    app = QtWidgets.QApplication(sys.argv)
    main_window = AsistenteWeb()
    main_window.show()
    sys.exit(app.exec_())
