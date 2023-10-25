import datetime
import os
import random
import random
import struct
from lib.structs import EBR, MBR, Partition

class Disk:

    staticmethod
    def mostrar_informacion(path):
        with open(path, "rb") as archivo:
            contenido = archivo.read()
            size = struct.unpack("I", contenido[:4])[0]
            fecha = contenido[4:24].decode('utf-8').strip('\0')
            asignatura = struct.unpack("I", contenido[24:28])[0]
            fit = contenido[28:29].decode('utf-8')
            message = "→ Disco creado con éxito."+ "\n→ Tamaño del disco: " + str(size) + "\n→ Fecha de creación: " + fecha + "\n→ Asignatura: " + str(asignatura) + "\n→ Ajuste: " + fit
            print("→ Tamaño del disco: ", size)
            print("→ Fecha de creación: ", fecha)
            print("→ Asignatura: ", asignatura)
            print("→ Ajuste: ", fit)
            print()
            return message


    staticmethod
    def create_disk(size, unit, fit, path):
        ruta = os.path.dirname(path)
        
        if not os.path.exists(ruta):
            os.makedirs(ruta, exist_ok=True)
            print("Ruta creada para el disco: ", ruta)

        disk_size = 0
        if unit.upper() == 'K':
            disk_size = int(size) * 1024
        elif unit.upper() == 'M':
            disk_size = int(size) * 1024 * 1024
        else:
            return "Unidad inválida -> Use 'B' para bytes, 'K' para Kilobytes, ó 'M' para Megabytes."
            
        
        if fit != "FF" and fit != "BF" and fit != "WF":
            print("[Error] Ajuste inválido -> Use 'FF' para First Fit, 'BF' para Best Fit, ó 'WF' para Worst Fit.")
            return "Ajuste inválido -> Use 'FF' para First Fit, 'BF' para Best Fit, ó 'WF' para Worst Fit."
        
        if fit == "BF":
            fit = 'b'
        elif fit == "WF":
            fit = 'w'
        elif fit == "FF":
            fit = 'f'
        archivo = open(path,"wb")
        archivo.seek(disk_size-1)
        archivo.write(b"\0")
        archivo.close()
        fecha = datetime.date.today()
        fecha = str(fecha.strftime("%d/%m/%Y"))
        random_num = random.randint(1, 1000)
        part1 = Partition("0", "0", "0", 0, 0, "Partition1")
        part2 = Partition("0", "0", "0", 0, 0, "Partition2")
        part3 = Partition("0", "0", "0", 0, 0, "Partition3")
        part4 = Partition("0", "0", "0", 0, 0, "Partition4")
        new_mbr= MBR(disk_size,fecha,random_num,fit, part1, part2, part3, part4)
        new_mbr.partition_1.start = 138
        archivo = open(path, "r+b")
        archivo.seek(0)
        archivo.write(new_mbr.format_to_bytes())
        archivo.close()
        message =Disk.mostrar_informacion(path)
        return message
    
    staticmethod
    def fdisk(size,path, name, unit, type, fit, delete,  add):
       
        if size is None:
            if delete is  None:
                print("[Error] Parámetro -size faltante en comando fdisk.")
                return "Parámetro -size faltante en comando fdisk."
        if path is None:
            print("[Error] Parámetro -path faltante en comando fdisk.")
            return "Parámetro -path faltante en comando fdisk."
        if name is None:
            print("[Error] Parámetro -name faltante en comando fdisk.")
            return "Parámetro -name faltante en comando fdisk."
        if delete is not None and add is not None:
            print("[Error] No se puede usar -delete y -add al mismo tiempo en comando fdisk.")
            return "No se puede usar -delete y -add al mismo tiempo en comando fdisk."
        
        part_size = 0
        if size is not None:
            if unit.upper() == 'K':
                part_size = int(size) * 1024
            elif unit.upper() == 'M':
                part_size = int(size) * 1024 * 1024
            elif unit.upper() == 'B':
                part_size = int(size)
            else:
                print("[Error] Unidad inválida -> Use 'B' para bytes, 'K' para Kilobytes, ó 'M' para Megabytes.")
                return "Unidad inválida -> Use 'B' para bytes, 'K' para Kilobytes, ó 'M' para Megabytes."
        
        if not os.path.exists(path):
            print(f"[Error] El disco en {path} no se ha encontrado")
            return "El disco no se ha encontrado"
        
        if type == "E":
            type = 'e'
        elif type == "L":
            type = 'l'
        elif type == "P":
            type = 'p'
        else:
            print("[Error] Tipo inválido -> Use 'P' para primaria, 'E' para extendida, ó 'L' para lógica.")
            return "Tipo inválido -> Use 'P' para primaria, 'E' para extendida, ó 'L' para lógica."

        if fit == "BF":
            fit = 'b'
        elif fit == "WF":
            fit = 'w'
        elif fit == "FF":
            fit = 'f'
        else:
            print("[Error] Ajuste inválido -> Use 'FF' para First Fit, 'BF' para Best Fit, ó 'WF' para Worst Fit.")
            return "Ajuste inválido -> Use 'FF' para First Fit, 'BF' para Best Fit, ó 'WF' para Worst Fit."
       
        
        if delete is not None:
            print("→ Eliminando partición...")
            return Disk.delete_partition(path, name)
        if add is not None:
            print("→ Agregando espacio a partición...")
            return Disk.add_space_to_partition(path, name, add,unit)
        if delete is None and add is None:
            print("→ Creando partición...")
            return Disk.add_partition(path, name, part_size, type, fit)
             

    def add_partition(path, name, part_size, type, fit):
        partitions = []
        disk_size_avalaible = 0
        with open(path, "rb") as archivo:
            contenido = archivo.read()
            disk_size_avalaible = struct.unpack("I", contenido[:4])[0]
            part1 = Partition.format_from_bytes(contenido[29:56])
            partitions.append(part1)
            part2 = Partition.format_from_bytes(contenido[56:83])
            partitions.append(part2)
            part3 = Partition.format_from_bytes(contenido[83:110])
            partitions.append(part3)
            part4 = Partition.format_from_bytes(contenido[110:137])
            partitions.append(part4)
            archivo.close()
       
        inicio = partitions[0].start
        areThereExtended = False
        toseek = 29
        maxCapacity = 0
         #se busca el tamaño para la nueva partición
        for part in partitions:
            if part.status == '1':
                maxCapacity += 1
                inicio += part.size # se suma para el nuevo inicio de la partición
                disk_size_avalaible -=part.size # se resta para verificar si hay espacio para la partición
                toseek += 27 # se suma para buscar la posicion de la siguiente partición
            if part.type == 'e': #si hay una extendida, ya no pueden haber más particiones extendidas
                areThereExtended = True
        # para primarias y extendidas
        if type == 'p' or type == 'e':
            if maxCapacity==4:
                print("[Error] Ya no se pueden crear más particiones.")
                return "Ya no se pueden crear más particiones."
            if part_size > disk_size_avalaible:
                print("[Error] El tamaño de la partición es mayor al tamaño del disco.")
                return f"El tamaño de la partición es mayor al tamaño del disco. (Partición:{part_size} /Disco {disk_size_avalaible})" 
            
            for part in partitions:
                if part.name == name:
                    print("[Error] Ya existe una partición con ese nombre.")
                    return "Ya existe una partición con ese nombre."
                if part.status == '0': #encuentra una sin uso
        
                    part.name = name
                    part.status = '1'
                    part.fit = fit
                    part.size = part_size
                    part.start = inicio
                    part.type = type
                    
                    if part.type == 'e':
                        if areThereExtended:
                            print("[Error] Ya existe una partición extendida.")
                            return "Ya existe una partición extendida."
                        new_ebr = EBR('0', '0', part.start,0, 0, '0')
                        with open(path, "r+b") as archivo:
                            archivo.seek(toseek)
                            archivo.write(part.format_to_bytes())
                            archivo.seek(part.start)
                            archivo.write(new_ebr.format_to_bytes())
                            contenido = archivo.read()
                            txt = "Nueva partición extendida\nNombre: " + part.name + "\nStatus: " + part.status + "\nFit: " + part.fit + "\nSize: " + str(part.size) + "\nStart: " + str(part.start) + "\nType: " + part.type
                            print("\nNueva particion extendida")
                            print("Nombre: ", part.name)
                            print("Status: ", part.status)
                            print("Fit:    ", part.fit)
                            print("Size:   ", part.size)
                            print("Start:  ", part.start)
                            print("Type:   ", part.type)
                            archivo.close()
                        return txt
                        
                    elif part.type == 'p':
                        with open(path, "r+b") as archivo:
                            archivo.seek(toseek)
                            archivo.write(part.format_to_bytes())
                            txt = "Nueva partición primaria\nNombre: " + part.name + "\nStatus: " + part.status + "\nFit: " + part.fit + "\nSize: " + str(part.size) + "\nStart: " + str(part.start) + "\nType: " + part.type
                            print("\nNueva particion primaria")
                            print("Nombre: ", part.name)
                            print("Status: ", part.status)
                            print("Fit:    ", part.fit) 
                            print("Size:   ", part.size)
                            print("Start:  ", part.start)
                            print("Type:   ", part.type)
                            archivo.close()
                            return txt
        if type== 'l':
                if not areThereExtended :
                    print("[Error] No se puede crear una partición lógica sin una extendida.")
                    return "No se puede crear una partición lógica sin una extendida."
                for part in partitions:
                    if part.type == 'e':
                        if part_size > part.size:
                            print(part_size, part.size)
                            print("[Error] El tamaño de la partición es mayor al tamaño de la extendida.", part_size, part.size)
                            return "El tamaño de la partición lógica es mayor al tamaño de la extendida."
                        logical_start = part.start                            
                        next =0
                        with open(path, "r+b") as archivo:
                            contenido = archivo.read()
                            ebr = EBR.format_from_bytes(contenido[logical_start:logical_start+30])
                            

                            if  ebr.part_size==0 and ebr.part_status=="0" and ebr.part_next==0: 
                                ebr.part_name=name
                                ebr.part_status='1'
                                ebr.part_fit=fit
                                ebr.part_size=part_size
                                ebr.part_next=-1
                                archivo.seek(logical_start)
                                archivo.write(ebr.format_to_bytes())
                                archivo.close()
                                txt = "Nueva partición lógica\nNombre: " + ebr.part_name + "\nStatus: " + ebr.part_status + "\nFit: " + ebr.part_fit + "\nSize: " + str(ebr.part_size) + "\nStart: " + str(ebr.part_start) + "\nNext: " + str(ebr.part_next)
                                print("\nNueva particion lógica")
                                print("Nombre: ", ebr.part_name)
                                print("Status: ", ebr.part_status)
                                print("Fit:    ", ebr.part_fit)
                                print("Size:   ", ebr.part_size)
                                print("Start:  ", ebr.part_start)
                                
                                archivo.close()
                                return txt
                            elif ebr.part_next==-1 :
                                # si es -1 agrego en la siguiente posición
                                ebr.part_next = ebr.part_start+ebr.part_size
                                next_ebr = EBR('1', fit, ebr.part_next, part_size, -1, name)
                                archivo.seek(logical_start)
                                archivo.write(ebr.format_to_bytes())
                                logical_start = ebr.part_next
                                archivo.seek(logical_start)
                                archivo.write(next_ebr.format_to_bytes())
                                archivo.close()
                                txt = "Nueva partición lógica\nNombre: " + next_ebr.part_name + "\nStatus: " + next_ebr.part_status + "\nFit: " + next_ebr.part_fit + "\nSize: " + str(next_ebr.part_size) + "\nStart: " + str(next_ebr.part_start) + "\nNext: " + str(next_ebr.part_next)
                                print("\nNueva particion lógica")
                                print("Nombre: ", next_ebr.part_name)
                                print("Status: ", next_ebr.part_status)
                                print("Fit:    ", next_ebr.part_fit)
                                print("Size:   ", next_ebr.part_size)
                                print("Start:  ", next_ebr.part_start)
                                print("Next:   ", next_ebr.part_next)
                            
                                return txt
                            else:
                                while ebr.part_next!=-1:
                                    logical_start = ebr.part_next
                                    ebr = EBR.format_from_bytes(contenido[logical_start:logical_start+30])
                                ebr.part_next = ebr.part_start+ebr.part_size
                                next_ebr = EBR('1', fit, ebr.part_next, part_size, -1, name)
                                archivo.seek(logical_start)
                                archivo.write(ebr.format_to_bytes())
                                logical_start = ebr.part_next
                                archivo.seek(logical_start)
                                archivo.write(next_ebr.format_to_bytes())
                                archivo.close()
                                txt = "Nueva partición lógica\nNombre: " + next_ebr.part_name + "\nStatus: " + next_ebr.part_status + "\nFit: " + next_ebr.part_fit + "\nSize: " + str(next_ebr.part_size) + "\nStart: " + str(next_ebr.part_start) + "\nNext: " + str(next_ebr.part_next)
                                print("\nNueva particion lógica")
                                print("Nombre: ", next_ebr.part_name)
                                print("Status: ", next_ebr.part_status)
                                print("Fit:    ", next_ebr.part_fit)
                                print("Size:   ", next_ebr.part_size)
                                print("Start:  ", next_ebr.part_start)
                                print("Next:   ", next_ebr.part_next)
                                print("Next anterior:   ", ebr.part_next)
                                return txt
    
    def add_space_to_partition(path, name,size, unit):
        partitions = []
        disk_size_avalaible = 0
        with open(path, "rb") as archivo:
            contenido = archivo.read()
            disk_size_avalaible = struct.unpack("I", contenido[:4])[0]
            part1 = Partition.format_from_bytes(contenido[29:56])
            partitions.append(part1)
            part2 = Partition.format_from_bytes(contenido[56:83])
            partitions.append(part2)
            part3 = Partition.format_from_bytes(contenido[83:110])
            partitions.append(part3)
            part4 = Partition.format_from_bytes(contenido[110:137])
            partitions.append(part4)
            archivo.close()
       
        inicio = partitions[0].start
        areThereExtended = False
        toseek = 29
        maxCapacity = 0
         #se busca el tamaño para la nueva partición
        for part in partitions:
            if part.status == '1':
                maxCapacity += 1
                inicio += part.size # se suma para el nuevo inicio de la partición
                disk_size_avalaible -=part.size # se resta para verificar si hay espacio para la partición
                toseek += 27 # se suma para buscar la posicion de la siguiente partición
            if part.type == 'e': #si hay una extendida, ya no pueden haber más particiones extendidas
                areThereExtended = True
        
    
    def delete_partition(path,name):
        

        partitions = []
        disk_size = 0
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
        inicio = partitions[0].start
        toseek = 29
        for part in partitions:
            if part.name==name:
                part.name = "0"
                part.status = '0'
                part.fit = "0"
                part.size = 0
                part.start = part.start
                part.type = "0"
                with open(path, "r+b") as archivo:
                    archivo.seek(toseek)
                    archivo.write(part.format_to_bytes())
                    archivo.close()
                    return print("Partición eliminada con éxito.")
            toseek += 27 # se suma para buscar la posicion de la siguiente partición
        return print("[Error] No se encontró la partición.")