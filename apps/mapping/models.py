#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re
from django.db import models
from rapidsms.djangoproject.managers import *
from reporters.models import Reporter

class Mapping(models.Model):
    """   add comments here """
    alias      = models.CharField(max_length=20, unique=True)
    number     = models.IntegerField(max_length=10,unique=False)
    
