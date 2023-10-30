from General.Global import SesionActiva
from Utilidades.utilidades import *


def parametros_logout():
    sesionActiva = SesionActiva()
    
    if sesionActiva.getSesion_iniciada() is None:
        return printError("No existe una sesión activa.")

    sesionActiva.SetSesion_iniciada(None)
    sesionActiva.SetSesion_Particion("")
    sesionActiva.SetPath_Particion("")
    return printSuccess("Sesion cerrada correctamente!")
    