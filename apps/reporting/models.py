#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.db import models
from tags.models import Tag


class Report(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        pass
