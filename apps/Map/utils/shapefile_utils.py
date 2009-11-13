# @author mossplix

import os
import struct
from django.contrib.gis.gdal import Envelope, OGRGeometry
from django.conf import settings


"""  this module contains various methods for dealing with shapefiles
it contains helpers to import """
def shapefiles(dirname,files):
    for file in files:
        fullname =os.path.join(dirname,file)
        if os.path.isfile(fullname):
            base,ext=fullname.rsplit('.',1)
            if(ext=="sph"):
                shpfiles.append(fullname)
            
            
def  import_shapefiles(SHAPE_FILES_DIRECTORY):
    """ module to import shapefiles put in a particular directory 4 rendering with mapnik """
    shpfiles=[]
    os.path.walk(SHAPE_FILES_DIRECTORY,shapefiles)
    
    
    pass
def read_shapeindex():
    pass

def shape_index(file):
    pass
