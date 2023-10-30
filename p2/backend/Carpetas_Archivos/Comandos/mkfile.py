from Sistema_archivos.funciones.crearArchivos import crearArchivo
from Sistema_archivos.funciones.crearCarpetas import crearCarpetas
from Sistema_archivos.funciones.inodo import getInodeNumberForPath
from General.Global import SesionActiva
from Utilidades.utilidades import *

class Mkfile:
    def __init__(self, path, r, size, cont):
        self.path = path
        self.r = r
        self.size = size
        self.cont = cont

    def crear_archivo(self):
        sesionActiva = SesionActiva()
        particionId = sesionActiva.getSesion_Particion()

        if sesionActiva.getSesion_iniciada() is None:
            return printError("No existe una sesion iniciada.")
        
        # SE CREA LA CARPETA EN EL SISTEMA DE ARCHIVOS
        contr = 0

        if self.r is True:
            #Se verifica que exista carpeta por carpeta en el sistema de archivos
            carpetas = [elemento for elemento in self.path.split('/') if elemento != '']
            path = ''

            if len(carpetas) == 1:
                return printError("El parametro -r solo puede ser utilizado cuando no existen las carpetas.")
            
            for i in range(len(carpetas)):
                path = path + '/' + carpetas[i]
                nInodo = getInodeNumberForPath(particionId, path)

                if nInodo is None:
                    if i == len(carpetas) - 1:
                        seCreoArchivo = crearArchivo(particionId, path, self.size, self.cont)
                        if seCreoArchivo is True:
                            continue
                        
                        return printError("1. No se pudo crear el archivo.")
                    
                    seCreoCarpeta = crearCarpetas(particionId, path)
                    if seCreoCarpeta is True:
                        continue

                    return printError("No se pudo crear la carpeta.")
                
                else:
                    contr += 1

                if contr == len(carpetas) - 1:
                    break

            return printSuccess("Se creo el archivo y su directorio correctamente!")
        
        seCreoArchivo = crearArchivo(particionId, self.path, self.size, self.cont)
        if seCreoArchivo is True:
            return printSuccess("Se creo el archivo correctamente!")
        
        return printError("2. No se pudo crear el archivo.")
