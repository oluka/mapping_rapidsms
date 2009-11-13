#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from rapidsms.djangoproject.related import related_objects, with_related_objects
from rapidsms.djangoproject.utils import render_to_response, paginated
from reporters.utils import insert_via_querydict, update_via_querydict
from locations.models import *




@require_GET
def index(req):    
   
    return render_to_response(req,
        "mapping/index.html", {
        "all_locations": Location.objects.all().order_by("code"),
        "location_types": LocationType.objects.all() 
        })
def export_points(request):
    from django.http import HttpResponse
    x="lat    lon    title    description    icon </br>  "
    x+="\n30.06435 -2.04304 test describe  http://localhost:8000/Media/symbols/airport.png "
    
        
    
    return HttpResponse(x)