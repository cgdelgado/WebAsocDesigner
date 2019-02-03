# -*- coding: utf-8 -*-
from Noticia import *
from Control_app import *

control = Control()

class ControladorNoticia(object):

    def agregarNoticia(self, titulo, descripcion, fecha):
        id_noticia = control.obtenerIdNoticia()

        noticia_nueva = Noticia(id_noticia, titulo, descripcion, fecha)

        #Guardar informacion en el xml
        noticia_nueva.guardarNoticiaXML()
        #Aumentar el contador de los id de las nociticias
        control.aumentarIdNoticia(id_noticia)

    #Obtener las noticias para pasarlas a la vista
    def mostrarNoticias(self):
        n = Noticia()
        noticias = n.listarNoticias()
        return noticias

    def actualizarNoticia(self, id, titulo, descripcion, fecha):
        noticia = Noticia(id, titulo, descripcion, fecha)
        noticia.actualizarNoticiaXML()

    def eliminarNoticia(self, id):
        noticia = Noticia()
        noticia.borrarNoticiaXML(id)

    def eliminarTodasLasNoticias(self):
        noticia = Noticia()
        noticia.borrarTodasLasNoticias()

    # Obtiene los mensajes de validacion del modelo
    def obtenerMensajesValidacion(self, titulo, descripcion):
        noticia = Noticia()
        mensajes = noticia.validar(titulo, descripcion)
        return mensajes