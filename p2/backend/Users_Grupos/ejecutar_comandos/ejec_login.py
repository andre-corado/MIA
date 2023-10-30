from Discos.Comandos.mount import ParticionesMontadas
from General.Global import SesionActiva
from Sistema_archivos.funciones.bloqueArchivos import obtenerInfoInodo_1
from Utilidades.load import buscarInodo
from Utilidades.utilidades import *

def __existeUser(registros, user_, pass_):
    for registro in registros:
        data = registro.split(",")

        if data[1] != "U":
            continue

        estado = data[0] # 0 SIGNIFICA ELIMADO
        usuario = data[3] 
        contras = data[4]

        if usuario == user_ and contras == pass_ and estado != "0":
            return True
        
    return False
    

def parametros_login(parametros):
    sesionActiva = SesionActiva()
    user_, pass_, id_ = "", "", ""

    for elemento in parametros:
        
        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "user":
                entrada_sin_comillas = valor.replace('"', '')
                user_ = entrada_sin_comillas
            
            case "pass":
                entrada_sin_comillas = valor.replace('"', '')
                pass_ = entrada_sin_comillas
            
            case "id":
                id_ = valor

            case _:
                return printError(f"El parametro -{parametro} no existe.")
            

    #       <<<<<<<<<<<<<<<<<<<< VALIDACIONES >>>>>>>>>>>>>>>>>>>>
    montadas = ParticionesMontadas()

    # VERIFICAR QUE EXISTE EL ID DE LA PARTICION MONTADA
    particion = montadas.returnPartMontada(id_)
    if particion is None:
        return printError("La partición con id: {}, no esta montada.".format(id_))
    
    if sesionActiva.getSesion_iniciada() is not None:
        return printError("Ya existe una sesión iniciada.")

    sesionActiva.SetSesion_Particion(particion["id"])

    # VERIFICACION DE LOGIN
    try:
        inodo, seekBlock = buscarInodo(particion, "users.txt")
    except Exception:
        return printError("Verifique si existe un sistema de archivos.")

    # OBTENGO EN UNA CADENA TODO LO DEL INODO USERS.TXT
    contenidoBloque = obtenerInfoInodo_1(particion["path"], inodo, seekBlock)

    # SEPARAR POR LINEAS CADA REGISTRO
    registros = contenidoBloque.splitlines()

    if __existeUser(registros, user_, pass_) is False:
        return printError("Revise sus credenciales.")

    sesionActiva.SetSesion_iniciada(user_)
    sesionActiva.SetPath_Particion(particion["path"])

    return printSuccess("Logueado correctamente!")
