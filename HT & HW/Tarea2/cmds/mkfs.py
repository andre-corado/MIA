from cmds.structs.MBR import MBR, Partition, EBR, readMBR

EBR = 30
BLOCK = 64
SUPERBLOCK = 89
INODE = 128

T=307180,\:S=89,\:I=128,\:B=64

def execute(consoleLine):
    id = ''
    type = 'FULL'
    fs = '2FS'

    # Buscar parametros
    for i in range(1, len(consoleLine)):
        if consoleLine[i].startswith("-id="):
            id = consoleLine[i][4:]
            from cmds.mount import isMounted
            if not isMounted(id):
                return 'Error: No existe partición montada con ese id.'
        if consoleLine[i].startswith("-type="):
            type = consoleLine[i][6:].upper()
            if type != 'FULL':
                return 'Error: Type no válido.'
        if consoleLine[i].startswith("-fs="):
            fs = consoleLine[i][4:].upper()
            if fs != '2FS' and fs != '3FS':
                return 'Error: FS no válido.'

    if fs == '2FS':
        return format2FS(id)
    elif fs == '3FS':
        return format2FS(id)  # TODO: Cambiar a 3FS


def format2FS(id):
    # Obtener partición
    from cmds.mount import getMountedPartition
    mountedPart = getMountedPartition(id)
    # Obtener MBR
    mbr = readMBR(mountedPart.path)
    if mbr == None:
        return 'Error: No se pudo leer el disco.'
    # Obtener partición
    partition, type = mbr.getPartitionNamed(mountedPart.name, mountedPart.path)
    # Cálculo de n cantidad de bloques
    print("Calculando cantidad de bloques e inodos...")
    n = float((partition.part_s - SUPERBLOCK) / (INODE + 3 * BLOCK + 4)).__floor__()
    print("Cantidad de Inodos: " + str(n) + "\tCantidad de Bloques: " + str(n * 3))

    # Crear Superbloque
    from cmds.structs.Superbloque import Superbloque
    superblock = Superbloque()
    superblock.s_filesystem_type = 0
    superblock.s_inodes_count = n
    superblock.s_blocks_count = n * 3



    return 'Se formateó la partición:  ' + id + ' correctamente.'
