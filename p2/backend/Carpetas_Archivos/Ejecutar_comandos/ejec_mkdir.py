from Discos.Comandos.mount import ParticionesMontadas
from Carpetas_Archivos.Comandos.mkdir import Mkdir
from Utilidades.utilidades import printError
from General.Global import SesionActiva

def parametros_mkdir(parametros):
    sesionActiva = SesionActiva()
    partMontadas = ParticionesMontadas()
    path, r = "", False

    for elemento in parametros:
        
        partes = elemento.split("=")

        if partes[0] == "-r": 
            r = True
            continue

        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "path":
                valor = valor.replace('"', '')
                path = valor

            case "r":
                r = True

            case _:
                return f"El parametro -{parametro} no existe."

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VALIDACIONES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # VERIFICAR QUE EXISTA UNA SESION ACTIVA
    if sesionActiva.getSesion_iniciada() is None:
        return printError("No existe una sesión activa.")
    
    mParticion = partMontadas.returnPartMontada(sesionActiva.getSesion_Particion())

    # VERIFICAR QUE EXISTA LA PARTICION
    if mParticion is None:
        return printError("La particion no esta montada.")
    
    mkdir = Mkdir(path, r)

    return mkdir.crear_directorio()
 