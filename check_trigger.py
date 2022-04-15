# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:33:42 2018

"""

import os
from get_download_config import Declare
import yaml

CONF_FILE = Declare()
CONF = CONF_FILE.CONF
#path = 'G:\\csdb\\data\\download\\'

def get_trigger(path):
    fnames = []
    for fname in os.listdir(path):
        if fname.endswith('.trg'):
            print("Yes the trigger file is present = ", fname)
            fnames.append(fname)
        else:
            pass
    return fnames

def split_trigger(fname):
    provider, task, date, _ = fname.split(".")
    return provider, task, date


def count_triggers(file_names):
    provider = []
    task = []
    date = []
    for files in file_names:
        provider_name, task_name, date_name = split_trigger(files)
        provider.append(provider_name)
        task.append(task_name)
        date.append(date_name)
    return provider, task, date


def read_all_provider_task_files():
    list_files = []
    for file in os.listdir(CONF_FILE.CONF['Dir']['confdir']):
        if file.endswith("files.yml"):
            list_files.append(file)
    return list_files

def validate_trigger():
    match_file = []
    list_files = read_all_provider_task_files()
    file_names = get_trigger(CONF_FILE.CONF['Folder']['triggerpath'])
    provider, task, date = count_triggers(file_names)
    for i in range(0, len(provider)):
        concate_str = provider[i]+"_"+task[i]+"_files.yml"
        for j in range(0, len(list_files)):
            if concate_str == list_files[j]:
                match_file.append(list_files[j])
            else:
                pass
    return match_file


matched_files = validate_trigger()

def provider_read(matched_files):
    provider_conf = []
    for i in range(0, len(matched_files)):
        full_name = matched_files[i]
        provider_name, _, _ = full_name.split("_")
        conf_file = provider_name + "_conf.yml"
        path = 'C:\\Users\\Xa_dixitan\\Desktop\\CSDB Python Project\\Config_Folder\\'+conf_file
        provider_conf.append(dict(yaml.safe_load(open(path, "r"))))
    return provider_conf

def task_read(matched_files):
    task_conf = []
    for i in range(0, len(matched_files)):
        full_name = matched_files[i]
        provider_name, task_name, _ = full_name.split("_")
        conf_file = provider_name +"_"+ task_name +"_files.yml"
        path = 'C:\\Users\\Xa_dixitan\\Desktop\\CSDB Python Project\\Config_Folder\\'+conf_file
        task_conf.append(dict(yaml.safe_load(open(path, "r"))))
    return task_conf

provider_conf = provider_read(matched_files) #It contains the provider configuration
task_conf = task_read(matched_files) #It contains the task configuration

#I have readed the provider & task files now proceed ahead on coding
# Now next task is to start create a SFTP connection by reading the Providers config
#------------------------------------
import pysftp
import sys
import glob

srv = pysftp.Connection(host="#", username="#",
password="#")

# Download the file from the remote server
for file in glob.glob("*.txt"):
        srv.get(file,'/mnt/sas/ftp_mlb')

# Closes the connection
srv.close()
