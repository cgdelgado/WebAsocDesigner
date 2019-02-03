# -*- coding: utf-8 -*-
import re
from Control_app import *
import xml.etree.ElementTree as ET

class Actividad(object):

    def __init__(self, id_actividad=None, nombre=None, descripcion=None, fecha=None, hora=None, lugar=None):
        self.id_actividad = id_actividad
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha
        self.hora = hora
        self.lugar = lugar

    def obtenerFicheroXML(self):
        control = Control()
        actividad_xml = control.obtenerRutaDirRecursosDestino()
        actividad_xml = actividad_xml + "\\actividad.xml"
        return actividad_xml

    def guardarActividadXML(self):
        actividad_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(actividad_xml)

        id_int = int(self.__getattribute__("id_actividad"))
        if id_int == 0:
            # Si es la primera actividad que se almacena
            id_actividad = arbolXML.find("actividad/id_actividad")
            id_actividad.text = self.__getattribute__("id_actividad")
            nombre = arbolXML.find("actividad/nombre")
            nombre.text = self.__getattribute__("nombre")
            descripcion = arbolXML.find("actividad/descripcion")
            descripcion.text = self.__getattribute__("descripcion")
            fecha = arbolXML.find("actividad/fecha")
            fecha.text = self.__getattribute__("fecha")
            hora = arbolXML.find("actividad/hora")
            hora.text = self.__getattribute__("hora")
            lugar = arbolXML.find("actividad/lugar")
            lugar.text = self.__getattribute__("lugar")
        else:

            # si no es la primera actividad que se almacena, crea el arbol xml agregando elementos
            actividades = arbolXML.getroot()
            actividad_nueva = ET.SubElement(actividades, "actividad")

            id_actividad = ET.SubElement(actividad_nueva, "id_actividad")
            id_actividad.text = self.__getattribute__("id_actividad")
            nombre = ET.SubElement(actividad_nueva, "nombre")
            nombre.text = self.__getattribute__("nombre")
            descripcion = ET.SubElement(actividad_nueva, "descripcion")
            descripcion.text = self.__getattribute__("descripcion")
            fecha = ET.SubElement(actividad_nueva, "fecha")
            fecha.text = self.__getattribute__("fecha")
            hora = ET.SubElement(actividad_nueva, "hora")
            hora.text = self.__getattribute__("hora")
            lugar = ET.SubElement(actividad_nueva, "lugar")
            lugar.text = self.__getattribute__("lugar")

        # Se guardan los cambios en el fichero correspondiente
        arbolXML.write(actividad_xml)

    #Devuelve un array de actividades con los datos obtenidos en el XML
    def listarActividades(self):
        #Obtener el directorio donde se encuentran los recursos
        actividad_xml = self.obtenerFicheroXML()
        #Parsear el fichero actividad.xml
        arbolXML = ET.parse(actividad_xml)
        #Buscar los elementos actividad
        elementos_actividad = arbolXML.findall("actividad")
        actividades = []

        #Recorrer los elementos actividad para obtener los datos y guardarlos en un array
        for a in elementos_actividad:
            id = a.find('id_actividad').text
            nombre = a.find('nombre').text
            desc = a.find('descripcion').text
            fecha = a.find('fecha').text
            hora = a.find('hora').text
            lugar = a.find('lugar').text
            actividad = {'id_actividad': id, 'nombre': nombre, 'descripcion': desc, 'fecha': fecha, 'hora':hora, 'lugar':lugar}
            actividades.append(actividad)

        return actividades

    def actualizarActividadXML(self):
        # Obtener el fichero xml para parsearlo
        actividad_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(actividad_xml)

        # Buscar todas las actividades
        elementos_actividad = arbolXML.findall("actividad")
        for a in elementos_actividad:
            id = a.find('id_actividad').text

            # Buscar la actividad con el id actual y asignar los nuevos datos
            if self.__getattribute__("id_actividad") == id:
                titulo = a.find('nombre')
                titulo.text = self.__getattribute__("nombre")
                desc = a.find('descripcion')
                desc.text = self.__getattribute__("descripcion")
                fecha = a.find('fecha')
                fecha.text = self.__getattribute__("fecha")
                hora = a.find('hora')
                hora.text = self.__getattribute__("hora")
                lugar = a.find('lugar')
                lugar.text = self.__getattribute__("lugar")

        # Escribir en el XML para guardar los nuevo datos
        arbolXML.write(actividad_xml)

    def borrarActividadXML(self, id):
        actividad_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(actividad_xml)
        raiz = arbolXML.getroot()

        # Buscar todas las actividades
        elementos_actividad = arbolXML.findall("actividad")
        for a in elementos_actividad:
            id_actividad = a.find('id_actividad').text
            # Buscar la actividad con el id actual y eliminarla
            if id_actividad == id:
                raiz.remove(a)

        # Escribir en el XML para actualizar
        arbolXML.write(actividad_xml)

    def borrarTodasLasActividades(self):
        actividad_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(actividad_xml)
        raiz = arbolXML.getroot()

        elemento_noticias = arbolXML.findall("actividad")
        for a in elemento_noticias:
            raiz.remove(a)

        # Escribir en el XML para actualizar
        arbolXML.write(actividad_xml)

    def validar(self, nombre, descripcion, lugar):
        msg = []
        if len(nombre) == 0 and len(descripcion) == 0 and len(lugar) == 0:
            msg.append("No hay contenido para añadir")

        if len(nombre) > 50:
            msg.append("Nombre demasiado largo (máx. 50)")

        if len(descripcion) > 500:
            msg.append("Descripción demasiado extensa")

        if len(lugar) > 100:
            msg.append("Lugar demasiado extenso")

        return msg