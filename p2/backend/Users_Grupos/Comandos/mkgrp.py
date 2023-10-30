from Users_Grupos.importaciones import *

TAM_INODO = 101
TAM_SB = 80

class Mkgrp:
    def __init__(self, name):
        self.name = name 

    def crearGrupo(self):
        sesionActiva = SesionActiva()

        # SE OBTIENE LA PARTICION QUE ESTA ACTIVA CON EL USUARIO
        particionesMontadas = ParticionesMontadas()
        particionEnUso = particionesMontadas.returnPartMontada(sesionActiva.getSesion_Particion())

        # SE OBTIENE EL SUPERBLOQUE
        particion:Particion = particionEnUso["part"]
        superB = Desplazamiento_lectura_obj(particionEnUso["path"], particion.part_start, TAM_SB, SuperBloque())

        # SE BUSCA EL ARCHIVO USERS.TXT PARA EDITARLO
        inodo, seekBlock = buscarInodo(particionEnUso, "users.txt")


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ESCcontenidoUsersRITURA DE GRUPO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # SE OBTIENE LA INFO DE TODOS LOS BLOQUES DE ARCHIVOS DEL INODO USERS.TXT
        contenidoGrupos = obtenerInfoInodo_1(particionEnUso["path"], inodo, seekBlock)

        # SEPARAR POR LINEAS CADA REGISTRO 
        registros = contenidoGrupos.splitlines()
        indice_de_registro = 0

        for registro in registros:
            datos = registro.split(",")

            if datos[1] != "G": continue

            # VERIFICAR QUE EL GRUPO NO EXISTA
            if datos[2] == self.name:
                return printError("El grupo {} ya existe.".format(self.name))

            indice_de_registro = int(datos[0])

        # SE AGREGA EL GRUPO
        contenidoGrupos += f"{str(indice_de_registro+1)},G,{self.name}\n"

        # LISTA QUE ALMACENA EL INICIO DE BM_BLOCK Y EL INICIO DE LA PARTICION 
        seeks = [superB.bmBlock_start, particion.part_size]

        # SE ESCRIBE LA NUEVA CADENA CON INFO ACTUALIZADA
        escribirInfoInodo_1(particionEnUso["path"], inodo, seekBlock, contenidoGrupos, seeks, superB)

        # ESCRIBIR INODO Y SUPER BLOQUE MODIFICADO
        file = open(particionEnUso["path"], "rb+")
        Desplazamiento_escritura_obj(file, superB.inode_start + TAM_INODO, inodo)
        Desplazamiento_escritura_obj(file, particion.part_start, superB)
        file.close()


        return printSuccess("Grupo creado correctamente!")
    