from cmds import mkdisk, fdisk, rmdisk, rep # Importar módulo de comandos


def split_Command(inputTxt):  # ANALIZADOR LÉXICO EN TEORÍA

    words = inputTxt.split(" ")
    words2 = []

    for i in range(len(words)):  # Se analiza cada palabra

        # ------------- COMILLAS DOBLE O SIMPLE -------------

        if words[i].startswith('"') or words[i].startswith("'"):
            # Si también termina con comillas dobles o simples
            if words[i].endswith('"') or words[i].endswith("'") and len(words[i]) > 1:
                words2.append(words[i])
            else:  # Sino se busca el siguiente elemento que termine con comillas
                for j in range(i + 1, len(words)):
                    if words[j].endswith('"') or words[j].endswith("'"):
                        # Unir palabras desde i hasta j
                        w = ""
                        for k in range(i, j + 1):
                            if k is not j and words[k] != "'""":
                                w = w + words[k] + " "
                            else:
                                w = w + words[k]
                        words2.append(w)
                        break
                else:  # Sino la encontró
                    return "Error: Comillas no cerradas"

        else:  # SE REALIZA LOWERCASE A LAS PALABRAS, EXCEPTO TODO LO QUE ESTE DESPUES DE UN =
            if "=" not in words[i]:
                words[i] = words[i].lower()
                words2.append(words[i])
            else:
                # SOLO DAR LOWER A LO QUE ESTE ANTES DE UN =
                words2.append(words[i][:words[i].find("=")].lower() + words[i][words[i].find("="):])                

    return analizar_Comando(words2);


def analizar_Comando(consoleLine):
    print (consoleLine)
    # ------------- COMANDO EXECUTE -------------
    if consoleLine[0] == "execute":
        # Si contiene -path= y tiene un path válido
        if consoleLine[1].startswith(">path=") and len(consoleLine[1]) > 6:
            # Obtener path
            path = consoleLine[1][6:]
            # tratar de leer el archivo y obtener String
            try:
                file = open(path, "r")
                text = file.read()
                file.close()
            except:
                return "Error: No se pudo leer el archivo"
            # Separar líneas
            lines = text.split("\n")
            # Analizar cada línea
            for line in lines:
                print(split_Command(line))
        return "Comando execute ejecutado.\n"

    # ===========================================================
    # ================ ADMINISTRACIÓN DE DISCOS =================
    # ===========================================================
    # ------------- COMANDO MKDISK -------------
    elif consoleLine[0] == "mkdisk":
        sizeFound, pathFound = False, False
        for i in range(1, len(consoleLine)):
            if consoleLine[i].startswith(">size="):
                sizeFound = True
            elif consoleLine[i].startswith(">path="):
                pathFound = True
        if not sizeFound or not pathFound:
            return "Error: Faltan parámetros obligatorios"
        return mkdisk.execute(consoleLine)

    # ------------- COMANDO FDISK -------------
    elif consoleLine[0] == "fdisk":
        pathFound, nameFound = False, False
        for i in range(1, len(consoleLine)):
            if consoleLine[i].startswith("-path="):
                pathFound = True
            elif consoleLine[i].startswith("-name="):
                nameFound = True
        if not pathFound or not nameFound:
            return "Error: Faltan parámetros obligatorios"
        return fdisk.execute(consoleLine)        
    
    # ------------- COMANDO RMDISK -------------
    elif consoleLine[0] == "rmdisk":
        if ">path=" not in consoleLine:
            return "Error: Faltan parámetros obligatorios"
        return rmdisk.execute(consoleLine)
    
    # ------------- COMANDO FDISK -------------
    elif consoleLine[0] == "fdisk":
        if ">path=" not in consoleLine or ">name=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.fdisk.execute(consoleLine)
    
    # ------------- COMANDO MOUNT -------------
    elif consoleLine[0] == "mount":
        if ">path=" not in consoleLine or ">name=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.mount.execute(consoleLine)
    
    # ------------- COMANDO UNMOUNT -------------
    elif consoleLine[0] == "unmount":
        if ">id=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.unmount.execute(consoleLine)

    # ------------- COMANDO MKFS -------------
    elif consoleLine[0] == "mkfs":
        if ">id=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.mkfs.execute(consoleLine)
    # ===========================================================
    # =========== ADMINISTRACIÓN DE USUARIOS Y GRUPOS ===========
    # ===========================================================

    # ------------- COMANDO LOGIN -------------
    elif consoleLine[0] == "login":
        if ">user=" not in consoleLine or ">pass=" not in consoleLine or ">id=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.login.execute(consoleLine)

    # ------------- COMANDO LOGOUT -------------
    elif consoleLine[0] == "logout":
        #return c.logout.execute(consoleLine)
        return
    # ------------- COMANDO MKGRP -------------
    elif consoleLine[0] == "mkgrp":
        if ">name=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.mkgrp.execute(consoleLine)
    # ------------- COMANDO RMGRP -------------
    elif consoleLine[0] == "rmgrp":
        if ">name=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.rmgrp.execute(consoleLine)
    # ------------- COMANDO MKUSR -------------
    elif consoleLine[0] == "mkusr":
        if ">user=" not in consoleLine or ">pwd=" not in consoleLine or ">grp=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.mkusr.execute(consoleLine)
    # ------------- COMANDO RMUSR -------------
    elif consoleLine[0] == "rmusr":
        if ">user=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.rmusr.execute(consoleLine)
    
    # ===========================================================
    # ======= ADMINISTRACIÓN DE CARPETAS Y ARCHIVOS =============
    # ===========================================================

    # ------------- COMANDO MKFILE -------------
    elif consoleLine[0] == "mkfile":
        if ">path=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.mkfile.execute(consoleLine)
    # ------------- COMANDO CAT -------------
    elif consoleLine[0] == "cat":
        if ">fileN=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.cat.execute(consoleLine)
    # ------------- COMANDO REMOVE -------------
    elif consoleLine[0] == "remove":
        if ">path=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.remove.execute(consoleLine)
    # ------------- COMANDO EDIT -------------
    elif consoleLine[0] == "edit":
        if ">path=" not in consoleLine or ">cont=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.edit.execute(consoleLine)
    # ------------- COMANDO RENAME -------------
    elif consoleLine[0] == "rename":
        if ">path=" not in consoleLine or ">name=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.rename.execute(consoleLine)
    # ------------- COMANDO MKDIR -------------
    elif consoleLine[0] == "mkdir":
        if ">path=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.mkdir.execute(consoleLine)
    # ------------- COMANDO COPY -------------
    elif consoleLine[0] == "copy":
        if ">path=" not in consoleLine or ">destino=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.copy.execute(consoleLine)
    # ------------- COMANDO MOVE -------------
    elif consoleLine[0] == "move":
        if ">path=" not in consoleLine or ">destino=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.move.execute(consoleLine)
    # ------------- COMANDO FIND -------------
    elif consoleLine[0] == "find":
        if ">path=" not in consoleLine or ">name=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.find.execute(consoleLine)
    # ------------- COMANDO CHOWN -------------
    elif consoleLine[0] == "chown":
        if ">path=" not in consoleLine or ">user=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.chown.execute(consoleLine)
    # ------------- COMANDO CHGRP -------------
    elif consoleLine[0] == "chgrp":
        if ">user=" not in consoleLine or ">grp=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.chgrp.execute(consoleLine)
    # ------------- COMANDO CHMOD -------------
    elif consoleLine[0] == "chmod":
        if ">path=" not in consoleLine or ">ugo=" not in consoleLine:    
            return "Error: Faltan parámetros obligatorios"
        #return c.chmod.execute(consoleLine)
    # ------------- COMANDO PAUSE -------------
    elif consoleLine[0] == "pause":
        #return c.pause.execute(consoleLine)
        return
    
    # ===========================================================
    # ==================== REPORTE DE DATOS =====================
    # ===========================================================

    # ------------- COMANDO REP -------------
    elif consoleLine[0] == "rep":
        return rep.execute()

    # ------------- COMANDO EXIT -------------
    elif consoleLine[0] == "exit":
        return "Comando exit reconocido.\n"

    # ------------- COMANDO NO RECONOCIDO -------------
    return "Comando no reconocido\n"
