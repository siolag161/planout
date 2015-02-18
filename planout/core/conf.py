from django.conf import settings
from PIL import Image

#from appconf import AppConf

class BaseImageFieldConf(object):
    DEFAULT_SIZE = 80
    RESIZE_METHOD = Image.ANTIALIAS
    RESIZED = True
    
    WIDTH = 400
    HEIGH = 600    

    FORMAT = 'jpg'
    
    STORAGE_DIR = 'image'
    STORAGE_PARAMS = {}
    DEFAULT_URL = 'image/default/default.jpg'
    MAX_SIZE = 1024 * 1024
    HASH_FILENAMES = False
    HASH_DIRNAMES = False
    ALLOWED_FILE_EXTS = None
    STORAGE = settings.DEFAULT_FILE_STORAGE
    CLEANUP_DELETED = False



    
