#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    url(r'^follow$',             views.index),
  #  url(r'^follow/add$',         views.add_follow,  name="add-follow"),
  #  url(r'^follow/(?P<pk>\d+)$', views.edit_follow, name="view-follow"),
    
    #url(r'^groups/$',            views.index),
    #url(r'^groups/add$',         views.add_group),
    #url(r'^groups/(?P<pk>\d+)$', views.edit_group),
)
