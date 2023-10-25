import os
from time import sleep

from flask import jsonify
from lib.disk import Disk
from lib.mount import Lista_mounts
from lib.mount import ID
from lib.rep import Rep
mounts = Lista_mounts()


def command_mkdisk(tokens):
    size_param = None
    unit_param = 'M'
    path_param = None
    fit_param = 'FF'
    for token in tokens[1:]:
        if token.startswith("-size="):
            size_param = token.split('=')[1]
        elif token.startswith("-unit="):
            unit_param = token.split('=')[1]
        elif token.startswith("-path="):
            path_param = token.split('=')[1]
        elif token.startswith("-fit="):
            fit_param = token.split('=')[1]
        else:
            print(f"[Error] Parámetro {token} no reconocido.")
            return{"Error":"true",
                "Message":"Parámetro {token} no reconocido."}
    if size_param and path_param is not None:
        message = Disk.create_disk(size_param,unit_param,fit_param,path_param)
        return {"Error":"false",
                "Message":message}
    else:
        return {"Error":"true",
                "Message":"Parámetros faltantes o incorrectos para el comando mkdisk."}

def command_rmdisk(tokens):
    path = None
    for token in tokens[1:]:
        if token.startswith("-path="):
            path = token.split('=')[1]
        else:
            print(f"[Error] Parámetro {token} no reconocido.")
    if path is not None and os.path.exists(path):
        os.remove(path)
        print(f"Disco en {path} eliminado con éxito.")
        return {"Error":"true",
                "Message":f"Disco en {path} eliminado con éxito."}
    else:
        print(f"[Error] El disco en {path} no se ha encontrado o no se puede eliminar.")  
        return{"Error":"true",
                "Message":f"El disco en {path} no se ha encontrado o no se puede eliminar."}
         

    
def command_fdisk(tokens):
    size_param = None
    path_param = None
    name_param = None
    unit_param = "K"
    type_param = "P"
    fit_param = "WF"
    delete_param = None
    add_param = None
    for token in tokens[1:]:
        if token.startswith("-size="):
            size_param = token.split('=')[1]
        elif token.startswith("-path="):
            path_param = token.split('=')[1]
        elif token.startswith("-unit="):
            unit_param = token.split('=')[1]
        elif token.startswith("-name="):
            name_param = token.split('=')[1]
        elif token.startswith("-type="):
            type_param = token.split('=')[1]
        elif token.startswith("-fit="):
            fit_param = token.split('=')[1]
        elif token.startswith("-delete="):
            delete_param = token.split('=')[1]
        elif token.startswith("-add="):
            add_param = token.split('=')[1]
        else:
            print(f"[Error] Parámetro {token} no reconocido.")
            
    
    message = Disk.fdisk(size_param,path_param,name_param,unit_param,type_param,fit_param,delete_param,add_param)
    return {"Error":"false",
            "Message":message}

def command_mount(tokens):
    path_param = None
    name_partition_param = None
    for token in tokens[1:]:
        if token.startswith("-path="):
            path_param = token.split('=')[1]
        elif token.startswith("-name="):
            name_partition_param = token.split('=')[1]
    if path_param and name_partition_param is not None:
        id = ID.generate_id(path_param,name_partition_param)
        message = mounts.mount(id,path_param)
        return {"Error":"false",
                "Message":message}
    else:
        print("[Error] Parámetros faltantes o incorrectos para el comando mount.")
        return {"Error":"true",
                "Message":"Parámetros faltantes o incorrectos para el comando mount."}
    
def command_unmount(tokens):
    id_param = None
    for token in tokens[1:]:
        if token.startswith("-id="):
            id_param = token.split('=')[1]
    if id_param is not None:
        message = mounts.unMount(id_param)
        return {"Error":"false",
                "Message":message}
    else:
        print("[Error] Parámetros faltantes o incorrectos para el comando unmount.")
        return{"Error":"true",
                "Message":"Parámetros faltantes o incorrectos para el comando unmount."}
    
def command_rep(tokens):
    name_param = None
    path_report = None
    id_param = None
    for token in tokens[1:]:
        if token.startswith("-name="):
            name_param = token.split('=')[1]
        elif token.startswith("-path="):
            path_report = token.split('=')[1]
        elif token.startswith("-id="):
            id_param = token.split('=')[1]
    if name_param and path_report and id_param is not None:
        path_disk = mounts.getMount(id_param).path #obtengo el path del disco, usando la lista de montajes
        if path_disk is None:
            print(f"[Error] No se ha encontrado el disco de la partición con id {id_param}.")
            return {"Error":"true",
                    "Message":f"No se ha encontrado el disco de la partición con id {id_param}."}
        if name_param == "mbr":
            print("Generando reporte mbr...")
            sleep(2)
            message =Rep.mbr(path_report,path_disk)
            return {"Error":"false",
                    "Message":message}
        elif name_param == "disk":
            print("Generando reporte disk...")
            sleep(2)
            message =Rep.disk(path_report,path_disk)
            return {"Error":"false",
                    "Message":message}
    else:
        print("[Error] Parámetros faltantes o incorrectos para el comando rep.")
        return{"Error":"true",
               "message":"Parámetros faltantes o incorrectos para el comando rep."}