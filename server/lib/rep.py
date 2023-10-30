import os
import struct
import graphviz as gv
import boto3
from lib.structs import EBR, Partition

class Rep:

    def disk(path_rep,path_disk,aws_id,aws_key,bucket_name):
        path = os.path.dirname(path_rep)
        
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print("Ruta creada para el reporte disk ", path)

        title = Rep.obtain_name_disk(path_disk)
        size = Rep.size_disk(path_disk)
        percent = 0
        graph_content = Rep.header_rep_disk(title)

        parts = Rep.get_partitions(path_disk)
        for part in parts:
            if part.status == '1':
                percent += Rep.calc_percentage(size,part.size)
                percent = round(percent,2)
                if part.type == 'e':
                    graph_content+= Rep.column_rep_Disk("Extendida", str(percent))
                elif part.type == 'p':
                    graph_content+= Rep.column_rep_Disk("Primaria", str(percent))
        free_space = 100 - percent
        graph_content+= Rep.column_rep_Disk("Libre", str(free_space))
        graph_content+= Rep.footer_rep_disk()      
 

        src = gv.Source(graph_content,format="png")
        src.render(path_rep)
        if os.path.exists(path_rep):
            os.remove(path_rep)
        name = os.path.basename(path_rep)+".png"
        s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_key)            
        s3.upload_file(path_rep+".png", bucket_name, name)
        return "Se ha generado el reporte disk en la ruta "+str(path_rep)+".png\ny se ha cargado a la carpeta de reportes de la web"
    


    def mbr(path_rep,path_disk,aws_id,aws_key,bucket_name):
        path = os.path.dirname(path_rep)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print("Ruta creada para el reporte mbr ", path)
        with open(path_disk, "r+b") as archivo:
            contenido = archivo.read()
            size = struct.unpack("I", contenido[:4])[0]
            date = contenido[4:24].decode('utf-8').strip('\0')
            signature = struct.unpack("I", contenido[24:28])[0]
            archivo.close()
            graph_content = Rep.header_rep_mbr(size,date,signature)
            
            parts = Rep.get_partitions(path_disk)
            for part in parts:
                if part.status == '1':
                    if part.type == 'e':
                        logical_start = part.start
                        with open(path_disk, "r+b") as archivo:
                            contenido = archivo.read()
                            ebr = EBR.format_from_bytes(contenido[logical_start:logical_start+30])
                            if  ebr.part_size==0 and ebr.part_status=="0" and ebr.part_next==0:
                                print("No hay particiones logicas")
                                return
                            while ebr.part_next != -1:
                                graph_content+= Rep.column_rep_logic_mbr(ebr.part_next,ebr.part_fit,ebr.part_start,ebr.part_size,ebr.part_name,ebr.part_status)
                                logical_start = ebr.part_next
                                ebr = EBR.format_from_bytes(contenido[logical_start:logical_start+30]) 
                            archivo.close()
                    elif part.type == 'p':
                        graph_content+= Rep.column_rep_primary_mbr(part.type,part.fit,part.start,part.size,part.name,part.status) 
            graph_content+= Rep.footer_rep_mbr()      


            src = gv.Source(graph_content,format="png")
            src.render(path_rep)
            
            name = os.path.basename(path_rep)+".png"
            print(path_rep, name)                        
            s3 = boto3.client('s3', aws_access_key_id=aws_id, aws_secret_access_key=aws_key)            
            s3.upload_file(path_rep+".png", bucket_name, name)
            return "Se ha generado el reporte mbr en la ruta "+str(path_rep)+".png\ny se ha cargado a la carpeta de reportes de la web"




    def obtain_name_disk(path):
        name_disk = os.path.basename(path)  # Obtiene el nombre del archivo de la ruta
        name_disk = os.path.splitext(name_disk)[0]  # Elimina la extensión del archivo
        return name_disk
    
    def size_disk(path):
        with open(path, "rb") as archivo:
            contenido = archivo.read()
            size = struct.unpack("I", contenido[:4])[0]
            archivo.close()
            return size
        
    def get_partitions(path):
        partitions = []
        with open(path, "rb") as archivo:
            contenido = archivo.read()
            part1 = Partition.format_from_bytes(contenido[29:56])
            partitions.append(part1)
            part2 = Partition.format_from_bytes(contenido[56:83])
            partitions.append(part2)
            part3 = Partition.format_from_bytes(contenido[83:110])
            partitions.append(part3)
            part4 = Partition.format_from_bytes(contenido[110:137])
            partitions.append(part4)
            archivo.close()
        return partitions
    
    def calc_percentage(Total, part):
        if Total == 0:
            return None #no se puede dividir entre 0
        porcentaje = (part / Total) * 100
        return porcentaje
    
    def header_rep_disk(title):
        txt  ="""digraph G{
    \n\tnode [shape=plaintext, fontname="Arial", fontsize=12];
    \n\tedge [style=invis];
    \n\ttitulo [label="""+title+""" shape="underline"  fontsize=25];
    
    \n\ttable [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="3">
      \n\t<TR>
       \n\t<TD BGCOLOR="lightgrey" CELLPADDING="15" >MBR</TD>"""
        return txt
    
    def column_rep_Disk(type,percent):
        txt = """\n\t<TD BGCOLOR="lightgrey" CELLPADDING="15" >"""+type+"""<BR/>"""+percent+"""'%' espacio</TD>"""
        return txt
    
    def footer_rep_disk():
        txt = """\n\t</TR> 
        \n\t</TABLE>>];
        \n\ttitulo -> { table } [dir=none];
        \n}"""
        return txt
    
    def header_rep_mbr(size,date,signature):
        txt = """digraph G {
        \n\tnode [shape=plaintext, fontname="Arial", fontsize=12];
        \n\tedge [style=invis];
    \n\ttable [label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="3">
        \n\t<TR> <TD CELLPADDING="8" BGCOLOR="PINK">REPORTE DE MBR</TD></TR>
        \n\t<TR>
            \n\t<TD BGCOLOR="white" CELLPADDING="6" >Size</TD>
           \n\t <TD BGCOLOR="white" CELLPADDING="6" >"""+str(size)+"""</TD>
        \n\t</TR>
        \n\t<TR>
           \n\t <TD BGCOLOR="lightblue" CELLPADDING="6" >Creation date</TD>
           \n\t <TD BGCOLOR="lightblue" CELLPADDING="6" >"""+str(date)+"""</TD>
        \n\t</TR>
        \n\t<TR>
            \n\t<TD BGCOLOR="white" CELLPADDING="6" >Disk asignature</TD>
            \n\t<TD BGCOLOR="white" CELLPADDING="6" >"""+str(signature)+"""</TD>
        \n\t</TR>"""
        return txt
    def column_rep_primary_mbr(type,fit,start,size,name,status):
        txt= """
     \n\t<TR> <TD CELLPADDING="8" BGCOLOR="yellow">Particion primaria</TD></TR>
      \n\t<TR>
       \n\t <TD BGCOLOR="white" CELLPADDING="6" >Status</TD>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >"""+str(status)+"""</TD>
      \n\t</TR>
     \n\t <TR>
       \n\t <TD BGCOLOR="burlywood2" CELLPADDING="6" >Type</TD>
        \n\t<TD BGCOLOR="burlywood2" CELLPADDING="6" >"""+str(type)+"""</TD>
      \n\t</TR>
    \n\t<TR>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >Fit</TD>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >"""+str(fit)+"""</TD>
     \n\t </TR>
    \n\t<TR>
      \n\t  <TD BGCOLOR="burlywood2" CELLPADDING="6" >Start</TD>
       \n\t <TD BGCOLOR="burlywood2" CELLPADDING="6" >"""+str(start)+"""</TD>
     \n\t </TR>
    \n\t<TR>
    \n\t    <TD BGCOLOR="white" CELLPADDING="6" >Size</TD>
    \n\t    <TD BGCOLOR="white" CELLPADDING="6" >"""+str(size)+"""</TD>
     \n\t </TR>
     \n\t <TR>
       \n\t <TD BGCOLOR="burlywood2" CELLPADDING="6" >Name</TD>
        \n\t<TD BGCOLOR="burlywood2" CELLPADDING="6" >"""+str(name)+"""</TD>
      \n\t</TR>"""
        return txt
    
    def column_rep_logic_mbr(next,fit,start,size,name,status):
        txt= """
     \n\t<TR> <TD CELLPADDING="8" BGCOLOR="darkorchid1">Particion logica</TD></TR>
      \n\t<TR>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >Status</TD>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >"""+str(status)+"""</TD>
      \n\t</TR>
      \n\t<TR>
        \n\t<TD BGCOLOR="gainsboro" CELLPADDING="6" >Next</TD>
        \n\t<TD BGCOLOR="gainsboro" CELLPADDING="6" >"""+str(next)+"""</TD>
      \n\t</TR>
    \n\t<TR>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >Fit</TD>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >"""+str(fit)+"""</TD>
      \n\t</TR>
   \n\t<TR>
        \n\t<TD BGCOLOR="gainsboro" CELLPADDING="6" >Start</TD>
        \n\t<TD BGCOLOR="gainsboro" CELLPADDING="6" >"""+str(start)+"""</TD>
      \n\t</TR>

    \n\t<TR>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >Size</TD>
        \n\t<TD BGCOLOR="white" CELLPADDING="6" >"""+str(size)+"""</TD>
      \n\t</TR>
      \n\t<TR>
        \n\t<TD BGCOLOR="gainsboro" CELLPADDING="6" >Name</TD>
        \n\t<TD BGCOLOR="gainsboro" CELLPADDING="6" >"""+str(name)+"""</TD>
      \n\t</TR>"""
        return txt
    
    def footer_rep_mbr():
        txt = """
        \n\t</TABLE>>];
        \n\ttable [dir=none];
        \n}"""
        return txt