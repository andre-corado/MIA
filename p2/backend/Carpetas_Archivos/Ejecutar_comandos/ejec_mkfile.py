from Carpetas_Archivos.Comandos.mkfile import Mkfile
from Discos.Comandos.mount import ParticionesMontadas
from Utilidades.utilidades import printError
from General.Global import SesionActiva

def parametros_mkfile(parametros):
    sesionActiva = SesionActiva()
    partMontadas = ParticionesMontadas()
    path, r, size, cont = "", False, 1, ""

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

            case "size":
                try:
                    size = int(valor)
                except Exception as e:
                    return printError("El size debe ser un numero entero.")

            case "cont":
                cont = valor.replace('"', '')

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
    
    # VERIFICAR EL PATH
    if path == "":
        return printError("El parametro path es obligatorio.")
    
    # VERIFICAR QUE EL SIZE SEA MAYOR A 0
    if size < 0:
        return printError("El parametro size debe ser mayor a 0.")
    
    mkfile = Mkfile(path, r, size, cont)

    return mkfile.crear_archivo()
