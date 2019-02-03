# -*- coding: utf-8 -*-
import shutil, os, re
from Control_app import *
from Plantilla import *


class ControladorPlantilla(object):

    def guardarPlantilla(self, idPlantilla):
        c = Control()
        proyectoActual = c.obtenerProyectoActual()
        directorioWS = c.obtenerWorkspace()
        dirPlantillas = directorioWS + "\\" + proyectoActual + "\\plantillas"

        # Listar los directorios existentes en plantillas
        dirs = os.listdir(dirPlantillas)
        for d in dirs:
            # Buscar el directorio de la plantilla y eliminarlo
            if re.match("p[0-9]", d):
                dir_aux = dirPlantillas + "\\" + d
                shutil.rmtree(dir_aux)

        # Copiar el directorio de la plantilla seleccionada
        if idPlantilla == "Plantilla_1":
            dirP = dirPlantillas + "\\p1"
            shutil.copytree(".\\plantillas\\p1", dirP)
        elif idPlantilla == "Plantilla_2":
            dirP = dirPlantillas + "\\p2"
            shutil.copytree(".\\plantillas\\p2", dirP)

        # Establecer la plantilla actual y parsear el css correspondiente para obtener los valores
        c.asignarIdPlantillaActual(idPlantilla)
        c.asignarRutaPlantillaActual(dirP)
        props = self.parsearCSS()

        plantilla = Plantilla(props['--bg_color_seccion'],props['--h_color'], props['--p_color_section'],
                              props['--p_color_body'], props['--name_website_color'], props['--h_tipoFuente'],
                              props['--p_tipoFuente'])

        plantilla.guardarValoresOriginalesXML()


    def obtenerPlantillaActual(self):
        c = Control()
        proyectoActual = c.obtenerProyectoActual()
        directorioWS = c.obtenerWorkspace()
        dirPlantillas = directorioWS + "\\" + proyectoActual + "\\plantillas"
        # Listar los directorios existentes en plantillas
        dir_aux = None
        dirs = os.listdir(dirPlantillas)
        for d in dirs:
            # Buscar el directorio de la plantilla si existe
            if re.match("p[0-9]", d):
                dir_aux = dirPlantillas + "\\" + d

                if d == "p1":
                    c.asignarIdPlantillaActual("Plantilla_1")
                elif d == 'p2':
                    c.asignarIdPlantillaActual("Plantilla_2")

        return dir_aux

    def obtenerIdPlantilla(self):
        c = Control()
        id = c.obtenerIdPlantillaAtual()
        return id

    def parsearCSS(self):
        if os.path.isdir(self.obtenerPlantillaActual()):
            fichero = self.obtenerPlantillaActual() + "\\rules.css"

            hoja_estilos = open(fichero, "r")
            array_auxiliar = []

            # Recorrer las 8 primeras lineas del fichero rules.css donde estan declaradas las variables
            for i in range(8):
                linea = hoja_estilos.readline()
                array_auxiliar.append(linea)

            # Eliminar el primer elemento del array (:root), no interesa
            array_auxiliar.pop(0)
            # Obtener y asignar las propiedades con su valor a un diccionario
            self.propiedades = {}
            for a in array_auxiliar:
                # Cada elemento del array tiene una estructura similar a: '    --bg_color_seccion: #F05F40;\n'
                # Buscar los ":", ";" y "-" en cada elemento para obtener solo el nombre de la variable y su valor
                pos_dospuntos = a.find(":")
                pos_guion = a.find("-")
                pos_puntcoma = a.find(";")
                clave = str(a[pos_guion:pos_dospuntos])
                valor = str(a[pos_dospuntos + 1:pos_puntcoma])

                self.propiedades[clave] = valor

            return self.propiedades
        else:
            return None

    def modificarCSS(self, bg_color_sec, h_color, p_color_sec, p_color_body, web_color, h_font, p_font):

        fichero = self.obtenerPlantillaActual() + "\\rules.css"

        self.propiedades['--bg_color_seccion'] = bg_color_sec
        self.propiedades['--h_color'] = h_color
        self.propiedades['--p_color_section'] = p_color_sec
        self.propiedades['--p_color_body'] = p_color_body
        self.propiedades['--name_website_color'] = web_color
        self.propiedades['--h_tipoFuente'] = h_font
        self.propiedades['--p_tipoFuente'] = p_font

        # Abrir fichero para sobreescribirlo con los valores nuevos
        hoja_estilos = open(fichero, "w")
        lineas = [":root {\n"]
        for clave in self.propiedades:
            linea = "   " + clave + ": " + self.propiedades[clave] + ";\n"
            lineas.append(linea)

        lineas.append("}\n")

        for l in lineas:
            hoja_estilos.write(l)

    def obtenerValoresOriginales(self):
        p = Plantilla()
        valores = p.obtenerValoresXML()
        return valores