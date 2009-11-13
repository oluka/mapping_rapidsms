#from django.db import models
from django.contrib.gis.db import models


class UgandaAdministrative(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=24)
    admin_leve = models.CharField(max_length=1)
    the_geom = models.LineStringField(srid=-1)
    objects = models.GeoManager()
    class Meta:
        db_table = u'uganda_administrative'

class UgandaNatural(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    type = models.CharField(max_length=6)
    the_geom = models.PolygonField(srid=-1)
    objects = models.GeoManager()
    class Meta:
        db_table = u'uganda_natural'

class UgandaWater(models.Model):
    gid = models.IntegerField(primary_key=True)
    natural = models.CharField(max_length=9)
    name = models.CharField(max_length=10)
    the_geom = models.PolygonField(srid=-1)
    objects = models.GeoManager()
    class Meta:
        db_table = u'uganda_water'

class GeometryColumns(models.Model):
    f_table_catalog = models.CharField(max_length=256)
    f_table_schema = models.CharField(max_length=256)
    f_table_name = models.CharField(max_length=256)
    f_geometry_column = models.CharField(max_length=256)
    coord_dimension = models.IntegerField()
    srid = models.IntegerField()
    type = models.CharField(max_length=30)
    class Meta:
        db_table = u'geometry_columns'

class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256)
    auth_srid = models.IntegerField()
    srtext = models.CharField(max_length=2048)
    proj4text = models.CharField(max_length=2048)
    class Meta:
        db_table = u'spatial_ref_sys'

class ShorelineA(models.Model):
    gid = models.IntegerField(primary_key=True)
    error = models.SmallIntegerField()
    tile_x = models.SmallIntegerField()
    tile_y = models.SmallIntegerField()
    way = models.MultiPolygonField(srid=900913)
    objects = models.GeoManager()
    class Meta:
        db_table = u'shoreline_a'

class UgandaCoastline(models.Model):
    gid = models.IntegerField(primary_key=True)
    natural = models.CharField(max_length=9)
    name = models.CharField(max_length=26)
    the_geom = models.LineStringField(srid=-1)
    objects = models.GeoManager()
    class Meta:
        db_table = u'uganda_coastline'


