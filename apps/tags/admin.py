#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.contrib import admin
from models import *


class TagAdmin(admin.ModelAdmin):
    list_display=("code", "title")


admin.site.register(Tag, TagAdmin)
