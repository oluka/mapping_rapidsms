#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    url(r'^tags$',             views.index),
    url(r'^tags/add$',         views.add_tag,  name="add-tag"),
    url(r'^tags/(?P<pk>\d+)$', views.edit_tag, name="view-tag"),
    
    #url(r'^groups/$',            views.index),
    #url(r'^groups/add$',         views.add_group),
    #url(r'^groups/(?P<pk>\d+)$', views.edit_group),
)
