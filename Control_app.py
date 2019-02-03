# -*- coding: utf-8 -*-
# Fichero de control de variables globales
import xml.etree.ElementTree as ET
import shutil

import os


class Control(object):

    # Realizar una copia del fichero original para trabajar sobre la copia
    def configurarFicheroInicial(self):
        try:
            shutil.copy('.\\control\\control_original.xml', '.\\control\\control.xml')
            self.asignarWorskpace()
            self.asignarRutaDirRecusros('.\\recursos')
        except Exception as err:
            print("Error: {0}".format(err))

    # Obtiene el arbol del XML del fichero de control para parsearlo y trabajar con el
    def asignarFicheroParse(self):
        arbol = ET.parse('.\\control\\control.xml')
        return arbol

    # Obtiene el directorio de trabajo
    def obtenerWorkspace(self):
        arbol = self.asignarFicheroParse()
        ws = arbol.findtext("workspace")
        return ws

    # Asigna el directorio de trabajo
    def asignarWorskpace(self):
        arbol = self.asignarFicheroParse()
        ws = arbol.find("workspace")
        import getpass
        # El nombre del usuario actual
        user = getpass.getuser()
        dir = "C:\\Users\\" + user + "\\WebAsistDesigner\\Workspace"

        if not os.path.isdir(dir):
            os.makedirs(dir)

        ws.text = dir

        arbol.write(".\\control\\control.xml")

    # Obtiene el proyecto actual
    def obtenerProyectoActual(self):
        arbol = self.asignarFicheroParse()
        pa = arbol.findtext("proyecto_actual")
        return pa

    # Establece el proyecto pasado como parametro, como proyecto actual
    def asignarProyectoActual(self, actual):
        arbol = self.asignarFicheroParse()
        pa = arbol.find("proyecto_actual")
        pa.text = actual
        arbol.write(".\\control\\control.xml")

    # Obtiene la ruta del directorio de recursos origen
    def obtenerRutaDirRecursos(self):
        arbol = self.asignarFicheroParse()
        ruta_recursos = arbol.findtext("ruta_dir_recursos")
        return ruta_recursos

    # Asigna la ruta del directorio de recursos origen
    def asignarRutaDirRecusros(self, ruta):
        arbol = self.asignarFicheroParse()
        ruta_recursos = arbol.find("ruta_dir_recursos")
        ruta_recursos.text = ruta
        arbol.write(".\\control\\control.xml")

    # Obtiene la ruta del directorio de recursos destino para cada proyecto
    def obtenerRutaDirRecursosDestino(self):
        arbol = self.asignarFicheroParse()
        ruta_recursos_destino = arbol.findtext("ruta_dir_recursos_destino")
        return ruta_recursos_destino

    # Asigna la ruta del directorio de recursos destino para cada proyecto
    def asignarRutaDirRecusrosDestino(self, ruta):
        arbol = self.asignarFicheroParse()
        ruta_recursos = arbol.find("ruta_dir_recursos_destino")
        ruta_recursos.text = ruta
        arbol.write(".\\control\\control.xml")

    # Obtiene la ruta del directorio de imagenes
    def obtenerRutaDirImg(self):
        arbol = self.asignarFicheroParse()
        ruta_img = arbol.findtext("ruta_img")
        return ruta_img

    # Asigna la ruta del directorio de imagenes
    def asignarRutaDirImg(self, ruta):
        arbol = self.asignarFicheroParse()
        ruta_img = arbol.find("ruta_img")
        ruta_img.text = ruta
        arbol.write(".\\control\\control.xml")

    # Obtiene el contador de id de noticias para cada proyecto
    def obtenerIdNoticia(self):
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        contador = arbol.findtext("id_noticia")
        return contador

    # Aumenta el contador de id de noticias para cada proyecto
    def aumentarIdNoticia(self, id):
        id_int = int(id)
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        cont = arbol.find("id_noticia")
        cont.text = str(id_int + 1)
        arbol.write(fichero_control_id)

    # Obtiene el contador de id de actividades para cada proyecto
    def obtenerIdActividad(self):
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        contador = arbol.findtext("id_actividad")
        return contador

    # Aumenta el contador de id de actividades para cada proyecto
    def aumentarIdActividad(self, id):
        id_int = int(id)
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        cont = arbol.find("id_actividad")
        cont.text = str(id_int + 1)
        arbol.write(fichero_control_id)

    # Obtiene el contador de id de enlaces para cada proyecto
    def obtenerIdEnlace(self):
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        contador = arbol.findtext("id_enlace")
        return contador

    # Aumenta el contador de id de enlaces para cada proyecto
    def aumentarIdEnlace(self, id):
        id_int = int(id)
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        cont = arbol.find("id_enlace")
        cont.text = str(id_int + 1)
        arbol.write(fichero_control_id)

    # Obtiene el contador de id de imagenes para cada proyecto
    def obtenerIdImagen(self):
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        contador = arbol.findtext("id_imagen")
        return contador

    # Aumenta el contador de id de imagenes para cada proyecto
    def aumentarIdImagen(self, id):
        id_int = int(id)
        recursos = self.obtenerRutaDirRecursosDestino()
        fichero_control_id = recursos + '\\control_id.xml'
        arbol = ET.parse(fichero_control_id)
        cont = arbol.find("id_imagen")
        cont.text = str(id_int + 1)
        arbol.write(fichero_control_id)

    # Obtiene el  id de la plantilla actual para cada proyecto
    def obtenerIdPlantillaAtual(self):
        arbol = self.asignarFicheroParse()
        id = arbol.findtext("id_plantillaActual")
        return id

    # Asigna id de plantilla actual para cada proyecto
    def asignarIdPlantillaActual(self, id):
        arbol = self.asignarFicheroParse()
        cont = arbol.find("id_plantillaActual")
        cont.text = id
        arbol.write(".\\control\\control.xml")

    # Obtiene la ruta de la plantilla actual
    def obtenerRutaPlantillaActual(self):
        arbol = self.asignarFicheroParse()
        ruta_pl = arbol.findtext("ruta_plantillaActual")
        return ruta_pl

    # Asigna la ruta del directorio de imagenes
    def asignarRutaPlantillaActual(self, ruta):
        arbol = self.asignarFicheroParse()
        ruta_pl = arbol.find("ruta_plantillaActual")
        ruta_pl.text = ruta
        arbol.write(".\\control\\control.xml")
