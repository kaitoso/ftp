import datetime
import ftplib
from prettytable import PrettyTable

class ExtraccionFtp:
    def __init__(self,host,usuario,clave):
        self.host    = host
        self.usuario = usuario
        self.clave   = clave
        self.ftp = ftplib.FTP(self.host) 

    def login(self):
        try:
            self.ftp.login(self.usuario,self.clave)
        except Exception  as e:
            self.full(str(e),"login")
           
    def full(self,msg, level ):
            str_dattime = str(datetime.datetime.now())
            print('{0} - {1} - {2}'.format( str_dattime, level, msg))
       
    def close(self):
        try:
            self.ftp.quit()
        except  Exception  as e:
            self.full(str(e),"close")
    
    def void_ls_comand(self,path_dir):
        try:
            self.ftp.cwd(path_dir)
            self.ftp.dir()
        except Exception as e:
            full(str(e),'void_ls_comand')
    
    def size_fmt(self,num,suffix='B'):
        try:
            for unit in ['','K','M','G','T','P','E','Z']:
                if abs(num) < 1024.0:
                    return "%3.1f%s%s" % (num,unit,suffix)
                    
                num /= 1024.0
            return "%.1f%s%s" % (num,'Yi',suffix)  
        
        except Exception as e:
            self.full(str(e),"size_fmt")
         
    
    def get_datetime_format(date_time):
        date_time=date_time.strptime(date_time, "%Y%m%d%H%M%S")
        return date_time.strftime("%Y-%m-%d %H:%M:%S")
        
    def is_file(self,filename):
        current = self.ftp.pwd()
        try:
            self.ftp.cwd(filename)
        except:
            self.ftp.cwd(current)
            return True
        self.ftp.cwd(current)
        return False
    
    def download_file(self,path_remote,path_local,file_name):
        try:
            self.ftp.cwd(path_remote)
            new_file = open(path_local+'/'+file_name, 'wb') ; 
            self.ftp.retrbinary("RETR " + file_name ,new_file.write); 
            return "success"
        except  Exception  as e:
            return str(e)
            self.full(str(e),"download_file")
    
    def getTablePretty(selft,header,rows):
        table = PrettyTable(header)
        for row in rows:
            table.add_row(row)
        return table
    
    def get_content_nlst(self,path_dir):
        try:
            array_files = []
            self.ftp.cwd(path_dir)
            for file_name in self.ftp.nlst():
                if(self.is_file(file_name)):
                    size = self.ftp.size(file_name)
                    size = self.size_fmt(size)
                    object = {'size':size,'name':file_name}
                    array_files.append(object)
               
            return array_files
                   
        except  Exception  as e:
            self.full(str(e),"get_content_nlst")