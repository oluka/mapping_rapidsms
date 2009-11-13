#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.db import models
from reporting.models import Report
from people.models import Person


class PregnantPerson(Person):
    date_last_menses = models.DateField("Date of Last menses", blank=True ,null=True)


class PregnancyReport(Report):
    person = models.ForeignKey(PregnantPerson)


class PreBirthReport(Report):
    person = models.ForeignKey(PregnantPerson)
    pass


class BirthReport(Report):
    person = models.ForeignKey(PregnantPerson)
    weight = models.FloatField(null=True, blank=True)
    date = models.DateField(blank=True, null=True)


class ChildReport(Report):
    person = models.ForeignKey(PregnantPerson)
    weight = models.FloatField(null=True, blank=True)
    muac = models.FloatField(null=True, blank=True)


class Child(Person):
    weight =   models.DecimalField("weight",decimal_places=2,max_digits=6, blank=True ,null=True)
