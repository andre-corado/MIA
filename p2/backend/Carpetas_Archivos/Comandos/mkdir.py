from Sistema_archivos.funciones.crearCarpetas import crearCarpetas
from Sistema_archivos.funciones.inodo import getInodeNumberForPath
from General.Global import SesionActiva
from Utilidades.utilidades import *

class Mkdir:
    def __init__(self, path, r):
        self.path = path
        self.r = r

    def crear_directorio(self):
        sesionActiva = SesionActiva()
        particionId = sesionActiva.getSesion_Particion()

        if sesionActiva.getSesion_iniciada() is None:
            return printError("No existe una sesion iniciada.")
        
        # SE CREA LA CARPETA EN EL SISTEMA DE ARCHIVOS
        contr = 0
        
        if self.r is True:
            # SE VERIFICA QUE EXISTA CARPETA POR CARPETA EN EL SISTEMA DE ARCHIVOS
            carpetas = [elemento for elemento in self.path.split("/") if elemento != ""]
            path = ""

            if len(carpetas) == 1:
                return printError("El parametro -r solo puede ser utilizado cuando no existen las carpetas.")
            
            for i in range(len(carpetas)):
                path = path + "/" + carpetas[i]
                nInodo = getInodeNumberForPath(particionId, path)

                if nInodo is None:
                    seCreoCarpeta = crearCarpetas(particionId, path)
                    if seCreoCarpeta is True:
                        continue

                    return printError("No se pudo crear la carpeta.")
                else:
                    contr += 1

                if contr == len(carpetas) - 1:
                    return printError("Ya existe la carpeta")
            
            return printSuccess("Se creo la carpeta y su directorio correctamente!")
        
        seCreoCarpeta = crearCarpetas(particionId, self.path)
        if seCreoCarpeta is True:
            return printSuccess("Se creo la carpeta correctamente!")
        
        return printError("No se pudo crear la carpeta.")
