# -*- coding: utf-8 -*-
from Actividad import Actividad
from Control_app import Control

control = Control()

class ControladorActividad(object):

    def agregarActividad(self, nombre, descripcion, fecha, hora, lugar):
        id_actividad = control.obtenerIdActividad()
        actividad_nueva = Actividad(id_actividad, nombre, descripcion, fecha, hora, lugar)

        #Guardar informacion en el xml
        actividad_nueva.guardarActividadXML()
        #Aumentar el contador de los id de las actividades
        control.aumentarIdActividad(id_actividad)

    # Obtener las actividades para pasarlas a la vista
    def mostrarActividades(self):
        act = Actividad()
        actividades = act.listarActividades()
        return actividades

    def actualizarActividad(self, id, nombre, desc, fecha, hora, lugar):
        actividad = Actividad(id, nombre, desc, fecha, hora, lugar)
        actividad.actualizarActividadXML()

    def eliminarActividad(self,id):
        actividad = Actividad()
        actividad.borrarActividadXML(id)

    def eliminarTodasLasActividades(self):
        actividad = Actividad()
        actividad.borrarTodasLasActividades()

    # Obtiene los mensajes de validacion del modelo
    def obtenerMensajesValidacion(self, nombre, descripcion, lugar):
        actividad = Actividad()
        mensajes = actividad.validar(nombre, descripcion, lugar)
        return mensajes
