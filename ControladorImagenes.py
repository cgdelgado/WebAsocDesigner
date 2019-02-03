# -*- coding: utf-8 -*-
from Imagen import *
from Control_app import *
import os

control = Control()

class ControladorImagen(object):

    def agregarImagen(self, titulo, nombre, url):

        id_imagen = control.obtenerIdImagen()
        imagen_nueva = Imagen(id_imagen, titulo, url)

        #Obtener la ruta par aalmacenar las imagenes en el directorio del proyecto
        destino = control.obtenerRutaDirImg()
        ruta_img = destino + "\\" + nombre
        msg = None
        #Controlar que exista fichero para copiar
        if len(url) > 0:
            # Si no existe el fichero en el destino, se copia
            if not os.path.basename(url) in os.listdir(destino):
                shutil.copy(url, destino)
                imagen_nueva.__setattr__("img_url", ruta_img)
                # Guardar informacion en el xml
                imagen_nueva.guardarImagenXML()
                # Aumentar el contador de los id de las imagenes
                control.aumentarIdImagen(id_imagen)

            else:
                msg = "La imagen ya existe en el directorio"

        return msg

    def mostrarImagenes(self):
        img = Imagen()
        imagenes = img.listarImagen()
        return imagenes

    def actualizarTituloImagen(self, id, titulo):
        img = Imagen()
        img.actualizarImagenXML(id, titulo)

    def eliminarImagen(self, id):

        #obtener las imagenes existentes
        imgs = self.mostrarImagenes()
        #Recorrer el array de imagenes para buscar la imagen con el id pasado por parametro
        for i in imgs:
            if id == i['id_imagen']:
                ruta = i['img_url']
                os.remove(ruta)

        img = Imagen()
        img.borrarImagenXML(id)

    def eliminarTodasLasImagenes(self):
        # obtener las imagenes existentes
        imgs = self.mostrarImagenes()
        # Recorrer el array de imagenes para buscar la imagen con el id pasado por parametro
        for i in imgs:
            ruta = i['img_url']
            os.remove(ruta)

        img = Imagen()
        img.borrarTodasLasImagenesXML()

    def obtenerMensajesValidacion(self, titulo):
        imagen = Imagen()
        mensajes = imagen.validar(titulo)
        return mensajes