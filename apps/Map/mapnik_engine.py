# Django 
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

# Mapnik
import mapnik
from copy import deepcopy

map_cache = None

class MapCache(object):
    def __init__(self,mapfile,srs):
        self.map = mapnik.Map(1,1)
        mapnik.load_map(self.map,mapfile)
        self.map.srs = srs


# its easy to do per user permissions:
#
# if not request.user.has_perm(app.model):
#    raise Http404
#
# or globally protect map services to authenticated users
# @login_required
# def tile_serving_view(request):


def wms(request):
    global map_cache
    w,h = int(request.GET['WIDTH']), int(request.GET['HEIGHT'])
    mime = request.GET['FORMAT']
    p = mapnik.Projection('%s' % str("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs") )
    mapfile = settings.MAPNIK_MAPFILE
    if not map_cache:
        map_cache = MapCache(mapfile,p.params())
    env = map(float,request.GET['BBOX'].split(','))
    # note: must be run without threading until #345 is closed
    # http://trac.mapnik.org/ticket/345
    # tile = deepcopy(map_cache.map)
    tile = map_cache.map
    tile.buffer_size = 128
    try:
        tile.resize(w,h)
    except:
        tile.width = w
        tile.height = h
    tile.zoom_to_box(mapnik.Envelope(*env))
    draw = mapnik.Image(tile.width, tile.height)
    mapnik.render(tile,draw)
    image = draw.tostring(str(mime.split('/')[1]))
    response = HttpResponse()
    response['Content-length'] = len(image)
    response['Content-Type'] = mime
    response.write(image)
    return response