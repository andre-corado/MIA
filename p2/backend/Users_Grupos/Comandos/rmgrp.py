from Users_Grupos.importaciones import *

class Rmgrp:
    def __init__(self, name):
        self.name = name


    def eliminarGrupo(self):
        sesionActiva = SesionActiva()

        # SE OBTIENE LA PARTICION QUE ESTA ACTIVA CON EL USUARIO
        particionesMontadas = ParticionesMontadas()
        particionEnUso = particionesMontadas.returnPartMontada(sesionActiva.getSesion_Particion())

        # SE BUSCA EL ARCHIVO USERS.TXT PARA EDITARLO
        inodo, seekBlock = buscarInodo(particionEnUso, "users.txt")


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ELIMINAR GRUPO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # SE OBTIENE LA INFO DE TODOS LOS BLOQUES DE ARCHIVOS DEL INODO USERS.TXT
        contenidoUsers = obtenerInfoInodo_1(particionEnUso["path"], inodo, seekBlock)

        # SEPARAR POR LINEAS CADA REGISTRO 
        registros = contenidoUsers.splitlines()
        registrosNew = list(registros)
        encontrado = False

        for i, registro in enumerate(registros):
            datos = registro.split(",")

            if datos[1] != "G": continue

            # VERIFICAR QUE EL GRUPO EXISTA
            if datos[2] == self.name and datos[0] != "0":
                encontrado = True
                # SE LE COLOCA 0 EN EL GID(ESO ES ELIMINAR UN GRUPO)
                datos[0] = "0"
                # SE MODIFICA LA COPIA QUE SE REALIZO, INCLUYENDO EL CAMBIO
                registrosNew[i] = ','.join(datos)

        if encontrado is False:
            return printError("El grupo: {}, no existe.".format(self.name))

        # SE ACTUALIZA LA CADENA DE ACUERDO AL ARRELO QUE SE RECORRIO
        nuevoContent = '\n'.join(registrosNew) + "\n"

        escribirInfoInodo_0(particionEnUso["path"], inodo, seekBlock, nuevoContent)


        return printSuccess("Grupo eliminado correctamente!")