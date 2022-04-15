# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 11:40:27 2018

"""

from  ftplib import FTP
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from msci_path import Declare
import logging
from time import sleep


# Getting the values from conf file having key as 'msci'.
CONF_FILE = Declare()
CONF = CONF_FILE.get_conf()
BASE = declarative_base()
LCNF = CONF['DataBase']



#-----------------------Multihtreading Implementation----------------------

def my_function(item):
    res = item*item
    return res

results = []
my_array = [10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8,10,12,2,3,4,5,6,7,8]
for item in my_array:
    results.append(my_function(item))
print("The value of results is =",results)
#-------------------------------------------------------------------------
from multiprocessing.dummy import Pool as ThreadPool
pool = ThreadPool(4) 
results = pool.map(my_function, my_array)
print("The value of results is =",results)
#------------------------------------------------------------------------------
def get_engine():
    """
    Method get_engine will connect with the database and give a handle for use
    """
    url = 'mssql+pymssql://'+LCNF['user']+':'+LCNF['pass']+'@'+LCNF['host']+'/'+LCNF['schema']
    return sqlalchemy.create_engine(url, legacy_schema_aliasing=False)


class FtpService(object):
    """
    class FtpService will connect with the FTP location
    and Provide FTP service to get files from msci server
    """
    logger = logging.getLogger(__name__)
    def __init__(self, CONF: dict):
        """
        Initialize the service with configuration
        :type self: FtpService
        """
        self._conf = CONF
        self._ftp_host = CONF['FTP']['site']
        self._ftp_user = CONF['FTP']['user']
        self._ftp_pass = CONF['FTP']['pass']
        self.ftp = None


    def get_ftp(self):
        """
        Making the connection with the FTP Service
        """
        files = None
        i = 0
        while i < 3:
            i += 1
            try:              
                self.ftp = FTP(self._ftp_host)
                self.logger.info("Ftp to %s established", self._ftp_host)
                self.ftp.login(self._ftp_user, self._ftp_pass)
                files = self.ftp.nlst()
                self.logger.info("Login to FTP by user %s is established", self._ftp_user)
                return files
            except IOError as error:
                self.logger.error("I/O error occurred as %s", error)
                if i < 3:
                    self.logger.info("Login to FTP %s is not established trying one more\
                                      attempt", self._ftp_user)
                    sleep(10)
                    continue
                else:
                    raise IOError
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
import os
import paramiko
server, username, password = ('host', 'username', 'password')   
ssh = paramiko.SSHClient()  
parmiko.util.log_to_file(log_filename)    
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

' #In case the server's key is unknown,'
#we will be adding it automatically to the list of known hosts 
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))   

#Loads the user's local known host file  
ssh.connect(server, username=username, password=password) 
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls /tmp') 

print "output", ssh_stdout.read() #Reading output of the executed co'mmand 
error = ssh_stderr.read()  

#Reading the error stream of the executed command
print "err", error, len(error) 

#Transfering files to and from the remote machine' 
sftp = ssh.open_sftp()   
'sftp.get(remote_path, local_path)'
sftp.put(local_path, remote_path) 
sftp.close()
ssh.close()


















