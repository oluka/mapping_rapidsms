#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.contrib import admin
from rwanda.models import *


admin.site.register(PregnantPerson)
admin.site.register(PregnancyReport)
admin.site.register(PreBirthReport)
admin.site.register(BirthReport)
admin.site.register(ChildReport)
#admin.site.register(PersistantConnection)
