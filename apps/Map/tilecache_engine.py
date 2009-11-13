# Django 
from django.conf import settings
from django.http import HttpResponse
import re

# TileCache 
import TileCache
from TileCache.Service import Service, Request, TileCacheException
from TileCache.Caches.Disk import Disk
from TileCache.Layers import Mapnik as MN
import TileCache.Layer as Layer
#from TileCache.Layers import WMS
#from TileCache.Layers import MapServer as MS
request_pat = r'/(?P<version>\d{1,2}\.\d{1,3})/(?P<layername>[a-z]{1,64})/(?P<z>\d{1,10})/(?P<x>\d{1,10}),(?P<y>\d{1,10})\.(?P<extension>(?:png|jpg|gif))'
request_re = re.compile(request_pat)
s = TileCache.Service.load(settings.TILECACHE_CONF)

my_service = Service(Disk("%s" % settings.DISK_CACHE),
  {"world" : MN.Mapnik( "world", settings.MAPNIK_MAPFILE, extension = "png" ),}
  )
s
def tms(request):
    path_info = request.META["PATH_INFO"]
    host  = "http://" + request.META["HTTP_HOST"] + '/tiles/'
    # 'http://localhost:8000' vs. http://localhost/tilecache/tilecache.cgi
    # hack to pull off url prefix so tilecache interprets path_info correctly
    path_info = path_info.lstrip('/tms/tilecache')
    format, image = s.dispatchRequest( request.GET, path_info, "GET", host )
    response = HttpResponse()
    response['Content-Type'] = format
    response.write(image)
    return response

#def cache(request):
    #pass # static serve...
