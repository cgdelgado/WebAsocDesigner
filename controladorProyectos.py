# -*- coding: utf-8 -*-
import os
import shutil
import xml.etree.ElementTree as ET
import webbrowser, io
import paramiko
from Proyectos import Proyecto
from Control_app import *
from ControladorNoticias import *
from ControladorActividades import *
from ControladorImagenes import *
from ControladorEnlaces import *
from ControladorPlantillas import ControladorPlantilla
from jinja2 import Environment, FileSystemLoader, select_autoescape

control = Control()


class ControladorProyecto(object):

    def agregarSitioWeb(self, nomP, nomW, logo, res, email, tlf, dir, info, hist, jd, origenRutaImg):
        # Realizar una copia del fichero de control
        control.configurarFicheroInicial()
        proy_nuevo = Proyecto(nomP, nomW, logo, res, email, tlf, dir, info, hist, jd)

        # Configurar el proyecto en el directorio de trabajo
        msg = proy_nuevo.darDeAltaSitioWeb()

        if msg is None:
            # Obtener la ruta para almacenar la imagenes
            destino = control.obtenerRutaDirImg()
            ruta_img = destino + "\\" + logo

            # Controlar que exista fichero para copiar
            #if len(origenRutaImg) > 0:
            if os.path.isfile(origenRutaImg):
                shutil.copy(origenRutaImg, destino)
                proy_nuevo.__setattr__("logo", ruta_img)

            # Guardar informacion en el xml
            proy_nuevo.guardarProyectoXML()
            # Establecer el proyecto nuevo como proyecto actual
            control.asignarProyectoActual(nomP)
        else:
            return msg

    def consultarSitioWeb(self):
        # Obetener el proyecto cargado
        try:
            nomP = control.obtenerProyectoActual()
            p = Proyecto()
            # Buscar en el directorio de trabajo el proyecto actual para obtener el xml con la informacion
            arbolXML = p.buscarProyecto(nomP)
            # Obtener los datos del proyecto para mostrarlos
            p2 = Proyecto.obtenerDatosProyectodelXML(p, nomP, arbolXML)
            return p2
        except Exception:
            return None

    def editarSitioWeb(self, nomP, nomW, logo, res, email, tlf, dir, info, hist, jd, origenRutaImg):
        # Obetener el proyecto cargado
        nombreP = control.obtenerProyectoActual()
        p = Proyecto(nombreP, nomW, logo, res, email, tlf, dir, info, hist, jd)

        # Obtener la ruta para almacenar la imagenes
        destino = control.obtenerRutaDirImg()
        ruta_img = destino + "\\" + logo

        # Controlar que exista fichero para copiar
        if len(origenRutaImg) > 0:
            # Si no existe el fichero en el destino, se copia
            if not os.path.basename(origenRutaImg) in os.listdir(destino):
                shutil.copy(origenRutaImg, destino)

            p.__setattr__("logo", ruta_img)

        # Obtener los datos del proyecto
        p.guardarProyectoXML()

    def abrirProyecto(self, nomP, directorio):
        # Establecer nomP como proyecto actual para luego obtener los datos y configurar los directorios
        try:
            control.configurarFicheroInicial()
            control.asignarProyectoActual(nomP)
            recursos = directorio + "\\recursos"
            imgs = directorio + "\\plantillas\\img"
            control.asignarRutaDirRecusrosDestino(recursos)
            control.asignarRutaDirImg(imgs)
            controladorPlant = ControladorPlantilla()
            plantilla_actual = controladorPlant.obtenerPlantillaActual()
            if not plantilla_actual is None:
                control.asignarRutaPlantillaActual(plantilla_actual)
            else:
                control.asignarIdPlantillaActual("")
                control.asignarRutaPlantillaActual("")
            return None
        except Exception as err:
            msg = "Error: {0}".format(err)
            return msg

    # Obtiene los mensajes de validacion del modelo
    def obtenerMensajesValidacion(self, nomP, nomW, logo, res, email, tlf, dir, info, hist, jd):
        proy_nuevo = Proyecto(nomP, nomW, logo, res, email, tlf, dir, info, hist, jd)

        mensajes = proy_nuevo.validar()
        return mensajes

    # Abrir el fichero html con el contenido de la web en el navegador por defecto
    def abrirNavegador(self):
        try:
            ruta = control.obtenerRutaPlantillaActual()
            fichero = ruta + "\\index.html"
            webbrowser.open_new_tab(fichero)
            return None
        except Exception as err:
            msg = "Error: {0}".format(err)
            return msg

    # Pasa los datos del modelo a la vista HTML
    def renderizar(self):
        try:
            # Obtener los datos
            datosSitioWeb = self.consultarSitioWeb()

            cn = ControladorNoticia()
            noticias = cn.mostrarNoticias()

            ca = ControladorActividad()
            actividades = ca.mostrarActividades()

            ci = ControladorImagen()
            imagenes = ci.mostrarImagenes()
            dir_imgs = control.obtenerRutaDirImg()
            if os.path.isdir(control.obtenerRutaPlantillaActual()):
                dir_img_plant = control.obtenerRutaPlantillaActual() + "\\img"

                # Eliminar y copiar las imagenes en la carpeta de la plantilla
                shutil.rmtree(dir_img_plant)
                shutil.copytree(dir_imgs, dir_img_plant)
                logo = None

                # Si la imagen del logo existe en la carpeta de la plantilla, se asigna a logo para renderizarla
                if os.path.basename(datosSitioWeb.logo) in os.listdir(dir_img_plant):
                    logo = 'img\\' + os.path.basename(datosSitioWeb.logo)

                # Establecer la nueva ruta de las imagene para el rederizado
                if len(imagenes) > 0:
                    for i in imagenes:
                        if i['img_url'] != None and i['img_url'] != "":
                            i['img_url'] = 'img\\' + os.path.basename(i['img_url'])

                ce = ControladorEnlace()
                enlaces = ce.mostrarEnlaces()

                # Indicar la ruta donde se encuentra la plantilla HTML
                ruta = control.obtenerRutaPlantillaActual()
                rutabarra = ruta + "\\"
                ruta_nueva_plantilla = rutabarra + "index.html"
                # Cargar el entorno donde se encuentra la plantilla
                env = Environment(loader=FileSystemLoader(rutabarra), autoescape=select_autoescape(['html']))
                plantilla = env.get_template('plantilla.html')

                # Renderizar
                plant = plantilla.render(nombre=datosSitioWeb.nombre_web, resumen=datosSitioWeb.resumen, sobrenosotros=datosSitioWeb.sobrenosotros,
                                         historia=datosSitioWeb.historia, juntadir=datosSitioWeb.junta_directiva, telefono=datosSitioWeb.telefono,
                                         direccion=datosSitioWeb.direccion, email=datosSitioWeb.email, noticias=noticias, actividades=actividades,
                                         imagenes=imagenes, enlaces=enlaces, logo=logo)

                # Guardar el HTML con los datos en un fichero
                with io.open(ruta_nueva_plantilla, 'w', encoding='utf8') as f:
                    f.write(plant)
                    f.close()
                return None
            else:
                return "No existe la plantilla. Por favor, seleccione una."
        except Exception as err:
            msg = "Error: {0}".format(err)
            return msg

    # Publicar sitio web
    def publicar(self, host, user, psw, port):

        self.renderizar()
        try:
            # Indicar la ruta donde se encuentra la plantilla HTML, los ficheros css y js y las imagenes
            ruta = control.obtenerRutaPlantillaActual()
            ruta_inv = ruta.replace('\\', '/')

            rutabarra = ruta_inv + "/"
            ruta_local = rutabarra + "index.html"
            fichero_css = rutabarra + "styles.css"
            fichero_rules_css = rutabarra + "rules.css"
            fichero_js = rutabarra + "main.js"

            ruta_img_inv = control.obtenerRutaDirImg()
            ruta_img = ruta_img_inv.replace('\\', '/')

            remote = '/var/www/html/index.html'
            remote_css = '/var/www/html/styles.css'
            remote_css_rules = '/var/www/html/rules.css'
            remote_js = '/var/www/html/main.js'

            # Listar el directorio donde se encuentran las imagenes
            imgs = os.listdir(ruta_img)

            # Establecer el puerto 22 si no se recibe ninguno como parametro
            if len(port) == 0:
                puerto = 22
            else:
                puerto = int(port)

            # Conexion y transferencia de archivos con paramiko
            transport = paramiko.Transport((host, puerto))
            transport.connect(username=user, password=psw)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.chdir('/')
            sftp.put(ruta_local, remote)
            sftp.put(fichero_css, remote_css)
            sftp.put(fichero_rules_css, remote_css_rules)
            sftp.put(fichero_js, remote_js)

            # Si no existe el directorio img en el servidor, crearlo con los permisos 775 para transferir las imagenes
            list_remote = sftp.listdir('/var/www/html')
            if not 'img' in list_remote:
                # Crear directorio para almacenar las imagenes
                sftp.mkdir('/var/www/html/img', mode=775)

            # Transferir imagenes
            if len(imgs) > 0:
                for i in imgs:
                    img_local = ruta_img + "/" + i
                    img_remote = '/var/www/html/img/' + i
                    sftp.put(img_local, img_remote)

            # Cerrar conexiones
            sftp.close()
            transport.close()

            return None

        except paramiko.ssh_exception.BadHostKeyException as bhke:
            msg = "Error: {0}".format(bhke)
            return msg
        except paramiko.ssh_exception.BadAuthenticationType as bat:
            msg = "Error: {0}".format(bat)
            return msg
        except paramiko.ssh_exception.AuthenticationException as ae:
            msg = "Error: {0}".format(ae)
            return msg
        except paramiko.ssh_exception.ChannelException as ce:
            msg = "Error: {0}".format(ce)
            return msg
        except paramiko.ssh_exception.NoValidConnectionsError as nvce:
            msg = "Error: {0}".format(nvce)
            return msg
        except paramiko.ssh_exception.ProxyCommandFailure as pcf:
            msg = "Error: {0}".format(pcf)
            return msg
        except paramiko.ssh_exception.SSHException as sshe:
            msg = "Error: {0}".format(sshe)
            return msg
        except IOError as e:
            msg= "Error: {0}".format(e)
            return msg
        except Exception as e:
            msg = "Error inesperado al intentar publicar el sitio web."
            return msg

    # Consultar manual de usuario
    def consultarManualUsuario(self):
        fichero = "start plantillas\\MANUAL_USUARIO.pdf &"
        os.system(fichero)

    def validarPublicacion(self,host, usr, psw, puerto):
        msg = []
        if (len(host) == 0) or (host == None):
            msg.append("El servidor es obligatorio")

        if (len(usr) == 0) or (usr == None):
            msg.append("El usuario es obligatorio")

        if (len(psw) == 0) or (psw == None):
            msg.append("La contraseña es obligatoria")

        return msg
