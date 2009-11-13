#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import os
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^tree$', views.index),
    
    (r'^tree/data$', views.data),
    (r'^tree/data/(?P<id>\d+)$', views.data),
    
    (r'^tree/data/export$', views.export),
    (r'^tree/data/export/(?P<id>\d+)$', views.export)
)
