import struct


def execute():
    return showDiskData()


def showDiskData():
    with open("mbr.bin", "rb") as file:
        data = file.read(24)
        size, date, dsk = struct.unpack("H19sH", data)
        print("Tamaño: " + str(size) + " MB\nFecha: " + date.decode() + "\nDisco DSK SIGN: " + str(dsk) + "\n")
        file.close()
    return "Comando rep ejecutado.\n"