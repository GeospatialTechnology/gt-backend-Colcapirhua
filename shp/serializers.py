from rest_framework import serializers
from .models import Predio, Manzano, ViasGral
from django.contrib.gis.db import models as gis_models #añadido para geo
from django.contrib.gis.db import models


class PredioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predio
        fields = "__all__"
        #fields = ['gid', 'objectid', 'dist', 'codigo', 'codsist','shape_leng','shape_area', 'geom']

class ManzanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manzano
        fields = "__all__"
        #fields = ['OBJECTID', 'Shape_Leng', 'Shape_Area', 'CODIFICACI','geom']

class ViasGralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViasGral
        fields = "__all__"
