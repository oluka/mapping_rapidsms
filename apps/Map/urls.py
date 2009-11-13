from django.conf.urls.defaults import *
from Map.views import *
from django.conf import settings
from Map.tilecache_engine import *
from Map.mapnik_engine import *



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
     
     
     #(r'^wms$',wms),
      #(r'^homer$',homer),
      (r'^mapping$', index),
      (r'^tilecache/$', tms),
       (r'^mapnik/$', wms),
      
      (r'^map/(?P<method>\w+)/(?P<engine>\w+)/$', map_client),
    (r'^cache/tilecache/(.*)$','django.views.static.serve',{'document_root': settings.DISK_CACHE, 'show_indexes': True}),
    (r'^(?P<method>\w+)/(?P<engine>\w+)/(.*)$', tiles_dispatcher), 
    ( r'^tilecache/(?P<version>\d{1,2}\.\d{1,3})/(?P<layername>[a-z]{1,64})/(?P<z>\d{1,10})/(?P<x>\d{1,10}),(?P<y>\d{1,10})\.(?P<extension>(?:png|jpg|gif))',wms),
    
     (r'^Media/(?P<path>.*)', 'django.views.static.serve',\
     {'document_root': '/home/mugisha/projects/django-projects/rapidsms_geo/Media/'}),
)
