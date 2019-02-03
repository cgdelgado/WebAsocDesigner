# -*- coding: utf-8 -*-
import shutil
import xml.etree.ElementTree as ET
from Control_app import *
import os
import re
control = Control()


class Proyecto(object):

    def __init__(self, nombre_proyecto=None, nombre_web=None, logo=None, resumen=None, email=None, telefono=None, direccion=None, sobrenosotros=None,
                 historia=None, junta_directiva=None):
       
        self.nombre_proyecto = nombre_proyecto
        self.nombre_web = nombre_web
        self.logo = logo
        self.resumen = resumen
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.sobrenosotros = sobrenosotros
        self.historia = historia
        self.junta_directiva = junta_directiva

    # Modifica el fichero xml, almacenando los valores obtenidos en el formulario
    def guardarProyectoXML(self):
        proyecto_xml = control.obtenerRutaDirRecursosDestino()
        proyecto_xml = proyecto_xml + "\\proyecto.xml"
        arbolXML = ET.parse(proyecto_xml)

        # Accede al elemento en XML y lo almacena en variable correspondiente y añade el valor obtenido
        nom_p = arbolXML.find("nombre_proyecto")
        nom_p.text = self.__getattribute__("nombre_proyecto")
        nom_w = arbolXML.find("nombre_web")
        nom_w.text = self.__getattribute__("nombre_web")
        logo = arbolXML.find("logo")
        logo.text = self.__getattribute__("logo")
        res = arbolXML.find("resumen")
        res.text = self.__getattribute__("resumen")
        mail = arbolXML.find("email")
        mail.text = self.__getattribute__("email")
        tel = arbolXML.find("telefono")
        tel.text = self.__getattribute__("telefono")
        direcc = arbolXML.find("direccion")
        direcc.text = self.__getattribute__("direccion")
        sn = arbolXML.find("sobrenosotros")
        sn.text = self.__getattribute__("sobrenosotros")
        hist = arbolXML.find("historia")
        hist.text = self.__getattribute__("historia")

        # Se almacenan los valores del array junta_directiva creando un nuevo elemento para nombre del array
        junta_d = arbolXML.find("junta_directiva")
        elems_nombre = arbolXML.findall("junta_directiva/nombre")

        # Si existen subelementos, se eliminan y se vuelven a crear mas adelante si se introducen datos en junta directiva
        if len(elems_nombre) > 0:
            for elem in elems_nombre:
                ET.Element.remove(junta_d, elem)

        for i in range(len(self.junta_directiva)):
            n = ET.SubElement(junta_d, "nombre")
            n.text = self.junta_directiva[i]

        # Guardar los cambios en el fichero correcpondente
        arbolXML.write(proyecto_xml)

    def darDeAltaSitioWeb(self):
        # Ruta establecida por el usuario en la instalacion
        destinoWS = control.obtenerWorkspace()

        # Ruta del workspace y el nombre del proyecto
        ruta_DIR_proyecto = destinoWS + "\\" + self.nombre_proyecto

        try:
            # Crear el directorio en el workspace
            os.mkdir(ruta_DIR_proyecto)

            # Agregar el directorio de plantillas en el directorio del proyecto
            plantillas = ruta_DIR_proyecto + "\\plantillas"
            os.mkdir(plantillas)
            imgs = plantillas + "\\img"
            os.mkdir(imgs)

            # Copiar los xml donde se almacena la informacion
            recursosOrigen = control.obtenerRutaDirRecursos()
            recursosDestino = ruta_DIR_proyecto + "\\recursos"
            shutil.copytree(recursosOrigen, recursosDestino)
            control.asignarRutaDirRecusrosDestino(recursosDestino)
            control.asignarRutaDirImg(imgs)
            return None

        except Exception as err:
            msg = "Error: {0}".format(err)
            return msg

    # Busca el proyecto en el directorio del Workspace y devuelve el arbol del fichero xml con los datos del proyecto
    def buscarProyecto(self, nombre):
        directorio = control.obtenerWorkspace() + "\\" + nombre
        #Si existe el directorio
        if os.path.isdir(directorio):
            proyecto_xml = control.obtenerRutaDirRecursosDestino()
            proyecto_xml = proyecto_xml + "\\proyecto.xml"
            arbolXML = ET.parse(proyecto_xml)
            return arbolXML

    # Obtiene los datos del fichero donde esta almacenada la infomacion y crea el objeto
    def obtenerDatosProyectodelXML(self,nombre,arbol):
        nom_p = arbol.findtext("nombre_proyecto")

        # si el nombre del proyecto pasado es igual al nombre del proyecto
        if nom_p == nombre:
            nom_w = arbol.findtext("nombre_web")
            logo = arbol.findtext("logo")
            res = arbol.findtext("resumen")
            mail = arbol.findtext("email")
            tlf = arbol.findtext("telefono")
            dir = arbol.findtext("direccion")
            nos = arbol.findtext("sobrenosotros")
            hist = arbol.findtext("historia")

            # obtener el array de nombres de la junta directiva
            jd = []
            nombres_jd = arbol.findall("junta_directiva/nombre")
            for n in nombres_jd:
                jd.append(n.text)

        self.__setattr__("nombre_proyecto", nom_p)
        self.__setattr__("nombre_web", nom_w)
        self.__setattr__("logo", logo)
        self.__setattr__("resumen", res)
        self.__setattr__("email", mail)
        self.__setattr__("telefono", tlf)
        self.__setattr__("direccion", dir)
        self.__setattr__("sobrenosotros", nos)
        self.__setattr__("historia", hist)
        self.__setattr__("junta_directiva", jd)

        return self

    # Validacion de datos
    def validar(self):
        msg = []
        if len(self.nombre_proyecto) > 30:
            msg.append("Nombre del proyecto demasiado largo (máx. 30)")

        if not re.match('^([a-zA-Z0-9]+[\_\-]?[a-zA-Z0-9]*){3,30}', self.nombre_proyecto):
            msg.append("Formato del nombre del proyecto incorrecto")

        if len(self.nombre_web) > 40:
            msg.append("Nombre del sitio web demasiado largo (máx. 40)")

        if len(self.telefono) > 20:
                msg.append("Teléfono: máx 20 caracteres")

        if len(self.email) > 0:
            if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', self.email):
                msg.append("Dirección de correo no válida")

        if len(self.resumen) > 200:
            msg.append("Resumen demasiado largo")

        if len(self.direccion) > 100:
            msg.append("Dirección demasiado larga")

        for n in self.junta_directiva:
            if (len(n) < 3) or (len(n) > 50):
                msg.append("Nombre directivo demasiado largo: " + n)

        if len(self.sobrenosotros) > 5000:
            msg.append("Texto demasiado largo")

        if len(self.historia) > 8000:
            msg.append("Texto demasiado largo")

        return msg