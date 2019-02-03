# -*- coding: utf-8 -*-
import re

from Control_app import *
import xml.etree.ElementTree as ET

class Imagen(object):

    def __init__(self, id_imagen=None, img_titulo=None, img_url=None):
        self.id_imagen = id_imagen
        self.img_titulo = img_titulo
        self.img_url = img_url

    def obtenerFicheroXML(self):
        control = Control()
        imagen_xml = control.obtenerRutaDirRecursosDestino()
        imagen_xml = imagen_xml + "\\imagen.xml"
        return imagen_xml

    def guardarImagenXML(self):
        imagen_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(imagen_xml)

        id_int = int(self.__getattribute__("id_imagen"))

        if id_int == 0:
            # Si es la primera imagen que se almacena
            id_imagen = arbolXML.find("imagen/id_imagen")
            id_imagen.text = self.__getattribute__("id_imagen")
            titulo = arbolXML.find("imagen/img_titulo")
            titulo.text = self.__getattribute__("img_titulo")
            url = arbolXML.find("imagen/img_url")
            url.text = self.__getattribute__("img_url")

        else:
            # si no es la primera imagen que se almacena, crea el arbol xml agregando elementos
            imagenes = arbolXML.getroot()
            imagen_nueva = ET.SubElement(imagenes, "imagen")

            id_actividad = ET.SubElement(imagen_nueva, "id_imagen")
            id_actividad.text = self.__getattribute__("id_imagen")
            titulo = ET.SubElement(imagen_nueva, "img_titulo")
            titulo.text = self.__getattribute__("img_titulo")
            url = ET.SubElement(imagen_nueva, "img_url")
            url.text = self.__getattribute__("img_url")

        # Se guardan los cambios en el fichero correspondiente
        arbolXML.write(imagen_xml)

    def listarImagen(self):
        # Obtener el directorio donde se encuentran los recursos
        imagen_xml = self.obtenerFicheroXML()
        # Parsear el fichero imagen.xml
        arbolXML = ET.parse(imagen_xml)
        # Buscar los elementos imagen
        elementos_imagen = arbolXML.findall("imagen")
        imagenes = []

        # Recorrer los elementos imagen para obtener los datos y guardarlos en un array
        for i in elementos_imagen:
            id = i.find('id_imagen').text
            titulo = i.find('img_titulo').text
            url = i.find('img_url').text

            imagen = {'id_imagen': id, 'img_titulo': titulo, 'img_url': url}
            imagenes.append(imagen)

        return imagenes

    def actualizarImagenXML(self, id, titulo):

        # Obtener el fichero xml para parsearlo
        imagen_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(imagen_xml)

        # Buscar todos las imagenes
        elementos_imagen = arbolXML.findall("imagen")
        for i in elementos_imagen:
            id_img = i.find('id_imagen').text

            # Buscar la imagen con el id actual y asignar los nuevos datos
            if id_img == id:
                titulo_img = i.find('img_titulo')
                titulo_img.text = titulo

        # Escribir en el XML para guardar los nuevo datos
        arbolXML.write(imagen_xml)

    def borrarImagenXML(self, id):
        imagen_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(imagen_xml)
        raiz = arbolXML.getroot()

        # Buscar todas las imagenes
        elementos_img = arbolXML.findall("imagen")
        for i in elementos_img:
            id_imagen = i.find('id_imagen').text
            # Buscar la imagen con el id actual y la elimina
            if id_imagen == id:
                raiz.remove(i)

        # Escribir en el XML para actualizar
        arbolXML.write(imagen_xml)

    def borrarTodasLasImagenesXML(self):
        imagen_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(imagen_xml)
        raiz = arbolXML.getroot()

        elementos_imagen = arbolXML.findall("imagen")
        for i in elementos_imagen:
            raiz.remove(i)

        # Escribir en el XML para actualizar
        arbolXML.write(imagen_xml)

    def validar(self, titulo):
        msg = []
        if len(titulo) > 50:
            msg.append("Nombre demasiado largo (máx. 50)")

        return msg