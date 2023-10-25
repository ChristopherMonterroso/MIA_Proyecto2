import os
import struct

from lib.structs import Partition


class mount:
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.siguiente = None

class Lista_mounts:
    def __init__(self):
        self.cabeza = None

    def mount(self, id, path):
        if self.getMount(id) is not None:
            print(f"La partición {id} ya se encuentra montada.")
            return f"La partición{id} ya se encuentra montada."
        new_mount = mount(id, path)
        if self.cabeza is None:
            self.cabeza = new_mount
            print(f"Partición {id} montada.")
            parts = self.showMounts()
            return f"Partición {id} montada.\n{parts}"
        else:
            tmp = self.cabeza
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = new_mount
            print(f"Partición {id} montada.")
            parts = self.showMounts()
            return f"Partición {id} montada.\n{parts}"


    def unMount(self, id):
        if self.cabeza is None:
            print("No hay particiones montadas.")
            return

        if self.cabeza.id == id:
            self.cabeza = self.cabeza.siguiente
            print(f"Partición {id} desmontada.")
            parts=self.showMounts()
            return f"Partición {id} desmontada.\n{parts}" 

        tmp = self.cabeza
        while tmp.siguiente is not None:
            if tmp.siguiente.id == id:
                tmp.siguiente = tmp.siguiente.siguiente
                print(f"Partición {id} desmontada.")
                return f"partición {id} desmontada."
            tmp = tmp.siguiente
        print(f"Partición {id} no encontrada.")
        return f"Partición {id} no encontrada."
    
    def showMounts(self):
        if self.cabeza is None:
            print("No hay particiones montadas.")
            return "No hay particiones montadas."
        tmp = self.cabeza
        print("Particiones montadas:")
        txt = "\nParticiones montadas:\n"
        while tmp is not None:
            print(f"ID: {tmp.id} - Path: {tmp.path}")
            txt += f"ID: {tmp.id} - Path: {tmp.path}\n"
            tmp = tmp.siguiente
        return txt
    def getMount(self, id):
        tmp = self.cabeza
        while tmp is not None:
            if tmp.id == id:
                return tmp
            tmp = tmp.siguiente
        return None
    

class ID:

    def generate_id(path, name_partition):
        if not os.path.exists(path):
            print(f"[Error] El disco en {path} no se ha encontrado para el montaje.")
            return
        name_disk = ID.obtain_name_disk(path)
        no_partition = ID.obtain_No_partition(path,name_partition)
        id = "63"+str(no_partition)+name_disk
        return id
     
    def obtain_No_partition(path,name_partition):
        partitions = [] 
        with open(path, "rb") as archivo:
            contenido = archivo.read()
            disk_size = struct.unpack("I", contenido[:4])[0]
            part1 = Partition.format_from_bytes(contenido[29:56])
            partitions.append(part1)
            part2 = Partition.format_from_bytes(contenido[56:83])
            partitions.append(part2)
            part3 = Partition.format_from_bytes(contenido[83:110])
            partitions.append(part3)
            part4 = Partition.format_from_bytes(contenido[110:137])
            partitions.append(part4)
            archivo.close()
        no_partition = 0
        for part in partitions:
            if part.status == '1':
                no_partition += 1
                if part.name==name_partition:
                    break
            
        return no_partition
            
    def obtain_name_disk(path):
        name_disk = os.path.basename(path)  # Obtiene el nombre del archivo de la ruta
        name_disk = os.path.splitext(name_disk)[0]  # Elimina la extensión del archivo
        return name_disk

    

   