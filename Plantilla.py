# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from Control_app import Control


class Plantilla(object):

    def __init__(self, bg_color_seccion=None, h_color=None, p_color_section=None, p_color_body=None, name_website_color=None, h_tipoFuente=None, p_tipoFuente=None):

        self.bg_color_seccion = bg_color_seccion
        self.h_color = h_color
        self.p_color_section = p_color_section
        self.p_color_body = p_color_body
        self.name_website_color = name_website_color
        self.h_tipoFuente = h_tipoFuente
        self.p_tipoFuente = p_tipoFuente

    def obtenerFicheroXML(self):
        control = Control()
        estilo_xml = control.obtenerRutaDirRecursosDestino()
        estilo_xml = estilo_xml + "\\estilo.xml"
        return estilo_xml

    def guardarValoresOriginalesXML(self):
        estilo_xml = self.obtenerFicheroXML()
        arbolXML = ET.parse(estilo_xml)

        # Guardar los datos originales del estilo de la plantilla por si se quieren recuperar
        bg_color_seccion = arbolXML.find("bg_color_seccion")
        bg_color_seccion.text = self.__getattribute__("bg_color_seccion")
        h_color = arbolXML.find("h_color")
        h_color.text = self.__getattribute__("h_color")
        p_color_section = arbolXML.find("p_color_section")
        p_color_section.text = self.__getattribute__("p_color_section")
        p_color_body = arbolXML.find("p_color_body")
        p_color_body.text = self.__getattribute__("p_color_body")
        name_website_color = arbolXML.find("name_website_color")
        name_website_color.text = self.__getattribute__("name_website_color")
        h_tipoFuente = arbolXML.find("h_tipoFuente")
        h_tipoFuente.text = self.__getattribute__("h_tipoFuente")
        p_tipoFuente = arbolXML.find("p_tipoFuente")
        p_tipoFuente.text = self.__getattribute__("p_tipoFuente")

        # Se guardan los cambios en el fichero correspondiente
        arbolXML.write(estilo_xml)

    def obtenerValoresXML(self):
        # Obtener el directorio donde se encuentran los recursos
        estilo_xml = self.obtenerFicheroXML()
        # Parsear el fichero estilo.xml
        arbolXML = ET.parse(estilo_xml)

        # Buscar los elementos
        bg_color_seccion = arbolXML.findtext('bg_color_seccion')
        h_color = arbolXML.findtext('h_color')
        p_color_section = arbolXML.findtext('p_color_section')
        p_color_body = arbolXML.findtext('p_color_body')
        name_website_color = arbolXML.findtext('name_website_color')
        h_tipoFuente = arbolXML.findtext('h_tipoFuente')
        p_tipoFuente = arbolXML.findtext('p_tipoFuente')

        plantilla = Plantilla(bg_color_seccion,h_color,p_color_section,p_color_body,name_website_color,h_tipoFuente,p_tipoFuente)
        return plantilla