# 
#@author mossplix
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, \
    HttpResponseNotAllowed, Http404, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.db import connection
from TileCache.Service import Service, Request, TileCacheException
from TileCache.Caches.Disk import Disk
import TileCache.Layer as Layer
import re
from mapnik import *
# Django 
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from TileCache.Service import Service
from TileCache.Caches.Disk import Disk
from TileCache.Layers import Mapnik as MN

# Mapnik
import mapnik
from copy import deepcopy

map_cache = None
my_service = Service(Disk("%s" % settings.DISK_CACHE),
  {"world" : MN.Mapnik( "world", settings.MAPNIK_MAPFILE, extension = "png" ),}
  )
request_pat = r'/(?P<version>\d{1,2}\.\d{1,3})/(?P<layername>[a-z]{1,64})/(?P<z>\d{1,10})/(?P<x>\d{1,10}),(?P<y>\d{1,10})\.(?P<extension>(?:png|jpg|gif))'
request_re = re.compile(request_pat)

def main(request):
    return render_to_response('index.html')
def homer(request):
    return render_to_response('index.html')


from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext


engines = {}
methods = {}
  
try:
    import mapnik_engine
    engines['mapnik'] = mapnik_engine
    methods['mapnik'] = ['wms','gmaps']
except ImportError, E:
    print 'Unable to import tile engine:\n %s' % E

try:
    import nik2img_engine
    engines['nik2img'] = mapnik_engine
    methods['nik2img'] = ['wms']
except ImportError, E:
    print 'Unable to import tile engine:\n %s' % E
    
try:
    import mapscript_engine
    engines['mapscript'] = mapscript_engine
    methods['mapscript'] = ['wms']
except ImportError, E:
    print 'Unable to import tile engine:\n %s' % E

try:
    import mapserv_engine
    engines['mapserv'] = mapserv_engine
    methods['mapserv'] = ['wms']
except ImportError, E:
    print 'Unable to import tile engine:\n %s' % E

try:
    import tilecache_engine
    engines['tilecache'] = tilecache_engine
    methods['tilecache'] = ['wms','tms','tms-force','cache']
except ImportError, E:
    print 'Unable to import tile engine:\n %s' % E


# TODO weave dicts into auto index html of possible pages
def home(request):
    return render_to_response('index.html', RequestContext(request,{}))

def tiles_dispatcher(request, method, engine):
    global engines
    global methods
    tile_engine = engines.get(engine)
    responder = getattr(tile_engine,method)
    if tile_engine and method in methods[engine]:
      return getattr(tile_engine,method)(request)

def map_client(request, method, engine):
    return render_to_response('index.html',
        RequestContext(request, {'method':method,'engine':engine} ) )
    
