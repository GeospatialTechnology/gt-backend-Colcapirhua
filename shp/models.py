from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement
from geo.Geoserver import Geoserver
from pathlib import Path
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db import models


# Create your models here.

#Modelamiento tabla Predios
class Predio(models.Model):
    gid = models.AutoField(primary_key=True)
    objectid = models.IntegerField(blank=True, null=True)
    dist = models.CharField(max_length=2, blank=True, null=True)
    codigo = models.CharField(max_length=50, blank=True, null=True)
    codsist = models.CharField(max_length=50, blank=True, null=True)
    shape_leng = models.FloatField(null=True)
    shape_area = models.FloatField(null=True)
    geom = gis_models.MultiPolygonField(db_column='geom')

    def __str__(self):
        return self.gid

    class Meta:
        managed = False
        db_table = 'PREDIOS'

#Modelamiento tabla Manzanos
class Manzano(models.Model):
    OBJECTID = models.BigIntegerField(db_column='OBJECTID', blank=True, null=True)  # Field name made lowercase.
    Shape_Leng = models.FloatField(db_column='Shape_Leng', blank=True, null=True)  # Field name made lowercase.
    Shape_Area = models.FloatField(db_column='Shape_Area', blank=True, null=True)  # Field name made lowercase.
    CODIFICACI = models.TextField(db_column='CODIFICACI', blank=True, null=True)  # Field name made lowercase.
    geom = gis_models.MultiPolygonField()

    def __str__(self):
        return self.OBJECTID

    class Meta:
        managed = False
        db_table = 'MANZANOS'

#Modelamiento tabla Vias Gral
class ViasGral(models.Model):
    gid = models.BigIntegerField(db_column='gid', blank=False, null=False, primary_key=True)
    id = models.BigIntegerField(db_column='id', blank=True, null=True)  # Field name made lowercase.
    nombre = models.TextField(db_column='nombre', blank=True, null=True)  # Field name made lowercase.
    objectid = models.BigIntegerField(db_column='objectid', blank=True, null=True)  # Field name made lowercase.
    perfil = models.TextField(db_column='perfil', blank=True, null=True)  # Field name made lowercase.
    categoria = models.TextField(db_column='categoria', blank=True, null=True)  # Field name made lowercase.
    shape_leng = models.FloatField(db_column='shape_leng', blank=True, null=True)  # Field name made lowercase.
    geom =  gis_models.MultiPolygonField(db_column='geom')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'VIAS_GRAL'
