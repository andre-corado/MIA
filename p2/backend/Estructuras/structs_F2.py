# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SUPERBLOQUE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import datetime
import struct

class SuperBloque: # 80 Bytes
    def __init__(self, filesystem_type=-1, inodes_count=0, blocks_count=0, 
                 free_blocks_count=0, free_inodes_count=0, mtime=0, 
                 umtime=0, mnt_count=0, magic=0xEF53, 
                 inode_s=101, block_s=64, 
                 firts_ino=0, first_bio=0, bm_inode_start=-1, 
                 bm_block_start=-1, inode_start=-1, block_start=-1):
        self.fileSystem_type = filesystem_type      #  4 Bytes          
        self.inodes_count = inodes_count            #  4 Bytes
        self.blocks_count = blocks_count            #  4 Bytes
        self.freeBlocks_count = free_blocks_count   #  4 Bytes
        self.freeInodes_count = free_inodes_count   #  4 Bytes
        self.mTime = mtime                          #  8 Bytes
        self.umTime = umtime                        #  8 Bytes
        self.mnt_count = mnt_count                  #  8 Bytes
        self.magic = magic                          #  4 Bytes
        self.inode_s = inode_s                      #  4 Bytes
        self.block_s = block_s                      #  4 Bytes
        self.first_ino = firts_ino                  #  4 Bytes
        self.first_bio = first_bio                  #  4 Bytes
        self.bmInode_start = bm_inode_start         #  4 Bytes
        self.bmBlock_start = bm_block_start         #  4 Bytes
        self.inode_start = inode_start              #  4 Bytes
        self.block_start = block_start              #  4 Bytes

    def serealizar(self):
        fileS = struct.pack("i", self.fileSystem_type)
        inodesC = struct.pack("i", self.inodes_count)
        blocksC = struct.pack("i", self.blocks_count)
        freeBlocksC = struct.pack("i", self.freeBlocks_count)
        freeInodesC = struct.pack("i", self.freeInodes_count)
        mTime = struct.pack("d", self.mTime)
        umTime = struct.pack("d", self.umTime)
        mntC = struct.pack("d", self.mnt_count)
        magic = struct.pack("i", self.magic)
        inodeS = struct.pack("i", self.inode_s)
        blockS = struct.pack("i", self.block_s)
        firstI = struct.pack("i", self.first_ino)
        firstB = struct.pack("i", self.first_bio)
        bmInodeS = struct.pack("i", self.bmInode_start)
        bmBlockS = struct.pack("i", self.bmBlock_start)
        inodeStart = struct.pack("i", self.inode_start)
        blockStart = struct.pack("i", self.block_start)

        pack = fileS + inodesC + blocksC + freeBlocksC + freeInodesC + mTime + umTime + mntC + magic + inodeS + blockS + firstI + firstB + bmInodeS + bmBlockS + inodeStart + blockStart
        return pack

    @classmethod
    def deserealizar(cls, data):
        fileS = struct.unpack("i", data[:4])[0]
        inodesC = struct.unpack("i", data[4:8])[0]
        blocksC = struct.unpack("i", data[8:12])[0]
        freeInodesC = struct.unpack("i", data[12:16])[0]
        freeBlocksC = struct.unpack("i", data[16:20])[0]
        mTime = struct.unpack("d",data[20:28])[0]
        umTime = struct.unpack("d", data[28:36])[0]
        mntC = struct.unpack("d", data[36:44])[0]
        magic = struct.unpack("i",data[44:48])[0]
        inodeS = struct.unpack("i", data[48:52])[0]
        blockS = struct.unpack("i", data[52:56])[0]
        firstI = struct.unpack("i", data[56:60])[0]
        firstB = struct.unpack("i", data[60:64])[0]
        bmInodeS = struct.unpack("i", data[64:68])[0]
        bmBlockS = struct.unpack("i", data[68:72])[0]
        inodeStart = struct.unpack("i", data[72:76])[0]
        blockStart = struct.unpack("i", data[76:80])[0]
        
        return cls(fileS, inodesC, blocksC, freeBlocksC, freeInodesC, mTime, umTime, mntC, magic, inodeS, blockS, firstI, firstB, bmInodeS, bmBlockS, inodeStart, blockStart)

    def contCreacionInodo(self):
        '''MODIFICACION DE LOS CONTADORES AL CREAR UN NUEVO INODO''' 
        self.inodes_count += 1
        self.freeBlocks_count -= 1

    def contCreacionBlock(self):
        '''MODIFICACION DE LOS CONTADORES AL CREAR UN NUEVO BLOCK'''
        self.blocks_count += 1
        self.freeBlocks_count -= 1

    def graphvizBS(self):
        g = ""

        i = 2
        for atributo, valor in vars(self).items():
            if atributo == "mTime" or atributo == "umTime":
                valor = datetime.datetime.fromtimestamp(valor).strftime('%Y-%m-%d %H:%M:%S')
            
            g += f"<tr><td>{atributo}</td><td port='{str(i)}'>{str(valor)}</td></tr>\n"
            i += 1

        return g

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BLOQUE DE CARPETAS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class BloquesDeCarpetas: # 64 Bytes
    def __init__(self):
        self.b_content = [
            Content() for _ in range(4)             # 4 * 16 -> 64 Bytes
        ]

    def serealizar(self):
        content_pack = b""
        for cont in self.b_content:
            content_pack += cont.serealizar()

        return content_pack

    @classmethod
    def deserealizar(cls, data):
        content = []

        for i in range(0, len(data), 16):
            cont = Content.deserealizar(data[i:i + 16])
            content.append(cont)
   
        return list(content)
    
    def generarBloqueRep(self, n):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Bloque" + str(n) + "[label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\" port=\"0\" >Bloque "+ str(n) +"</td></tr>"
        cont = 0
        
        for content in self.b_content:
            reporte += content.generarContentRep(cont)
            cont += 1
        reporte += "</table>>];"
        
        return reporte
    

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONTENIDO DE CARPETAS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Content: # 16 Bytes
    def __init__(self, name="_", inode=-1):
        self.name = name                            # 12 Bytes
        self.inode = inode                          #  4 Bytes

    def serealizar(self):
        name = struct.pack("12s", self.name.encode())
        inode = struct.pack("i", self.inode)
        return name + inode

    @classmethod
    def deserealizar(cls, data):
        name = struct.unpack("12s", data[:12])[0].decode("utf-8").strip()
        inode = struct.unpack("i", data[12:16])[0]
        return cls(name, inode)

    def generarContentRep(self, n):
        reporte = ""
        #Se crea la etiqueta
        name = str(self.name.strip().replace("\x00", ""))
        reporte += "<tr><td>" + name + "</td><td port=\"" + str(n+1) + "\">" + str(self.inode) + "</td></tr>"
        
        return reporte
    

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> TABLA DE INODOS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class Inodo: # 101 Bytes
    def __init__(self, uid=-1, gid=-1, size=-1, atime=-1.0, ctime=-1.0, mtime=-1.0, block=[-1]*15, type_="-1", perm=-1):
        self.uid = uid                              #  4 Bytes
        self.gid = gid                              #  4 Bytes
        self.size = size                            #  4 Bytes
        self.atime = atime                          #  8 Bytes
        self.ctime = ctime                          #  8 Bytes
        self.mtime = mtime                          #  8 Bytes
        self.block = block                          # 15 * 4 ->60 Bytes
        self.type_ = type_                          #  1 Bytes
        self.perm = perm                            #  4 Bytes

    def serealizar(self):
        uid = struct.pack("i", self.uid)
        gid = struct.pack("i", self.gid)
        size = struct.pack("i", self.size)
        atime = struct.pack("d", self.atime)
        ctime = struct.pack("d", self.ctime)
        mtime = struct.pack("d", self.mtime)
        block = b"".join([struct.pack("i", block) for block in self.block])
        type_ = struct.pack("1s", self.type_.encode())
        perm = struct.pack("i", self.perm)

        return(uid + gid + size + atime + ctime + mtime + block + type_ + perm)

    @classmethod
    def deserealizar(cls, data):
        uid = struct.unpack("i", data[:4])[0]
        gid = struct.unpack("i", data[4:8])[0]
        size = struct.unpack("i", data[8:12])[0]
        atime = struct.unpack("d", data[12:20])[0]
        ctime = struct.unpack("d", data[20:28])[0]
        mtime = struct.unpack("d", data[28:36])[0]
        block = struct.unpack("15i", data[36:96])
        block = list(block)
        type_ = struct.unpack("1s", data[96:97])[0].decode("utf-8")
        perm = struct.unpack("i", data[97:101])[0]

        return cls(uid, gid, size, atime, ctime, mtime, block, type_, perm)
    
    def graphvizInode(self):
        cod = f"\t\t\t\t<tr><td>i_uid</td><td port='1'>{self.uid}</td></tr>\n"
        cod += f"\t\t\t\t<tr><td>i_gid</td><td port='2'>{self.gid}</td></tr>\n"
        cod += f"\t\t\t\t<tr><td>i_s</td><td port='3'>{self.size}</td></tr>\n"
        fecha_ = datetime.datetime.fromtimestamp(self.atime).strftime('%Y-%m-%d %H:%M:%S')
        cod += f"\t\t\t\t<tr><td>i_atime</td><td port='4'>{fecha_}</td></tr>\n"
        fecha_ = datetime.datetime.fromtimestamp(self.ctime).strftime('%Y-%m-%d %H:%M:%S')
        cod += f"\t\t\t\t<tr><td>i_ctime</td><td port='5'>{fecha_}</td></tr>\n"
        fecha_ = datetime.datetime.fromtimestamp(self.mtime).strftime('%Y-%m-%d %H:%M:%S')
        cod += f"\t\t\t\t<tr><td>i_mtime</td><td port='6'>{fecha_}</td></tr>\n"

        for a, regis in enumerate(self.block):
            cod += f"\t\t\t\t<tr><td bgcolor=\"gold\"  gradientangle=\"315\" >apt{str(a)}</td><td port='{str(a+7)}'>{str(regis)}</td></tr>\n"

        cod += f"\t\t\t\t<tr><td>i_type</td><td port='22'>{self.type_}</td></tr>\n"
        cod += f"\t\t\t\t<tr><td>i_perm</td><td port='23'>{self.perm}</td></tr>\n"

        return cod

    def generarInodoRep(self):
        reporte = "\n"
        #Se crea la etiqueta
        reporte += "\t\t\tInodo" + str(self.uid) + " [label =<\n"
        reporte += "\t\t\t<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">\n"
        reporte += "\t\t\t<tr><td colspan=\"2\" port=\"0\">Inodo " + str(self.uid) + "</td></tr>\n"

        reporte += f"\t\t\t\t<tr><td>i_uid</td><td>{self.uid}</td></tr>\n"
        reporte += f"\t\t\t\t<tr><td>i_gid</td><td>{self.gid}</td></tr>\n"
        reporte += f"\t\t\t\t<tr><td>i_s</td><td>{self.size}</td></tr>\n"
        fecha_ = datetime.datetime.fromtimestamp(self.atime).strftime('%Y-%m-%d %H:%M:%S')
        reporte += f"\t\t\t\t<tr><td>i_atime</td><td>{fecha_}</td></tr>\n"
        fecha_ = datetime.datetime.fromtimestamp(self.ctime).strftime('%Y-%m-%d %H:%M:%S')
        reporte += f"\t\t\t\t<tr><td>i_ctime</td><td>{fecha_}</td></tr>\n"
        fecha_ = datetime.datetime.fromtimestamp(self.mtime).strftime('%Y-%m-%d %H:%M:%S')
        reporte += f"\t\t\t\t<tr><td>i_mtime</td><td>{fecha_}</td></tr>\n"

        for i in range(15):
            reporte += "\t\t\t\t<tr><td>APT" + str(i+1) + "</td><td port=\"" + str(i+1) + "\">" + str(self.block[i]) + "</td></tr>\n"
            
        reporte += f"\t\t\t\t<tr><td>i_type</td><td>{self.type_}</td></tr>\n"
        reporte += f"\t\t\t\t<tr><td>i_perm</td><td>{self.perm}</td></tr>\n"

        reporte += "</table>>];\n"
        
        return reporte

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BLOQUE DE ARCHIVOS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def coding_str(string, size):  # Codificar un string a un archivo binario
    return string.encode('utf-8')[:size].ljust(size, b'\0')

class BloquesDeArchivos:
    def __init__(self, content="_"):
        self.content = content                      # 64 Bytes

    def serealizar(self):
        return struct.pack("64s", self.content.encode())
    
    @classmethod
    def deserealizar(cls, data):
        return cls(struct.unpack("64s", data[:64])[0].decode("utf-8").strip())
    
    def setContent(self, content):
        self.content = coding_str(content, 64)

    def graphvizBloqueArchivos(self):
        content = str(self.content.strip().replace("\x00", ""))
        return f"\t\t\t\t<tr><td port='1'>{content}</td></tr>\n"
    
    def generar_reporte_archivos(self, n):
        reporte = ""
        #Se crea la etiqueta
        reporte += "Bloque" + str(n) + "[label =<"
        reporte += "<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">"
        reporte += "<tr><td colspan=\"2\" port=\"0\" >Bloque Archivo "+ str(n) +"</td></tr>"
        content = str(self.content.strip().replace("\x00", ""))
        reporte += "\t\t\t\t<tr><td>"+ content +"</td></tr>"
        reporte += "</table>>];"
        return reporte


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BLOQUE DE APUNTADORES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class BloquesDeApuntadores:
    def __init__(self, pointers=[-1]*16):
        self.pointers = pointers                    # 4 * 16 -> 64 Bytes 

    def serealizar(self):
        return b"".join([struct.pack("i", punt) for punt in self.pointers])
    
    @classmethod
    def deserealizar(cls, data):
        return list(struct.unpack("16i", data[:64]))
