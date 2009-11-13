# Django 
from django.conf import settings
from django.http import HttpResponse

# Nik2img
from nik2img import Map

def get(r, key):
  ''' Get the dictionary key or return None '''
  if r.has_key(key):
      return r[key]
  elif r.has_key(key.upper()):
      return r[key.upper()]
  else: return None

def wms(request):
    w,h = int(request.GET['WIDTH']), int(request.GET['HEIGHT'])
    mime = request.GET['FORMAT']
    p = Projection('+init=%s' % str(request.GET['SRS']) )
    wms = Map(w,h,p.params())
    load_map(wms, settings.MAPNIK_MAPFILE)
    env = map(float,request.GET['BBOX'].split(','))
    bbox = Envelope(*env)
    wms.zoom_to_box(bbox)
    draw = Image(wms.width, wms.height)
    render(wms,draw)
    image = draw.tostring(str(mime.replace('image/','')))
    response = HttpResponse()
    response['Content-length'] = len(image)
    response['Content-Type'] = mime
    response.write(image)
    return response