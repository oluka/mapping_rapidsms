#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.db import models
from django.contrib import admin
import follow.models


for m in models.loading.get_models(follow.models):
    admin.site.register(m)
