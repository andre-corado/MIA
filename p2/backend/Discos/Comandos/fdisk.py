from Estructuras.structs_F1 import *
from Utilidades.utilidades import *

class FDisk:
    def __init__(self, size_, path_, name_, type_):
        self.size= int(size_)
        self.name = name_
        self.unit = 'K'
        self.path = path_
        self.type = type_
        self.fit = 'WF'
        self.delete = ''
        self.add = ''

    def __particionDisp(self, mbr:MBR):
        for indice, particion in enumerate(mbr.mbr_Partitions):
            if particion.part_status == "0":
                return indice
            
        return None

    # DEVUELVE LA PARTICION CON MAYOR TAMAÑO POR SER WF
    def __aplicarFIT(self, mbr:MBR):
        tamaño_maximo = 0
        indice_particion = None

        for indice, particion in enumerate(mbr.mbr_Partitions):

            if particion.part_status in ["e", "0"] and particion.part_size > tamaño_maximo:
                tamaño_maximo = particion.part_size
                indice_particion = indice

        return indice_particion


    def crear_particion(self, mbr: MBR):

        # VERIFICAR QUE EL ESTADO SEA (0 = DISPONIBLE)
        particionDisp = self.__particionDisp(mbr)

        if particionDisp is None:
            particionDisp = self.__aplicarFIT(mbr)

            if particionDisp is not None:
                # VERIFICAR SI LA NUEVA PARTICION CABE EN LA QUE ESTABA ELIMINADA
                particionN:Particion = mbr.mbr_Partitions[particionDisp]
                if not (self.size <= particionN.part_size):
                    return printError("Espacio insuficiente para la particion.")
                
                # SI NO SOBREPASA, SE LE CAMBIA EL TAMAÑO
                mbr.mbr_Partitions[particionDisp].part_size = -1


        if particionDisp is None and self.type.lower() != "l":
            return printError("Limite de particiones alcanzado.")
                        
        # VA A ENTRAR UNICAMENTE SI EL TIPO DEL FDISK ES L DE LOGICA
        if self.type.lower() == "l":
            p_extendida = mbr.returnParticionExt()
            start_ = p_extendida.part_start
            next_ = -1

            ebrInicial = obtener_ebr(self.path, start_)
            
            # SI EL EBR INICIAL ES ESTADO 0, SIGNIFICA QUE ESTA INACTIVO ENTONCES SE LLENA
            if ebrInicial.part_status == "0":
                status_ = "1"
                fit_ = self.fit
                size_ = self.size
                next_ = -1
                name_ = self.name
                
                newEBR = EBR(status_, fit_, start_, size_, next_, name_)
                escribir_ebr(newEBR, self.path, start_)
                return printSuccess("FDISK: Partición {} lógica creada correctamente!".format(self.name))

            textSalida = self._logica(ebrInicial, start_)
            return textSalida
        

        # DEFINIR LA POSICION INICIAL DE LA PARTICION
        tam_infoMBR = 130 # Esta es la cantidad de bytes que ocupa el mbr(sin bytes de particiones)
        start = tam_infoMBR 
        index = 0

        # SI NO ES LA PRIMERA PARTICION DEL ARREGLO, SE MODIFICA EL START(PROVISIONAL)
        for particion in mbr.mbr_Partitions:
            if particion.part_size != -1:
                start = particion.part_start + particion.part_size
                index += 1
            else:
                break

        # NUEVA PARTICION CON DATOS ACTUALIZADOS
        NuevaParticion = Particion("1", self.type, self.fit, start, self.size, self.name)

        # VERIFICO SI LA PARTICION QUE SE CREO ES TIPO EXTENDIDA
        if self.type.lower() == "e":
            self._extendida(start)

        # AGREGAMOS LA NUEVA PARTICION YA CON UN VALOR
        mbr.añadir_particion(NuevaParticion, particionDisp)

        # BORRAR ESTO<<<<<<<<<<<<
        n = 1
        for p in mbr.mbr_Partitions:
            print("------DESPUES PARTICION {}------".format(str(n)))
            print("status: {}, type: {}\nfit: {}, start: {}\nsize: {}, name: {}".format(p.part_status, p.part_type, p.part_fit, str(p.part_start), str(p.part_size), p.part_name))
            n += 1
            
        # SE ESCRIBE DE NUEVO EL MBR AL DISK
        escribir_mbr(mbr, self.path)

        tipoParticion = "extendida" if self.type.lower() == "e" else  "primaria"
        return printSuccess("FDISK: Partición {} {} creada correctamente!".format(tipoParticion, self.name))

    
    def _extendida(self, start:int):
        # AL MOMENTO DE CREAR UNA EXTENDIDA, COLOCO UN EBR POR DEFECTO EN ESTADO INACTIVO
        ebrDefault = EBR("0", "_", start, -1, -1, "")
        escribir_ebr(ebrDefault, self.path, start)


    def _logica(self, ebrInicial: EBR, start_:int):
        TAM_EBR = 31 # Bytes
        start_ += ebrInicial.part_size + TAM_EBR
        next_ = -1

        EBR_actual = EBR("1", self.fit, start_, self.size, next_, self.name)

        if ebrInicial.part_next == -1:
            ebrInicial.part_next = start_

            # SE ESCRIBE EL ANTERIOR Y EL ACTUAL EBR
            escribir_ebr(ebrInicial, self.path, ebrInicial.part_start)
            escribir_ebr(EBR_actual, self.path, EBR_actual.part_start)
            return printSuccess("FDISK: Partición {} lógica creada correctamente!".format(self.name))


        mbr_anterior = obtener_ebr(self.path, start_)

        if mbr_anterior.part_next == -1:
            return self._logica(mbr_anterior, start_)
        
        return self._logica(mbr_anterior, mbr_anterior.part_start)
