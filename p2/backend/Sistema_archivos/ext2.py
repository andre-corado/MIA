from Estructuras.structs_F2 import SuperBloque
from Utilidades.utilidades import *
from Utilidades.load import *

def ext2(n:int, particionMount, superBloque:SuperBloque, fecha:float):    

    # COLOCARLE EL TIPO DE SISTEMA QUE ES EL SUPERBLOQUE INCIIAL
    superBloque.fileSystem_type = 2
    superBloque.bmInode_start = particionMount["part"].part_start + TAM_SB
    superBloque.bmBlock_start = superBloque.bmInode_start + n
    superBloque.inode_start = superBloque.bmBlock_start + 3*n
    superBloque.block_start = superBloque.inode_start + n * TAM_INODO

    superBloque.inode_s = TAM_INODO
    superBloque.block_s = TAM_BLOQUE

    # SE CREA EL INODO 0 
    # SE CREE UN BLOQUE DE CARPETAS
    # SE CREA EL INODO 1 PARA EL USER TXT, ESTE INODO CREA UN BLOQUE DE ARCHIVOS
    superBloque.freeInodes_count -= 1
    superBloque.freeBlocks_count -= 1
    superBloque.freeInodes_count -= 1
    superBloque.freeBlocks_count -= 1

    archivo = open(particionMount["path"], "rb+")

    cero = b"\0"

    # LIMPIAR LA ZONA DEL BITMAP DE INODOS
    for i in range(n):
        Desplazamiento_escritura_normal(archivo, superBloque.bmInode_start + i, cero)

    # LIMPIAR LA ZONA DEL BITMAP DE BLOQUE
    for i in range(3*n):
        Desplazamiento_escritura_normal(archivo, superBloque.bmBlock_start + i, cero)

    nuevoInodo = Inodo()
    for i in range(n):
        Desplazamiento_escritura_obj(archivo, superBloque.inode_start + i * TAM_INODO, nuevoInodo)

    nuevoBloqueDeArchivos = BloquesDeArchivos()
    for i in range(3*n):
        Desplazamiento_escritura_obj(archivo, superBloque.block_start + i * TAM_BLOQUE, nuevoBloqueDeArchivos)

    # CREACION DEL INODO 0 -> "/"
    inodo0 = Inodo(0, 0, 0, fecha, fecha, fecha, [-1]*15, "0", 664)
    inodo0.block[0] = 0


    # CREACION DE BLOQUE DE CARPETAS -> ACTUAL = INODO 0 Y PADRE = INODO 0
    #   | a = 0  | 
    #   | p =  0 |     
    #   |user.txt|   
    bloqueDeCarpetas0 = BloquesDeCarpetas()
    # ACTUAL
    bloqueDeCarpetas0.b_content[0].inode = 0
    bloqueDeCarpetas0.b_content[0].name = "."
    # PADRE
    bloqueDeCarpetas0.b_content[1].inode = 0
    bloqueDeCarpetas0.b_content[1].name = ".."
    # ARCHIVO USER
    bloqueDeCarpetas0.b_content[2].inode = 1
    bloqueDeCarpetas0.b_content[2].name = "users.txt"


    # CREACION DE INODO 1 -> ALMACENA USER.TXT 
    inodo1 = Inodo(1, 1, TAM_BLOQUE, fecha, fecha, fecha, [-1]*15, "1", 664)
    inodo1.block[0] = 1 

    # ARCHIVO USERS.TXT
    data_userTXT = '1,G,root\n1,U,root,root,123\n'
    # RELLENO MI BLOQUE DE ARCHIVOS LA DATA DEL INODO 1, O SEA USER.TXT
    bloqueDeArchivos = BloquesDeArchivos()
    bloqueDeArchivos.content = data_userTXT


    # ESCRITURA EN ARCHIVO BINARIO
    Desplazamiento_escritura_obj(archivo, particionMount["part"].part_start, superBloque)
    
    # BITMAP INODO
    Desplazamiento_escritura_normal(archivo, superBloque.bmInode_start, b"\1")
    Desplazamiento_escritura_normal(archivo, superBloque.bmInode_start+1, b"\1")
    
    # BITMAP BLOQUES
    Desplazamiento_escritura_normal(archivo, superBloque.bmBlock_start, b"\1")
    Desplazamiento_escritura_normal(archivo, superBloque.bmBlock_start+1, b"\1")

    # INODOS
    Desplazamiento_escritura_obj(archivo, superBloque.inode_start, inodo0)
    Desplazamiento_escritura_obj(archivo, superBloque.inode_start + TAM_INODO, inodo1)

    # BLQUES
    Desplazamiento_escritura_obj(archivo, superBloque.block_start, bloqueDeCarpetas0)
    Desplazamiento_escritura_obj(archivo, superBloque.block_start + TAM_BLOQUE, bloqueDeArchivos)

    archivo.close()
    
    return printSuccess("Se creo el sistema de archivos EXT2 exitosamente!")
