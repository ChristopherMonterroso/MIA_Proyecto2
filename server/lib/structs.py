import datetime
import struct
import time

class Partition:
   def __init__(self,status:str,type:str,fit:str,start,size,name:str):
      self.status = status  # 0 no usado. 1 ya esta en uso
      self.type = type     # P, E, L
      self.fit = fit      # Ajuste wf, bf, ff
      self.start = start    #
      self.size = size
      self.name = name  # nombre máximo de 16 caracteres

   def format_to_bytes(self):
      format = "1s 1s 1s I I 16s"
      return struct.pack(
         format, 
         self.status.encode('utf-8'), 
         self.type.encode('utf-8'), 
         self.fit.encode('utf-8'), 
         self.start, 
         self.size, 
         self.name.ljust(16, '\0').encode('utf-8'))
   
   @classmethod
   def format_from_bytes(cls, data):
      status = data[0:1].decode('utf-8').strip('\0')
      type = data[1:2].decode('utf-8').strip('\0')
      fit = data[2:3].decode('utf-8').strip('\0')
      start = struct.unpack('I', data[4:8])[0]
      size = struct.unpack('I', data[8:12])[0]
      name = data[12:28].decode('utf-8').rstrip('\0')
      return cls(status, type, fit, start, size, name)

class MBR:
   def __init__(self,mbr_tamano,fecha_creacion:str,signature,disk_fit:str,partition_1,partition_2,partition_3,partition_4):
      self.mbr_tamano = mbr_tamano     # 4 bytes
      self.fecha_creacion = fecha_creacion  # 24 bytes
      self.signature = signature  # 4 bytes
      self.disk_fit = disk_fit       # 1 byte
      self.partition_1 =partition_1  # {status, type, fit, start, size, name} // 27 bytes
      self.partition_2 =Partition("0","0","0",0,0,"0")  # 27 bytes
      self.partition_3 =Partition("0","0","0",0,0,"0")  # 27 bytes
      self.partition_4 =Partition("0","0","0",0,0,"0")  # n logicas // 27 bytes

   def format_to_bytes(self):
      format = "I 20s I 1s 27s 27s 27s 27s"
      return struct.pack(format,
         self.mbr_tamano,
         self.fecha_creacion.encode('utf-8'),
         self.signature,
         self.disk_fit.encode('utf-8'),
         self.partition_1.format_to_bytes(),
         self.partition_2.format_to_bytes(),
         self.partition_3.format_to_bytes(),
         self.partition_4.format_to_bytes())
   
class EBR:
   def __init__(self,part_status:str,part_fit:str,part_start:int,part_size:int,part_next:int,part_name:str):
      self.part_status = part_status  # 1 byte
      self.part_fit = part_fit     # 1 byte
      self.part_start = part_start    # 4 bytes
      self.part_size = part_size    # 4 bytes
      self.part_next = part_next    # 4 bytes
      self.part_name = part_name  # 16 bytes

   def format_to_bytes(self):
      format = "1s 1s i i i 16s"
      return struct.pack(
         format, 
         self.part_status.encode('utf-8'), 
         self.part_fit.encode('utf-8'), 
         self.part_start, 
         self.part_size, 
         self.part_next, 
         self.part_name.ljust(16, '\0').encode('utf-8'))
   
   @classmethod
   def format_from_bytes(cls, data):
      part_status = data[0:1].decode('utf-8').strip('\0')
      part_fit = data[1:2].decode('utf-8').strip('\0')
      part_start = struct.unpack('I', data[4:8])[0]
      part_size = struct.unpack('I', data[8:12])[0]
      part_next = struct.unpack('i', data[12:16])[0]
      part_name = data[16:32].decode('utf-8').rstrip('\0')
      return cls(part_status, part_fit, part_start, part_size, part_next, part_name)