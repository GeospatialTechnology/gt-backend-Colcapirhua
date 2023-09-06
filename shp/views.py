from django.db import connection
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .models import  Predio, Manzano, ViasGral
from .serializers import PredioSerializer, ManzanoSerializer, ViasGralSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, LineString, WKTWriter
from django.core.serializers import serialize

# Create your views here.

class PredioViewSet(viewsets.ModelViewSet):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer

class ManzanoViewSet(viewsets.ModelViewSet):
    queryset = Manzano.objects.all()
    serializer_class = ManzanoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields  = ['CODIFICACI']


@api_view(["GET"])
def RecuperarDatosPredio(request, cod_sist):
    try:
        #latitud= request.GET.get("latitud")
        #longitud= request.GET.get("longitud")
        print(cod_sist)

        #point = Point([float(longitud), float(latitud)]) #esta sentencia sirve
        #point=GEOSGeometry('SRID=32719;POINT(float(latitud) float(longitud))')
        #print (point)
       # wkt_w = WKTWriter()
       # wkt_w.write(point)

        #servicios = Predio.objects.filter(geom__contains=point)
        resultado_predios= serialize('geojson',Predio.objects.filter(codsist=cod_sist), geometry_field='geom')
        #print(servicios.query)
        print (resultado_predios)
        #is_inside = Predio.geom.cont
        return JsonResponse(
            #PredioSerializer(servicios, many=True).data,
            {
                "Predios Encontrados": resultado_predios
            },
            safe = False,
            status= 200,
        )
    except Exception as e:
        return JsonResponse( {"message:": str(e)}, status =400)


@api_view(["GET"])
def MazanoBuscar(request, codificacion):
    try:
        print (codificacion)
        resultado_manzanos = serialize('geojson',Manzano.objects.filter(CODIFICACI=codificacion), geometry_field='geom')
        #print(servicios.query)
        print (resultado_manzanos)
        #is_inside = Predio.geom.cont
        return JsonResponse(
            #PredioSerializer(servicios, many=True).data,
            {
                "Manzanos encontrados": resultado_manzanos
            },
            safe = False,
            status= 200,
        )
    except Exception as e:
        return JsonResponse( {"message:": str(e)}, status =400)

@api_view(["GET"])
def ViasGralBuscar(request, buscar_nombre):
    try:
        print (buscar_nombre)
        resultado_vias = serialize('geojson',ViasGral.objects.filter(nombre__contains=buscar_nombre), geometry_field='geom')
        #print(servicios.query)
        print (resultado_vias)
        #is_inside = Predio.geom.cont
        return JsonResponse(
            #PredioSerializer(servicios, many=True).data,
            {
                "Vias encontradas": resultado_vias
            },
            safe = False,
            status= 200,
        )
    except Exception as e:
        return JsonResponse( {"message:": str(e)}, status =400)


