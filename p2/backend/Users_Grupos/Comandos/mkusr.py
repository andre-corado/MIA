from Users_Grupos.importaciones import *

TAM_INODO = 101
TAM_SB = 80

class Mkusr:
    def __init__(self, user_, pass_, grp_):
        self.user = user_
        self.pass_ = pass_
        self.grp = grp_


    def __existeGrupoUser(self, registros):
        for registro in registros:
            data = registro.split(",")
        
            if data[1] != "G": continue

            grp = data[2]
            estado = data[0] # 0 ES ELIMINADO
            if grp == self.grp and estado != "0": 
                return True
            
        return False

    def crearUsuario(self):
        sesionActiva = SesionActiva()

        # SE OBTINE LA PARTICION QUE ESTA ACTIVA CON EL USUARIO
        particionesMontadas = ParticionesMontadas()
        particionEnUso = particionesMontadas.returnPartMontada(sesionActiva.getSesion_Particion())

        # SE OBTIENE EL SUPERBLOQUE
        particion:Particion = particionEnUso["part"]
        superB = Desplazamiento_lectura_obj(particionEnUso["path"], particion.part_start, TAM_SB, SuperBloque())

        # SE BUSCA EL ARCHIVO USERS.TXT PARA EDITARLO
        inodo, seekBlock = buscarInodo(particionEnUso, "users.txt")


        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ESCRITURA DE GRUPO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # SE OBTIENE LA INFO DE TODOS LOS BLOQUES DE ARCHIVOS DEL INODO USERS.TXT
        contenidoUsers = obtenerInfoInodo_1(particionEnUso["path"], inodo, seekBlock)

        # SEPARAR POR LINEAS CADA REGISTRO 
        registros = contenidoUsers.splitlines()
        indice_de_registro = 0

        for registro in registros:
            datos = registro.split(",")

            if datos[1] != "U": continue

            # VERIFICAR QUE EL GRUPO NO EXISTA
            if datos[3] == self.user and datos[2] == self.grp:
                return printError("El usuario: {}, ya existe con el grupo: {}.".format(self.user, self.grp))

            indice_de_registro = int(datos[0])

        # VERIFICAR QUE EL GRUPO DEL USUARIO EXISTA
        if self.__existeGrupoUser(registros) is False:
            return printError("No existe el grupo al cual se le quiere asignar el usuario.")

        # SE AGREGA EL USUARIO
        contenidoUsers += f"{str(indice_de_registro+1)},U,{self.grp},{self.user},{self.pass_}\n"

        # LISTA QUE ALMACENA EL INICIO DE BM_BLOCK Y EL INICIO DE INODO 
        seeks = [superB.bmBlock_start, particion.part_size]

        # SE ESCRIBE LA NUEVA CADENA CON INFO ACTUALIZADA
        escribirInfoInodo_1(particionEnUso["path"], inodo, seekBlock, contenidoUsers, seeks, superB)

        # ESCRIBIR INODO Y SUPER BLOQUE MODIFICADO
        file = open(particionEnUso["path"], "rb+")
        Desplazamiento_escritura_obj(file, superB.inode_start + TAM_INODO, inodo)
        Desplazamiento_escritura_obj(file, particion.part_start, superB)
        file.close()
        
        return printSuccess("Usuario creado correctamente!")
    