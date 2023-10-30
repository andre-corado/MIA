from Discos.Comandos.mount import ParticionesMontadas
from Estructuras.structs_F2 import SuperBloque
from Utilidades.load import calculate_n
from Sistema_archivos.ext2 import ext2
from Estructuras.structs_F1 import *
from Utilidades.utilidades import *
import time

def parametros_mkfs(parametros):
    id, type = "", ""

    for elemento in parametros:
        
        partes = elemento.split("=")
        # SI SU LONGITUD NO ES 2 NI EMPIEZA CON EL CARACTER -, SIGUE OTRA ITERACION
        if not(len(partes) == 2 and partes[0].startswith("-")):
            continue

        parametro = partes[0][1:]  # Eliminamos el "-"
        valor = partes[1]

        match parametro.lower():
            case "id":
                id = str(valor)

            case "type":
                type = valor

    # VERIFICAR QUE LA PARTICION ESTE MONTADA
    montadas = ParticionesMontadas()
    if not montadas.buscarParticion(id):
        return printError("La particion {}, no esta montada.".format(id))


    # CREACION DE SUPERBLOQUE(POR PRIMERA VEZ)

    # CALCULOS
    particionMount = montadas.returnPartMontada(id)
    particion:Particion = particionMount["part"]

    # CALCULAR LA CANTIDAD DE ESTRUCTURAS
    n = calculate_n(particion.part_size)

    # CREACION DE SUPER BLOQUE
    nuevo_superBloque = SuperBloque()

    # ASINACION DE VALORES A CADA ATRIBUTO DEL SUPER BLOQUE
    nuevo_superBloque.freeBlocks_count = 3 * n
    nuevo_superBloque.freeInodes_count = n
    date = time.time()
    nuevo_superBloque.mTime = date
    nuevo_superBloque.umTime = date
    nuevo_superBloque.mnt_count = 1

    return ext2(n, particionMount, nuevo_superBloque, date)
