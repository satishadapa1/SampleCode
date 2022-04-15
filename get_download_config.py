# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 16:36:11 2018

"""

import platform
import sys
from sqlalchemy.ext.declarative import declarative_base
import yaml
import os
from os.path import join
import time
from os import path
import logging

# Finding the conf file from the system location for downloader credentials
LOGGER = logging.getLogger(__name__)

class Declare(object):
    """
    Class Declare changes the name of some column names in Dataframe
    """
    def get_config_loc(filename):
        lookfor = filename
        for root, dirs, files in os.walk('C:\\'):
#            print( "searching", root)
            if lookfor in files:
                print( "found: %s" % join(root, lookfor))
                get_path = join(root, lookfor)
                break
        return get_path
    CONF_LOCATION = get_config_loc("Downloader_config.yml")
    CONF = yaml.safe_load(open(CONF_LOCATION, "r"))

    def find_platform():
        """
        Method find_platform will find the platform of the current system on
        which Daily Loader is executed & if it is not windows/Linux then it will
        stop the Daily Loader Execution
        """
        if platform.system() == "Windows":
            start_location = "C:"
            LOGGER.info("The current platform is Windows with start_location =  %s", start_location)
        elif platform.system() == "Linux":
            start_location = "/Volumes/dfsshares"
            LOGGER.info("The current platform is Linux with start_location =  %s", start_location)
        else:
            LOGGER.error("Current platform is not a Linux or Windows")
            sys.exit()
        return  start_location


    def clean_up(number_of_days, folder_path):
        """
        Removes files from the passed in path that are older than or equal
        to the number_of_days
        """
        time_in_secs = time.time() - (number_of_days * 24 * 60 * 60)
        for j in range(len(folder_path)):
            for root, dirs, files in os.walk(folder_path[j], topdown=False):
                for file_ in files:
                    full_path = os.path.join(root, file_)
                    stat = os.stat(full_path)

                    if stat.st_mtime <= time_in_secs:
                        os.remove(full_path)

                if not os.listdir(root):
                    os.rmdir(root)
        return LOGGER.info("Clean up of All folders is done older files and folders are deleted")


    def is_folder_exist(folder_path):
        """
        Method is_folder_exist will find the folders which are required & check
        if they are present if not then it will create a new folder.
        """
        for j in range(len(folder_path)):
            if not os.path.exists(folder_path[j]):
                os.makedirs(folder_path[j])
                LOGGER.info("Created folder_path is = %s", folder_path[j])
            else:
                LOGGER.info("Folder is already present at location = %s", folder_path[j])
        return  LOGGER.info("All the folders are created/located successfully")

# here clean_up method is taking the number of days older files user want to delete
#    check = clean_up(4, folder_path)
#    folder_status = is_folder_exist(folder_path)
#   
