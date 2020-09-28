import sys
import codecs
import os
import datetime
import configparser
from extraccionFtp import  ExtraccionFtp
from conexion import Conexion
config = configparser.ConfigParser()
config.read('config.ini')

## Datos FTP
FTP_HOST    = config['extraccion']['host_ftp']
FTP_USER    = config['extraccion']['user_ftp']
FTP_PASS    = config['extraccion']['pass_ftp']
PATH_REMOTE = config['extraccion']['path_remoto']
PATH_LOCAL  = config['extraccion']['path_local']

## Datos de manipulación
ENDWITH = config['manipulacion']['extension']


def fechaHora():
    str_dattime = str(datetime.datetime.now())
    return '{0}'.format( str_dattime)

def compareline(buscar, sline, nline):
    print("BUSCAR ES: ----------",buscar)
    print("SLINE ES --------------", sline)
    print("nLINE ES --------------", nline)
    contains = buscar.upper() in sline.upper()

    
    if contains:
        print(fechaHora()+" se encontró ---->"+buscar+" en la linea:",nline)
        #print("el contains",contains)
    return contains
    

def asignarVariables(sline):
    separado = "\t"
    asignacion = ""
    lineElements = sline.split(separado)
    if len(lineElements) > 2:
        print(asignacion)
        asignacion = lineElements[3].replace("'", "")
        print(asignacion)
    return asignacion

def  leerArchivo(array_logs):
    VQ = ""
    AGENT = ""
    PLACE = ""
    DN = ""
    ACCESS = ""
    SWITCH = ""
    TARGET = ""
    AttributeReferenceID = ""
    AttributeConnID = ""




    bVQ = False
    bAGENT = False
    bPLACE = False
    bDN = False
    bACCESS = False
    bSWITCH = False
    bTARGET = False
    bAttributeReferenceID = False
    bAttributeConnID = False
    IsNoAnswer = False
    IsCallHasDisconnected = False
    IsWordMatch= False

    for file in array_logs:

        if file.endswith(ENDWITH):
            
            print('archivo valido : {0}'.format(file))
            with codecs.open(PATH_LOCAL+file, 'r', encoding='utf-8', errors='ignore') as fdata:
                lineas = fdata.readlines()
                count = 1
                for linea in lineas:
                    
                    if not IsWordMatch:
                        IswordMatch = compareline('No answer at DN',linea,count)
                    if not IsWordMatch:
                        IswordMatch = compareline('Unknown cause',linea,count)
                    if not IsWordMatch:
                        IswordMatch = compareline('Out of service',linea,count)
                        
                    
                    if IswordMatch:
                        
                        if not bVQ:
                            
                            bVQ = compareline('VQ',linea,count)
                            print ("SEÑORAAAAAAAAAA",bVQ)
                            if bVQ:
                                VQ = asignarVariables(linea)
                                print("holaaaaaaaa",VQ)
                        if not bAGENT:
                            
                            bAGENT = compareline("AGENT",linea,count)
                            
                            if bAGENT:
                                AGENT = asignarVariables(linea)
                                
                        if not bPLACE:
                            
                            bPLACE = compareline('PLACE',linea,count)
                            
                            if bPLACE:
                                PLACE = asignarVariables(linea)
                                
                        if not bDN:
                            
                            bDN = compareline('DN',linea,count)
                            
                            if bDN:
                                DN = asignarVariables(linea)
                                
                        if not bACCESS:
                            
                            bACCESS = compareline('ACCESS',linea,count)
                            
                            if bACCESS:
                                ACCESS = asignarVariables(linea)
                                
                        if not bSWITCH:
                            
                            bSWITCH = compareline('SWITCH',linea,count)
                            
                            if bSWITCH:
                                SWITCH = asignarVariables(linea)
                                
                        if not bTARGET:
                            
                            bTARGET = compareline('TARGET',linea,count)
                            
                            if bTARGET:
                                TARGET = asignarVariables(linea)
                                
                        if not bAttributeReferenceID:
                            
                            bAttributeReferenceID = compareline("AttributeReferenceID",linea,count)
                            
                            if bAttributeReferenceID:
                                AttributeReferenceID = asignarVariables(linea)
                                
                        if not bAttributeConnID:
                            
                            bAttributeConnID = compareline("AttributeConnID",linea,count)
                            
                            if bAttributeConnID:
                                AttributeConnID = asignarVariables(linea)
                                
                        if bVQ and bAGENT and bPLACE and bDN and bACCESS and bSWITCH and bTARGET and bAttributeReferenceID and bAttributeConnID:
                            print("VQ = ",VQ)
                            print("AGENT = ",AGENT)
                            print("PLACE = ",PLACE)
                            print("DN = ",DN)
                            print("ACCESS = ",ACCESS)
                            print("SWITCH = ",SWITCH)
                            print("TARGET = ",TARGET)
                            print("AttributeReferenceID = ",AttributeReferenceID)
                            print("AttributeConnID = ",AttributeConnID)
                    # if'Unknown cause' in linea:
                    #     print(fechaHora()+" se encontró ---->"+linea+" en la linea:",count)
                    # if'Out of service' in linea:
                    #      print(fechaHora()+" se encontró ---->"+linea+" en la linea:",count)
                            VQ = ""
                            AGENT = ""
                            PLACE = ""
                            DN = ""
                            ACCESS = ""
                            SWITCH = ""
                            TARGET = ""
                            AttributeReferenceID = ""
                            AttributeConnID = ""
                            

                            bVQ = False
                            bAGENT = False
                            bPLACE = False
                            bDN = False
                            bACCESS = False
                            bSWITCH = False
                            bTARGET = False
                            bAttributeReferenceID = False
                            bAttributeConnID = False
                            IsNoAnswer = False
                            IsCallHasDisconnected = False
                            IsWordMatch= False
                    count = count+1



if __name__ == '__main__':
    print ('main() FTP_HOST        :     ' + FTP_HOST   )
    print ('main() FTP_USER        :     ' + FTP_USER   )
    
    print ('main() FTP_PATH_REMOTE :     ' + PATH_REMOTE)
    print ('main() FTP_PATH_LOCAL  :     ' + PATH_LOCAL )
    print ('main() FECHA_EJECUCION :     ' + str(datetime.datetime.now()) )


    extraccion = ExtraccionFtp(FTP_HOST,FTP_USER,FTP_PASS)
    extraccion.full("Abriendo conexión FTP ","paso 0")
    extraccion.login()
    
    print("-"*80)
    print("*"*1,"Listado total del contenido remoto (directorios,archivos,link,etc)","*"*1)
    print("-"*80)
    extraccion.void_ls_comand(PATH_REMOTE)
    
    print("-"*80)
    extraccion.full("Obtener solo archivos remotos ","paso 1")
    
    array_files = extraccion.get_content_nlst(PATH_REMOTE)
    array_header = ["FILE_NAME","SIZE"]
    array_rows = []
    
    for file in array_files:
        array_rows.append([file['name'],file['size']])
    
    print(extraccion.getTablePretty(array_header,array_rows))
    
    array_header = ["PATH_REMOTE","PATH_LOCAL","FILE_NAME","STATUS_DOWNLOAD"]
    array_rows = []
    
    """  extraccion.full("Descargar archivos remotos ","paso 2")
    
   for file in array_files:
        result = extraccion.download_file(PATH_REMOTE,PATH_LOCAL,file['name'])
        array_rows.append([PATH_REMOTE,PATH_LOCAL,file['name'],result])
        
    print(extraccion.getTablePretty(array_header,array_rows))  """
    
    extraccion.full("Cerrando conexión FTP","paso 3")
    extraccion.close()

    ##Logic
    print("-"*80)
    print("*"*1,"Manipulación de log validos *.log","*"*1)
    print("-"*80)

    array_logs = os.listdir(PATH_LOCAL)
    
    leerArchivo(array_logs)
    
            



