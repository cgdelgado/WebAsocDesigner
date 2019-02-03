# -*- coding: utf-8 -*-
from Enlace import *
from Control_app import *

control = Control()

class ControladorEnlace(object):

    def agregarEnlace(self, nombre=None, url=None):
        id_enlace = control.obtenerIdEnlace()
        enlace_nuevo = Enlace(id_enlace, nombre, url)

        #Guardar informacion en el xml
        enlace_nuevo.guardarEnlaceXML()
        #Aumentar el contador de los id de los enlaces
        control.aumentarIdEnlace(id_enlace)

    #Obtener los enlaces para pasarlo a la vista
    def mostrarEnlaces(self):
        enl = Enlace()
        enlaces = enl.listarEnlaces()
        return enlaces

    def actualizarEnlace(self, id, nombre, url):
        enlace = Enlace(id, nombre, url)
        enlace.actualizarEnlacedXML()

    def eliminarEnlace(self, id):
        enlace = Enlace()
        enlace.borrarEnlaceXML(id)

    def eliminarTodosLosEnlaces(self):
        enlace = Enlace()
        enlace.borrarTodosLosEnlaces()

    def obtenerMensajesValidacion(self, titulo, url):
        enlace = Enlace()
        mensajes = enlace.validar(titulo, url)
        return mensajes