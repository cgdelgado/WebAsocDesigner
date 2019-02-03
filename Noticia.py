# -*- coding: utf-8 -*-
from Control_app import *
import xml.etree.ElementTree as ET

class Noticia(object):

    def __init__(self, id_noticia = None, titulo=None, descripcion=None, fecha=None):
        self.id_noticia =id_noticia
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha

    def obtenerFicheroXML(self):
        control = Control()
        noticia_xml = control.obtenerRutaDirRecursosDestino()
        noticia_xml = noticia_xml + "\\noticia.xml"
        return noticia_xml

    def guardarNoticiaXML(self):

        noticia_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(noticia_xml)

        id_int = int(self.__getattribute__("id_noticia"))

        if id_int == 0:
            # Si es la primera noticia que se almacena
            id_noticia = arbolXML.find("noticia/id_noticia")
            id_noticia.text = self.__getattribute__("id_noticia")
            titulo = arbolXML.find("noticia/titulo")
            titulo.text = self.__getattribute__("titulo")
            descripcion = arbolXML.find("noticia/descripcion")
            descripcion.text = self.__getattribute__("descripcion")
            fecha = arbolXML.find("noticia/fecha")
            fecha.text = self.__getattribute__("fecha")
        else:

            # si no es la primera noticia que se almacena, crea el arbol xml agregando elementos
            noticias = arbolXML.getroot()
            noticia_nueva = ET.SubElement(noticias, "noticia")

            id_noticia = ET.SubElement(noticia_nueva, "id_noticia")
            id_noticia.text = self.__getattribute__("id_noticia")
            titulo = ET.SubElement(noticia_nueva, "titulo")
            titulo.text = self.__getattribute__("titulo")
            descripcion = ET.SubElement(noticia_nueva, "descripcion")
            descripcion.text = self.__getattribute__("descripcion")
            fecha = ET.SubElement(noticia_nueva, "fecha")
            fecha.text = self.__getattribute__("fecha")

        # Se guardan los cambios en el fichero correspondiente
        arbolXML.write(noticia_xml)

    #Devuelve un array de noticias con los datos obtenidos en el XML
    def listarNoticias(self):

        #Obtener el directorio donde se encuentran los recursos
        noticia_xml = self.obtenerFicheroXML()
        #Parsear el fichero noticias.xml
        arbolXML = ET.parse(noticia_xml)
        #Buscar los elementos noticia
        elemento_noticias = arbolXML.findall("noticia")
        noticias = []

        #Recorrer los elementos noticia para obtener los datos y guardarlos en un array
        for n in elemento_noticias:
            id = n.find('id_noticia').text
            titulo = n.find('titulo').text
            desc = n.find('descripcion').text
            fecha = n.find('fecha').text
            noticia = {'id_noticia':id, 'titulo':titulo, 'descripcion':desc, 'fecha':fecha}
            noticias.append(noticia)

        return noticias

    def actualizarNoticiaXML(self):
        #Obtener el fichero xml para parsearlo
        noticia_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(noticia_xml)

        #Buscar todas las nocticias
        elemento_noticias = arbolXML.findall("noticia")
        for n in elemento_noticias:
            id = n.find('id_noticia').text

            #Buscar la noticia con el id actual y asignar los nuevos datos
            if self.__getattribute__("id_noticia") == id:
                titulo = n.find('titulo')
                titulo.text = self.__getattribute__("titulo")
                desc = n.find('descripcion')
                desc.text = self.__getattribute__("descripcion")
                fecha = n.find('fecha')
                fecha.text = self.__getattribute__("fecha")

        #Escribir en el XML para guardar los nuevo datos
        arbolXML.write(noticia_xml)

    def borrarNoticiaXML(self, id):
        noticia_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(noticia_xml)
        raiz = arbolXML.getroot()

        # Buscar todas las nocticias
        elemento_noticias = arbolXML.findall("noticia")
        for n in elemento_noticias:
            id_noticia = n.find('id_noticia').text

            # Buscar la noticia con el id actual y eliminarla
            if id_noticia == id:
                raiz.remove(n)

        # Escribir en el XML para actualizar
        arbolXML.write(noticia_xml)

    def borrarTodasLasNoticias(self):
        noticia_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(noticia_xml)
        raiz = arbolXML.getroot()

        elemento_noticias = arbolXML.findall("noticia")
        for n in elemento_noticias:
            raiz.remove(n)

        # Escribir en el XML para actualizar
        arbolXML.write(noticia_xml)

    def validar(self, titulo, descripcion):
        msg = []

        if (len(titulo) == 0) and (len(descripcion) == 0):
            msg.append("No hay contenido para añadir una noticia")

        if len(titulo) > 100:
            msg.append("Título demasiado largo (máx. 50)")

        if len(descripcion) > 5000:
            msg.append("Contenido demasiado extenso")

        return msg