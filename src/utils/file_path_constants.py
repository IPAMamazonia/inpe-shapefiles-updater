import os

ABS_PATH = os.getcwd()
SHAPEFILES_DOWNLOAD_PATH = ABS_PATH+'/shapeFiles/'


def get_zip_file_path():
    print os.listdir(
        SHAPEFILES_DOWNLOAD_PATH)
    return SHAPEFILES_DOWNLOAD_PATH+'/'+os.listdir(
        SHAPEFILES_DOWNLOAD_PATH)[0]


def generate_file_name():

    for name in os.listdir(
            SHAPEFILES_DOWNLOAD_PATH):
        if 'shp' == name[-3:]:
            return SHAPEFILES_DOWNLOAD_PATH+name
