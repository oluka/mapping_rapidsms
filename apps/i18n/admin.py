#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.contrib import admin
from models import Language, Token


admin.site.register(Language)
admin.site.register(Token)
