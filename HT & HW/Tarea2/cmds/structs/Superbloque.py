from datetime import datetime


class Superbloque:
    def __init__(self):
        self.s_filesystem_type = 0
        self.s_inodes_count = 0
        self.s_blocks_count = 0
        self.s_free_blocks_count = 0
        self.s_free_inodes_count = 0
        self.s_mtime = "00/00/0000 00:00:00"
        self.s_umtime = "00/00/0000 00:00:00"
        self.s_mnt_count = 0
        self.s_magic = 0
        self.s_inode_s = 0
        self.s_block_s = 0
        self.s_first_ino = 0
        self.s_first_blo = 0
        self.s_bm_inode_start = 0
        self.s_bm_block_start = 0
        self.s_inode_start = 0
        self.s_block_start = 0


class Inode:
    def __init__(self):
        self.i_uid = 0
        self.i_gid = 0
        self.i_s = 0
        self.i_atime = "00/00/0000 00:00:00"
        self.i_ctime = getTime()
        self.i_mtime = "00/00/0000 00:00:00"
        self.i_block = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]  # int4[15]
        self.i_type = '0'  # '0' = Carpeta, '1' = Archivo
        self.i_perm = 0  # int3

    def encode(self):
        bytes = bytearray()
        bytes += self.i_uid.to_bytes(4, byteorder='big', signed=False)
        bytes += self.i_gid.to_bytes(4, byteorder='big', signed=False)
        bytes += self.i_s.to_bytes(4, byteorder='big', signed=False)
        bytes += formatStr(self.i_atime, 16).encode()
        bytes += formatStr(self.i_ctime, 16).encode()
        bytes += formatStr(self.i_mtime, 16).encode()
        for block in self.i_block:
            bytes += block.to_bytes(4, byteorder='big', signed=True)
        bytes += self.i_type.encode()
        bytes += self.i_perm.to_bytes(3, byteorder='big', signed=False)
        return bytes

    def decode(self):
        self.i_uid = int.from_bytes(bytes[0:4], byteorder='big', signed=False)
        self.i_gid = int.from_bytes(bytes[4:8], byteorder='big', signed=False)
        self.i_s = int.from_bytes(bytes[8:12], byteorder='big', signed=False)
        self.i_atime = bytes[12:28].decode().replace('\x00', '')
        self.i_ctime = bytes[28:44].decode().replace('\x00', '')
        self.i_mtime = bytes[44:60].decode().replace('\x00', '')
        for i in range(15):
            self.i_block[i] = int.from_bytes(bytes[60 + i * 4:60 + (i + 1) * 4], byteorder='big', signed=True)
        self.i_type = bytes[120:121].decode().replace('\x00', '')
        self.i_perm = int.from_bytes(bytes[121:124], byteorder='big', signed=False)


def getTime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S").rstrip()


def formatStr(string, size):
    if len(string) < size:
        string += (size - len(string)) * '\x00'
    elif len(string) > size:
        string = string[:size]
    return string
