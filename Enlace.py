# -*- coding: utf-8 -*-
import re
from Control_app import *
import xml.etree.ElementTree as ET

class Enlace(object):

    def __init__(self, id_enlace=None, nombre=None, url=None):
        self.id_enlace = id_enlace
        self.nombre = nombre
        self.url = url

    def obtenerFicheroXML(self):
        control = Control()
        enlace_xml = control.obtenerRutaDirRecursosDestino()
        enlace_xml = enlace_xml + "\\enlace.xml"
        return enlace_xml

    def guardarEnlaceXML(self):
        enlace_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(enlace_xml)

        id_int = int(self.__getattribute__("id_enlace"))
        if id_int == 0:
            # Si es el primer enlace que se almacena
            id_enlace = arbolXML.find("enlace/id_enlace")
            id_enlace.text = self.__getattribute__("id_enlace")
            nombre = arbolXML.find("enlace/nombre")
            nombre.text = self.__getattribute__("nombre")
            url = arbolXML.find("enlace/url")
            url.text = self.__getattribute__("url")

        else:

            # si no es el primer enlace que se almacena, crea el arbol xml agregando elementos
            enlaces = arbolXML.getroot()
            enlace_nuevo = ET.SubElement(enlaces, "enlace")

            id_actividad = ET.SubElement(enlace_nuevo, "id_enlace")
            id_actividad.text = self.__getattribute__("id_enlace")
            nombre = ET.SubElement(enlace_nuevo, "nombre")
            nombre.text = self.__getattribute__("nombre")
            url = ET.SubElement(enlace_nuevo, "url")
            url.text = self.__getattribute__("url")


        # Se guardan los cambios en el fichero correspondiente
        arbolXML.write(enlace_xml)

    # Devuelve un array de enlaces con los datos obtenidos en el XML
    def listarEnlaces(self):
        # Obtener el directorio donde se encuentran los recursos
        enlace_xml = self.obtenerFicheroXML()
        # Parsear el fichero enlace.xml
        arbolXML = ET.parse(enlace_xml)
        # Buscar los elementos enlace
        elementos_enlace = arbolXML.findall("enlace")
        enlaces = []

        # Recorrer los elementos enlace para obtener los datos y guardarlos en un array
        for e in elementos_enlace:
            id = e.find('id_enlace').text
            nombre = e.find('nombre').text
            url = e.find('url').text

            enlace = {'id_enlace': id, 'nombre': nombre, 'url': url}
            enlaces.append(enlace)

        return enlaces

    def actualizarEnlacedXML(self):
        # Obtener el fichero xml para parsearlo
        enlace_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(enlace_xml)

        # Buscar todos los enlaces
        elementos_enlace = arbolXML.findall("enlace")
        for e in elementos_enlace:
            id = e.find('id_enlace').text

            # Buscar la enlace con el id actual y asignar los nuevos datos
            if self.__getattribute__("id_enlace") == id:
                titulo = e.find('nombre')
                titulo.text = self.__getattribute__("nombre")
                url = e.find('url')
                url.text = self.__getattribute__("url")

        # Escribir en el XML para guardar los nuevo datos
        arbolXML.write(enlace_xml)

    def borrarEnlaceXML(self, id):
        enlace_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(enlace_xml)
        raiz = arbolXML.getroot()

        # Buscar todos los enlaces
        elementos_enlace = arbolXML.findall("enlace")
        for e in elementos_enlace:
            id_enlace = e.find('id_enlace').text
            # Buscar el enlace con el id actual y eliminarlo
            if id_enlace == id:
                raiz.remove(e)

        # Escribir en el XML para actualizar
        arbolXML.write(enlace_xml)

    def borrarTodosLosEnlaces(self):
        enlace_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(enlace_xml)
        raiz = arbolXML.getroot()

        elementos_enlace = arbolXML.findall("enlace")
        for e in elementos_enlace:
            raiz.remove(e)

        # Escribir en el XML para actualizar
        arbolXML.write(enlace_xml)

    def validar(self, titulo, url):
        msg = []
        if len(titulo) > 40:
            msg.append("Título demasiado largo (máx. 40)")

        if len(url) == 0:
            msg.append("Título obligatorio")

        if len(url) == 0:
            msg.append("Url obligatoria")
        elif not re.match('^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w%?=&:\.-]*)*\/?$', url):
            msg.append("Formato url no válido")

        return msg