# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtWidgets import QMessageBox, QColorDialog, QFileDialog
from ControladorPlantillas import *
from gen_estilo import *
from ControladorImagenes import *
c = ControladorPlantilla()

class Estilo(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, *args, **kwargs):
        super(Estilo, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.mostrarEstilo()
        self.btn_guardEstilo.clicked.connect(self.modificarEstilo)
        self.btn_colorbgSecc.clicked.connect(self.selecColorBg)
        self.btn_colorWeb.clicked.connect(self.selecColorWeb)
        self.btn_colorh.clicked.connect(self.selecColorH)
        self.btn_colorP.clicked.connect(self.selecColorP)
        self.btn_colorPsec.clicked.connect(self.selecColorPsec)
        self.btn_valorespredet.clicked.connect(self.restablecerValores)

    def mostrarEstilo(self):
        # Mostrar los valores actuales
        propiedades = c.parsearCSS()
        if not propiedades is None:
            self.btn_valorespredet.setEnabled(True)
            self.btn_guardEstilo.setEnabled(True)
            self.btn_cancelEdit.setEnabled(True)
            self.lbl_bg_color_sec.setText(propiedades['--bg_color_seccion'])
            prop = "color: " + propiedades['--bg_color_seccion']
            self.lbl_bg_color_sec.setStyleSheet(prop)

            self.lbl_h_color.setText(propiedades['--h_color'])
            prop = "color: " + propiedades['--h_color']
            self.lbl_h_color.setStyleSheet(prop)

            self.lbl_p_color.setText(propiedades['--p_color_body'])
            prop = "color: " + propiedades['--p_color_body']
            self.lbl_p_color.setStyleSheet(prop)

            self.lbl_p_color_sec.setText(propiedades['--p_color_section'])
            prop = "color: " + propiedades['--p_color_section']
            self.lbl_p_color_sec.setStyleSheet(prop)

            self.lbl_name_web_color.setText(propiedades['--name_website_color'])
            prop = "color: " + propiedades['--name_website_color']
            self.lbl_name_web_color.setStyleSheet(prop)

            h_font = str(propiedades['--h_tipoFuente'][2:len(propiedades['--h_tipoFuente']) - 1])
            p_font = str(propiedades['--p_tipoFuente'][2:len(propiedades['--p_tipoFuente']) - 1])

            self.h_fontComboBox.setCurrentFont(QFont(h_font))
            self.p_fontComboBox_2.setCurrentFont(QFont(p_font))
        else:
            QMessageBox.information(self, "Editar estilo",
                                    "Seleccione una plantilla, por favor.",
                                    QMessageBox.Ok)
            self.btn_valorespredet.setEnabled(False)
            self.btn_guardEstilo.setEnabled(False)
            self.btn_cancelEdit.setEnabled(False)


    def modificarEstilo(self):
        # Obtener los valores del formulario y pasarlos al controlador
        bg_color_sec = self.lbl_bg_color_sec.text()
        h_color = self.lbl_h_color.text()
        p_color_sec = self.lbl_p_color_sec.text()
        p_color_body = self.lbl_p_color.text()
        web_color = self.lbl_name_web_color.text()
        h_font = "'" + self.h_fontComboBox.currentText() + "'"
        p_font = "'" + self.p_fontComboBox_2.currentText() + "'"

        c.modificarCSS(bg_color_sec, h_color, p_color_sec, p_color_body, web_color, h_font, p_font)
        self.close()

    # Seleccionar colores
    def seleccionarColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            return color.name()
        else:
            return "#545454"

    def selecColorBg(self):
        color = self.seleccionarColor()
        self.lbl_bg_color_sec.setText(color)
        prop = "color: " + color
        self.lbl_bg_color_sec.setStyleSheet(prop)

    def selecColorWeb(self):
        color = self.seleccionarColor()
        self.lbl_name_web_color.setText(color)
        prop = "color: " + color
        self.lbl_name_web_color.setStyleSheet(prop)

    def selecColorH(self):
        color = self.seleccionarColor()
        self.lbl_h_color.setText(color)
        prop = "color: " + color
        self.lbl_h_color.setStyleSheet(prop)

    def selecColorP(self):
        color = self.seleccionarColor()
        self.lbl_p_color.setText(color)
        prop = "color: " + color
        self.lbl_p_color.setStyleSheet(prop)

    def selecColorPsec(self):
        color = self.seleccionarColor()
        self.lbl_p_color_sec.setText(color)
        prop = "color: " + color
        self.lbl_p_color_sec.setStyleSheet(prop)

    # Restablecer valores predeterminados
    def restablecerValores(self):
        valores = c.obtenerValoresOriginales()

        self.lbl_bg_color_sec.setText(valores.bg_color_seccion)
        prop = "color: " + valores.bg_color_seccion
        self.lbl_bg_color_sec.setStyleSheet(prop)

        self.lbl_h_color.setText(valores.h_color)
        prop = "color: " + valores.h_color
        self.lbl_h_color.setStyleSheet(prop)

        self.lbl_p_color.setText(valores.p_color_body)
        prop = "color: " + valores.p_color_body
        self.lbl_p_color.setStyleSheet(prop)

        self.lbl_p_color_sec.setText(valores.p_color_section)
        prop = "color: " + valores.p_color_section
        self.lbl_p_color_sec.setStyleSheet(prop)

        self.lbl_name_web_color.setText(valores.name_website_color)
        prop = "color: " + valores.name_website_color
        self.lbl_name_web_color.setStyleSheet(prop)

        h_font = str(valores.h_tipoFuente[2:len(valores.h_tipoFuente)-1])
        p_font = str(valores.p_tipoFuente[2:len(valores.p_tipoFuente)-1])

        self.h_fontComboBox.setCurrentFont(QFont(h_font))
        self.p_fontComboBox_2.setCurrentFont(QFont(p_font))