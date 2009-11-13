# Django 
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext

# MapServer 'python-mapscript'
from mapscript import mapObj, OWSRequest

def wms(request):
    from mapscript import mapObj, OWSRequest
    wms = mapObj(settings.MAPSERVER_MAPFILE)
    req = OWSRequest()
    mime = request.GET['FORMAT']
    req.setParameter("bbox", request.GET['BBOX'])
    req.setParameter("width", request.GET['WIDTH'])
    req.setParameter("height", request.GET['HEIGHT'])
    req.setParameter("srs", request.GET['SRS'])
    req.setParameter("format", mime)
    req.setParameter("layers", request.GET['LAYERS'])
    req.setParameter("styles", request.GET['STYLES'])
    req.setParameter("request", "GetMap")
    wms.loadOWSParameters(req)
    image = wms.draw().getBytes()
    response = HttpResponse()
    response['Content-length'] = len(image)
    response['Content-Type'] = mime
    response.write(image)
    return response

def wms_(request):
    from mapscript import mapObj
    mapobject = mapObj(settings.MAPSERVER_MAPFILE)
    mapimage = mapobject.draw()
    image = mapimage.getBytes()
    response = HttpResponse()
    response['Content-length'] = len(image)
    response['Content-Type'] = 'image/png'
    response.write(image)
    return response


