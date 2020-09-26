import sys
import datetime
import configparser
from extraccionFtp import  ExtraccionFtp

config = configparser.ConfigParser()
config.read('config.ini')

## Datos FTP
FTP_HOST    = config['extraccion']['host_ftp']
FTP_USER    = config['extraccion']['user_ftp']
FTP_PASS    = config['extraccion']['pass_ftp']
PATH_REMOTE = config['extraccion']['path_remoto']
PATH_LOCAL  = config['extraccion']['path_local']

'''
#################################################################################################################################
#################################################################################################################################
#################################################################################################################################
'''


if __name__ == '__main__':
    print ('main() FTP_HOST        :     ' + FTP_HOST   )
    print ('main() FTP_USER        :     ' + FTP_USER   )
    print ('main() FTP_PASS        :     ' + FTP_PASS   )
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
    
    extraccion.full("Descargar archivos remotos ","paso 2")
    
    for file in array_files:
        result = extraccion.download_file(PATH_REMOTE,PATH_LOCAL,file['name'])
        array_rows.append([PATH_REMOTE,PATH_LOCAL,file['name'],result])
        
    print(extraccion.getTablePretty(array_header,array_rows))
    
    extraccion.full("Cerrando conexión FTP","paso 3")
    extraccion.close()
