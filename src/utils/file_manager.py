import os
import zipfile
import shutil
import re
from file_path_constants import SHAPEFILES_DOWNLOAD_PATH

def remove_folder_and_shapeFiles():

    shutil.rmtree(SHAPEFILES_DOWNLOAD_PATH)


def delete_and_create_folder():

    if os.path.exists(SHAPEFILES_DOWNLOAD_PATH):
        remove_folder_and_shapeFiles()
        os.makedirs(SHAPEFILES_DOWNLOAD_PATH)
        
def extract_zip(path_to_zip_file):
    
    z = zipfile.ZipFile(path_to_zip_file,'r')
    z.extractall(path=SHAPEFILES_DOWNLOAD_PATH)
    z.close()


