from asyncio.windows_events import NULL
from doctest import ELLIPSIS_MARKER
from sqlite3 import enable_shared_cache
import string
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect
#from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django import forms
#from .forms import SubmitForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from pyparsing import Char
from .models import (ClassificationResidentialBuilding, ClassificationNotResidentialBuilding, NewBuildingDemand, NewBuildingEnergyConsume, NewBuildingEmissions, ExistingBuildingDemand, ExistingBuildingEnergyConsume, ExistingBuildingEmissions, NewBuldingDemandDispersions, NewBuldingEnergyAndEmissionsDispersions, ExistingBuldingDemandDispersions, ExistingBuldingEnergyAndEmissionsDispersions,User,File,Calcul)
from .serializers import (ClassificationResidentialBuildingSerializer, ClassificationNotResidentialBuildingSerializer, NewBuildingDemandSerializer, NewBuildingEnergyConsumeSerializer, NewBuildingEmissionsSerializer, ExistingBuildingDemandSerializer, ExistingBuildingEnergyConsumeSerializer, ExistingBuildingEmissionsSerializer, NewBuldingDemandDispersionsSerializer, NewBuldingEnergyAndEmissionsDispersionsSerializer, ExistingBuldingDemandDispersionsSerializer, ExistingBuldingEnergyAndEmissionsDispersionsSerializer, UserSerializer,FileSerializer,CalculSerializer)
from django.db.models import Case, When
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg import openapi
#from allauth.socialaccount import providers
#from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from django.shortcuts import get_object_or_404
#from allauth.socialaccount.providers.facebook.views import fb_complete_login
#from allauth.socialaccount.helpers import complete_social_login
#import allauth.account
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser

# Create your views here.

class ResidentialBuildingClassificationSet(ViewSet):
    parser_classes = [JSONParser]
    #Introducir valores de la clasificacion de edificios nuevos
    @swagger_auto_schema(
        operation_description='Crea les diferents classificacions per a edificis nous amb el valors de la classificacio',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'classificacio': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la lletra corresponent a la classificacio',
                                    example= 'A'),
                'min_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C1 que la classificacio pot obtenir',
                                    example= '1.5'),
                'max_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C1 que la classificacio pot obtenir',
                                    example= '2.5'),
                'min_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C2 que la classificacio pot obtenir',
                                    example= '1.7'),
                'max_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C2 que la classificacio pot obtenir',
                                    example= '1.9'),
            },
            required=["classificacio", "min_C1", "max_C1"],
        ),
        responses= {404:'No s\'ha pogut crear la classificacio', 201: ClassificationResidentialBuildingSerializer})
    def create(self, request):
        c = ClassificationResidentialBuilding(calification = request.data['classificacio'], min_C1 = request.data['min_C1'], max_C1 = request.data['max_C1'],min_C2 = request.data['min_C2'],max_C2 = request.data['max_C2'])
        if c.DoesNotExist:
            return Response ('No s\'ha pogut crear la classificacio', 404)
        else:
            serializer = ClassificationResidentialBuildingSerializer(c)
            return Response(serializer.data, 201)

#Actualizar los valores de una classificacion para un edificio nuevo
    @swagger_auto_schema(
        operation_description='Actualitza els valors de les classificacions per a edificis nous',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'classificacio': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la lletra corresponent a la classificacio',
                                    example= 'A'),
                'min_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C1 que la classificacio pot obtenir',
                                    example= '1.5'),
                'max_C1': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C1 que la classificacio pot obtenir',
                                    example= '2.5'),
                'min_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C2 que la classificacio pot obtenir',
                                    example= '1.7'),
                'max_C2': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C2 que la classificacio pot obtenir',
                                    example= '1.9'),
            },
            required=["classificacio", "min_C1", "max_C1"],
        ),
        responses= {404: 'Classificacio no actualitzada correctament', 200: ClassificationResidentialBuildingSerializer})
    def update(self, request, classification: string = None):
        c = ClassificationResidentialBuilding.objects.get(calification = request.data['classificacio'])
        if c.exisits:
            c.min_C1 = request.data['min_C1']
            c.max_C1 = request.data['max_C1']
            c.min_C2 = request.data['min_C2']
            c.max_C2 = request.data['max_C2']
            c.save()
            #queryset = ClassificationResidentialBuilding.objects.get(classification = c.classification)
            serializer = ClassificationResidentialBuildingSerializer(c)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar la classificacio', 404)

    #Obtener la clasificacion rerlacionada a un valor que se envia para un edificio nuevo
    @swagger_auto_schema(
        operation_description='Obtè el valor de la classificacio per un valor introduit d\'un edifici residencial',
        manual_parameters=[
            openapi.Parameter(
                'C1',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True,
                description='Proporciona el valor de C1 calculat',
            ),
            openapi.Parameter(
                'C2',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True,
                description='Proporciona el valor de C2 calculat',
            ),
        ],
        responses= {200: openapi.Schema(type = openapi.TYPE_STRING, description='Categoria pertanyent als valors proporcionats'), 204: 'no s\'ha trobat cap classiificacio per aquests valors'})
    def retrieve(self, request, classification_id: string = None):
        classification = ClassificationResidentialBuilding.objects.filter(min_C1__lt = request.data['C1'], max_C1__gt=request.data['C1']).count()
        if classification > 0:
            if request.data['C2'] == NULL:
                classification = ClassificationResidentialBuilding.objects.filter(min_C1__lt = request.data['C1'], max_C1__gt=request.data['C1']).values('classification')
                serializer = ClassificationResidentialBuildingSerializer(classification)
                return(Response.data, 200)
            else:
                classification = ClassificationResidentialBuilding.objects.filter(min_C1__lt = request.data['C1'], max_C1__gt = request.data['C1'], min_C2__lt =request.data['C2'], max_C2__gt = request.data['C2']).values('classification')
                serializer = ClassificationResidentialBuildingSerializer(classification)
                return(Response.data, 200)
        else:
            return Response ('no s\'ha trobat cap classificacio per aquests valor', 204)

class NonResidentialBuildingSet(ViewSet):
    parser_classes = [JSONParser]

    #Introducir valores de la clasificacion de edificios de uso no residencial
    @swagger_auto_schema(
        operation_description='Crea les diferents classificacions per a edificis d\'ús no residencial amb el valors de la classificacio',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'classificacio': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la lletra corresponent a la classificacio',
                                    example= 'A'),
                'min_C': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C que la classificacio pot obtenir',
                                    example= '1.5'),
                'max_C': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C que la classificacio pot obtenir',
                                    example= '2.5'),
            },
            required=["classificacio", "min_C", "max_C"],
        ),
        responses= {404:'No s\'ha pogut crear la classificacio', 201: ClassificationNotResidentialBuildingSerializer})    
        
    def create(self, request):
        c = ClassificationNotResidentialBuilding(classification = request.data['classificacio'], min_C = request.data['min_C'], max_C = request.data['max_C'])
        if c.DoesNotExist:
            return Response ('No s\'ha pogut crear la classificacio', 404)
        else:
            serializer = ClassificationNotResidentialBuildingSerializer(c)
            return Response(serializer.data)


    #Actualizar los valores de una classificacion para un edificio existente
    @swagger_auto_schema(
        operation_description='Actualitza els valors de les classificacions per a edificis existents',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'classificacio': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la lletra corresponent a la classificacio',
                                    example= 'A'),
                'min_C': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor minim de C que la classificacio pot obtenir',
                                    example= '1.5'),
                'max_C': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor maxim de C que la classificacio pot obtenir',
                                    example= '2.5'),
            },
            required=["classificacio", "min_C", "max_C"],
        ),
        responses= {404:'No s\'ha pogut crear la classificacio', 200: ClassificationNotResidentialBuildingSerializer})
    
    def update(self, request, pk=None):
        c = ClassificationNotResidentialBuilding.object.get(classification = request.data['classificacio'])
        if c.exists:
            c.min_C = request.data['min_C']
            c.max_C = request.data['max_C']
            c.save()
            #queryset = ClassificationResidentialBuilding.objects.get(classification = c.classification)
            serializer = ClassificationNotResidentialBuildingSerializer(c)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar la classificacio', 404)


    #Obtener la clasificacion rerlacionada a un valor que se envia para un edificio existente
    @swagger_auto_schema(
        operation_description='Obte el valor de la classificacio per al valor indicat',
        manual_parameters=[
            openapi.Parameter(
                'C',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True,
                description='Proporciona el valor de C calculat',
            ),
        ],
            responses= {401: 'No has proporcionat cap API key', 200: openapi.Schema(type = openapi.TYPE_STRING, description='Categoria pertanyent al valor proporcionat')})
    def retrieve(self, request, pk=None):
        classification = ClassificationNotResidentialBuilding.objects.filter(min_C__lt = request.data['C'], max_C__gt=request.data['C']).count()
        if classification > 0:
            classification = ClassificationNotResidentialBuilding.objects.filter(min_C__lt = request.data['C'], max_C__gt=request.data['C']).values('classification')
            serializer = ClassificationNotResidentialBuildingSerializer(classification)
            return(Response.data, 200)
        else:
            return Response ('no s\'ha trobat cap classificacio per aquests valors', 204)
        

class NewBuildingDemandSet(ViewSet):
    parser_classes = [JSONParser]

    #Introducir valores de la demanda
    @swagger_auto_schema(
        operation_description='Crea els valors mitjans de demanda de calefaccio i refrigeracio per un edifici nou', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, la zona climatica i els valors de calefaccion i refrigeracio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de refrigeracio',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration"],
        ),
        responses= {404: 'demanda de valors no creada', 201: NewBuildingDemandSerializer})
    def create(self, request):
        i_r = NewBuildingDemand(building_type = request.data['type'], climatic_zone = request.data['climatic_zone'], heating_mean = request.data['heating'], refrigeration = request.data['refrigeration'])
        if i_r.DoesNotExist:
            return Response('No s\'ha pogut crear correctament', 404)
        else:
            serializer = NewBuildingDemandSerializer(i_r)
            return Response(serializer.data, 201)


    #Actualizar valores de la demanda
    @swagger_auto_schema(
        operation_description='Actualitza la mitjana de la demanda de calefaccio i refrigeracio per una zona climatica i tipus d\'edifici',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, zona climatica i els valors de refrigeracio i calefaccio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de refrigeracio',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration"],
        ),
        responses= {404: 'Demanda no trobada', 200: NewBuildingDemandSerializer}) 
    def update(self, request, pk=None):
        d = NewBuildingDemand.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.heating_mean = request.data['heating']
            d.refrigeration = request.data['refrigeration']
            d.save()
            serializer = NewBuildingDemandSerializer(d)
            return Response(serializer.data)
        else:
            return Response('No s\'ha pogut actualitzar la demanda', 404)

    #Obtener valores de la demanda
    @swagger_auto_schema(
        operation_description='Obte el valor mitja de la metricaque es vol obtenir de la demanda', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
            openapi.Parameter(
                'demand',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Proporciona la metrica de la que es vol obternir la demanda',
            ),
        ],
        responses= {204: 'Demanda no trobada', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        if request.data['demand'] == 0:
            d = NewBuildingDemand.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('heating_mean')
        else:
            d = NewBuildingDemand.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('refrigeration')
        
        if d.exists:
            serializer = NewBuildingDemandSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut trobar la demanda', 204)

class NewBuildingEnergyConsumptionSet(ViewSet):
    parser_classes = [JSONParser]

    #Introducir valores de la energia
    @swagger_auto_schema(
        operation_description='Crea els valors mitjans d\'energia consumida de calefaccio, refrigeracio i aigua corrent sanitaria per un edifici nou', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, la zona climatica i els valors de calefaccion i refrigeracio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'ha pogut crear el consum', 201: NewBuildingEnergyConsumeSerializer})
    def create(self, request):
        i_r = NewBuildingEnergyConsume(building_type = request.data['type'], climatic_zone = request.data['climatic_zone'], heating_mean = request.data['heating'], refrigeration = request.data['refrigeration'], ACS = request.data['ACS'])
        if i_r.DoesNotExist:
            return Response('No s\'ha pogut crear el consum', 404)
        else:
            serializer = NewBuildingEnergyConsumeSerializer(i_r)
            return Response(serializer.data, 201)

    #Actualizar valores de la energia
    @swagger_auto_schema(
        operation_description='Actualitza la mitjana d\'energia consumida de calefaccio, refrigeracio i aigua corrent sanitaria per una zona climatica i tipus d\'edifici',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, zona climatica i els valors de refrigeracio, calefaccio i aigua corrent sanitaria',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar el consum d\'energia', 200: NewBuildingEnergyConsumeSerializer})
    def update(self, request, pk=None):
        d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.heating_mean = request.data['heating']
            d.refrigeration = request.data['refrigeration']
            d.ACS = request.data['ACS'];
            d.save()
            serializer = NewBuildingEnergyConsumeSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar el consum d\'energia', 404)

    #Obtener valores de la energia
    @swagger_auto_schema(
        operation_description='Like Contribution', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
            openapi.Parameter(
                'demand',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Proporciona la metrica de la que es vol obternir la demanda',
            ),
        ],
        responses= {204:'No s\'ha trobat cap consum amb aquestes dades', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        if request.data['demand'] == 0:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('heating_mean')
        elif request.data['demand'] == 1:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('refrigeration')
        elif request.data['demand'] == 2:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('ACS')    
        if d.exists:
            serializer = NewBuildingEnergyConsumeSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha trobat cap consum amb aquestes dades', 204)

class NewBuildingEmissionsSet(ViewSet):
    parser_classes = [JSONParser]
    
    #Introducir valores de la emisiones
    @swagger_auto_schema(
        operation_description='Crea els valors mitjans d\'emissions de calefaccio, refrigeracio i aigua corrent sanitaria per un edifici nou',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona la lletra de la classificacio i les diferents metriques de classificacio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'ha pogut crear l\'emissio', 200: NewBuildingEmissionsSerializer})
    def create(self, request):
        i_r = NewBuildingEmissions(building_type = request.data['type'], climatic_zone = request.data['climatic_zone'], heating_mean = request.data['heating'], refrigeration = request.data['refrigeration'], ACS = request.data['ACS'])
        if i_r.DoesNotExist:
            return Response('No s\'ha pogut crear l\'emissio', 404)
        else:
            serializer = NewBuildingEmissionsSerializer(i_r)
            return Response(serializer.data, 200)

    #Actualizar valores de la emisiones
    @swagger_auto_schema(
        operation_description='Actualitza la informacio de les emissions', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de les emissions produides per la calefaccio, refrigeracio i aigua corrent sanitaria',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar l\'emissio', 200: NewBuildingEmissionsSerializer})
    def update(self, request, pk=None):
        d = NewBuildingEmissions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.heating_mean = request.data['heating']
            d.refrigeration = request.data['refrigeration']
            d.ACS = request.data['ACS'];
            d.save()
            serializer = NewBuildingEmissionsSerializer(d)
            return Response(serializer.data)
        else:
            return Response()
    
    #Obtener valores de la emisiones
    @swagger_auto_schema(
        operation_description='Obte la informacio de les emissions per la metrica indicada',
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
            openapi.Parameter(
                'demand',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Proporciona la metrica de la que es vol obternir la demanda',
            ),
        ],
        responses= {204: 'No s\'ha pogut obtenir el valor de l\'emissio', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        if request.data['demand'] == 0:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('heating_mean')
        elif request.data['demand'] == 1:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('refrigeration')
        elif request.data['demand'] == 2:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('ACS')
        if d.exists:
            serializer = NewBuildingEmissionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut obtenir el valor de l\'emissio', 204)


class ExistingBuildingDemandSet (ViewSet):
    parser_classes = [JSONParser]

    #Introducir valores de la demanda
    @swagger_auto_schema(
        operation_description='Crea un nou registre de la demanda d\'un edifici existent', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de la calefaccio, refrigeracio i aigua sanitaria corrent',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de refrigeracio',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration"],
        ),
        responses= {404: 'No s\'ha pogut crear la demanda', 201: ExistingBuildingDemandSerializer})
    def create(self, request):
        i_r = ExistingBuildingDemand(building_type = request.data['type'], climatic_zone = request.data['climatic_zone'], heating_mean = request.data['heating'], refrigeration = request.data['refrigeration'])
        if i_r.DoesNotExist:
            return Response('No s\'ha pogut crear la demanda', 404)
        else:
            serializer = ExistingBuildingDemandSerializer(i_r)
            return Response(serializer.data, 201)

    #Actualizar valores de la demanda
    @swagger_auto_schema(
        operation_description='Actualitza una demanda',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de les emissions produides per la calefaccio, refrigeracio i aigua corrent sanitaria',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de refrigeracio',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar la demanda', 200: ExistingBuildingDemandSerializer}) 
    def update(self, request, pk=None):
        d = ExistingBuildingDemand.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.heating_mean = request.data['heating']
            d.refrigeration = request.data['refrigeration']
            d.save()
            serializer = ExistingBuildingDemandSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar la demanda', 404)

    #Obtener valores de la demanda
    @swagger_auto_schema(
        operation_description='Obté el valor de la metrica que es vol calcular per un edifici existent', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
            openapi.Parameter(
                'demand',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Proporciona la metrica de la que es vol obternir la demanda',
            ),
        ],
        responses= {204: 'No s\'ha trobat cap demanda', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT)})
    def retrieve(self, request, pk=None):
        if request.data['demand'] == 0:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('heating_mean')
        elif request.data['demand'] == 1:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('refrigeration')
        if d.exists:
            serializer = ExistingBuildingDemandSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha trobat cap demanda', 204)

class ExistingBuildingEnergyConsumptionSet(ViewSet):
    parser_classes = [JSONParser]

    #Introducir valores de la energia
    @swagger_auto_schema(
        operation_description='Crea una classificicacio de l\'energia consumida per un edifici existent', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de les emissions produides per la calefaccio, refrigeracio i aigua corrent sanitaria',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana de la demanda de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'ha pogut crear el consum d\'energia', 201: ExistingBuildingEnergyConsumeSerializer})
    def create(self, request):
        i_r = ExistingBuildingEnergyConsume(building_type = request.data['type'], climatic_zone = request.data['climatic_zone'], heating_mean = request.data['heating'], refrigeration = request.data['refrigeration'], ACS = request.data['ACS'])
        if i_r.DoesNotExist:
            return Response('No s\'ha pogut crear el consum d\'energia', 404)
        else:
            serializer = ExistingBuildingEnergyConsumeSerializer(i_r)
            return Response(serializer.data, 201)

    #Actualizar valores de la energia
    @swagger_auto_schema(
        operation_description='Actualitza un registre del consum d\'energia',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de les emissions produides per la calefaccio i refrigeracio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar el consum d\'energia', 200: ExistingBuildingEnergyConsumeSerializer})
    def update(self, request, pk=None):
        d = ExistingBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.heating_mean = request.data['heating']
            d.refrigeration = request.data['refrigeration']
            d.ACS = request.data['ACS'];
            d.save()
            serializer = ExistingBuildingEnergyConsumeSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar el consum d\'energia', 404)

    #Obtener valores de la energia
    @swagger_auto_schema(
        operation_description='Obté el valor del consum d\'energia per la metrica demanada', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
            openapi.Parameter(
                'demand',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Proporciona la metrica de la que es vol obternir la demanda',
            ),
        ],
        responses= {204: 'No s\'ha pogut obtenir el valor del consum', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        if request.data['demand'] == 0:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('heating_mean')
        elif request.data['demand'] == 1:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('refrigeration')
        elif request.data['demand'] == 2:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('ACS')
        if d.exists:  
            serializer = ExistingBuildingEnergyConsumeSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut obtenir el valor del consum', 204)

class ExistingBuildingEmissionsSet(ViewSet):
    parser_classes = [JSONParser]

    #Introducir valores de la emisiones
    @swagger_auto_schema(
        operation_description='Crea un registre de les emissions per un edifici existent',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de les emissions produides per la calefaccio, refrigeracio i aigua corrent sanitaria',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'han pogut crear les emissions', 200: ExistingBuildingEmissionsSerializer})
    def create(self, request):
        i_r = ExistingBuildingEmissions(building_type = request.data['type'], climatic_zone = request.data['climatic_zone'], heating_mean = request.data['heating'], refrigeration = request.data['refrigeration'], ACS = request.data['ACS'])
        if i_r.DoesNotExist:
            return Response('No s\'han pogut crear les emissions', 404)
        else:
            serializer = ExistingBuildingEmissionsSerializer(i_r)
            return Response(serializer.data, 201)


    #Actualizar valores de la emisiones
    @swagger_auto_schema(
        operation_description='Actualitza els valors de les emissions', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i els valors mitjans de les emissions produides per la calefaccio, refrigeracio i aigua corrent sanitaria',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'heating': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de calefaccio',
                                    example= '1.5'),
                'refrigeration': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de refrigeracio',
                                    example= '2.5'),
                'ACS': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la mitjana del consum d\'energia de agua corrent sanitaria',
                                    example= '2.5'),
            },
            required=["type", "climatic_zone", "heating", "refrigeration", "ACS"],
        ),
        responses= {404: 'No s\'han pogut actualitzar les emissions', 200: ExistingBuildingEmissionsSerializer})
    def update(self, request, pk=None):
        d = ExistingBuildingEmissions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.heating_mean = request.data['heating']
            d.refrigeration = request.data['refrigeration']
            d.ACS = request.data['ACS'];
            d.save()
            serializer = ExistingBuildingEmissionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'han pogut actualitzar les emissions', 404)
    
    #Obtener valores de la emisiones
    @swagger_auto_schema(
        operation_description='Obté el valor de les emissions per la metrica demanada',
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
            openapi.Parameter(
                'demand',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Proporciona la metrica de la que es vol obternir la demanda',
            ),
        ],
        responses= {204: 'No s\'han trobat emssions', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        if request.data['demand'] == 0:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('heating_mean')
        elif request.data['demand'] == 1:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('refrigeration')
        elif request.data['demand'] == 2:
            d = NewBuildingEnergyConsume.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('ACS')
        if d.exists:
            serializer = ExistingBuildingEmissionsSerializer(d)
            return Response(serializer.data)
        else:
            return Response('No s\'han trobat emissions', 204)


class NewBuildingDemandDispersionsSet (ViewSet):
    parser_classes = [JSONParser]

     #Introducir valores de la dispersion
    @swagger_auto_schema(
        operation_description='Crea les dispersions de la demanda per un edifici nou', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'han pogut crear les dispersions', 201: NewBuldingDemandDispersionsSerializer})
    def create(self, request, pk=None):
        d = NewBuldingDemandDispersions(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'], dispersion = request.data['value'])
        if d.DoesNotExist:
            return Response('No s\'han pogut crear les dispersions', 404)
        else:
            serializer = NewBuldingDemandDispersionsSerializer(d)
            return Response(serializer.data, 201)


    #Obtener valores de la dispersion introduciendo el valor de la zona climatica
    @swagger_auto_schema(
        operation_description='Actualitza els valors de la dispersio', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar la dispersio', 200: NewBuldingDemandDispersionsSerializer})
    def update(self, request, pk=None):
        d = NewBuldingDemandDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.dispersion = request.data['value']
            d.save()
            serializer = NewBuldingDemandDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar la dispersio', 404)


    #Actualizar valores de la dispersion
    @swagger_auto_schema(
        operation_description='Obté el valor de la dispersio', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
        ],
        responses= {404: 'No s\'ha trobat cap dispersio', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        d = NewBuldingDemandDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('dispersion')
        if d.exists:
            serializer = NewBuldingDemandDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha trobat cap dispersio', 204)


class NewBuildingEnergyAndEmissionsDispersionsSet(ViewSet):
    parser_classes = [JSONParser]

     #Introducir valores de la dispersion
    @swagger_auto_schema(
        operation_description='Crea una dispersio per l\'energia i demanda d\'un edifici nou', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut crear la dispersio', 201: NewBuldingEnergyAndEmissionsDispersionsSerializer})
    def create(self, request, pk=None):
        d = NewBuldingEnergyAndEmissionsDispersions(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'], dispersion = request.data['value'])
        if d.DoesNotExist:
            return Response('No s\'ha pogut crear la dispersio', 404)
        else:
            serializer = NewBuldingEnergyAndEmissionsDispersionsSerializer(d)
            return Response(serializer.data, 201)


    #Obtener valores de la dispersion introduciendo el valor de la zona climatica
    @swagger_auto_schema(
        operation_description='Actualitza els valor d\'una dispersio per un edifici nou', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar la dispersio', 200: NewBuldingEnergyAndEmissionsDispersionsSerializer})
    def update(self, request, pk=None):
        d = NewBuldingEnergyAndEmissionsDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.dispersion = request.data['value']
            d.save()
            serializer = NewBuldingEnergyAndEmissionsDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar la dispersio', 404)


    #Actualizar valores de la dispersion
    @swagger_auto_schema(
        operation_description='Obtñ el valor de la dispersio', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
        ],
        responses= {204: 'No s\'ha trobat cap dispersio', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        d = NewBuldingEnergyAndEmissionsDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('dispersion')
        if d.exists:
            serializer = NewBuldingEnergyAndEmissionsDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha trobat cap dispersio', 204)


class ExistingBuildingDemandDispersionsSet (ViewSet):
    parser_classes = [JSONParser]

         #Introducir valores de la dispersion
    @swagger_auto_schema(
        operation_description='Crea una dispersio de la demanda per un edifici existent', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut crear la dispersio', 201: ExistingBuldingDemandDispersionsSerializer})
    def create(self, request, pk=None):
        d = ExistingBuldingDemandDispersions(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'], dispersion = request.data['value'])
        if d.DoesNotExist:
            return Response('No s\'ha pogut crear la dispersio', 404)
        else:
            serializer = ExistingBuldingDemandDispersionsSerializer(d)
            return Response(serializer.data, 201)


    #Obtener valores de la dispersion introduciendo el valor de la zona climatica
    @swagger_auto_schema(
        operation_description='Actualitza el valor de la dispersio de la demanda per un edifici existent', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar la dispersio', 200: ExistingBuldingDemandDispersionsSerializer})
    def update(self, request, classificarion: string = None):
        d = ExistingBuldingDemandDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.dispersion = request.data['value']
            d.save()
            serializer = ExistingBuldingDemandDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar la dispersio', 404)

    #Actualizar valores de la dispersion
    @swagger_auto_schema(
        operation_description='Obté el valor de la dispersio de la demanda per un edifici existent', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
        ],
        responses= {204: 'No s\'ha trobat cap dispersio', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        d = ExistingBuldingDemandDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('dispersion')
        if d.exists:
            serializer = ExistingBuldingDemandDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha trobat cap dispersio', 204)

class ExistingBuildingEnergyAndEmissionsDispersionsSet(ViewSet):
    parser_classes = [JSONParser]

     #Introducir valores de la dispersion
    @swagger_auto_schema(
        operation_description='Crea la dispersio del consum i les emissions per un edifici existent', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut crear la demanda', 201: ExistingBuldingEnergyAndEmissionsDispersionsSerializer})
    def create(self, request, pk=None):
        d = ExistingBuldingEnergyAndEmissionsDispersions(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'], dispersion = request.data['value'])
        if d.DoesNotExist:
            return Response('No s\'ha pogut crear la demanda', 404)
        else:
            serializer = ExistingBuldingEnergyAndEmissionsDispersionsSerializer(d)
            return Response(serializer.data, 201)


    #Obtener valores de la dispersion introduciendo el valor de la zona climatica
    @swagger_auto_schema(
        operation_description='Actualitza el valor de la dispersio per un edifici existent', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus d\'edifici, el codi de la zona climatica i el valor de la dispersio',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el tipus d\'edifici',
                                    example= 'true'),
                'climatic_zone': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la zona climàtica',
                                    example= 'A3'),
                'value': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona la zona climàtica',
                                    example= '1.4'),
            },
            required=["type", "climatic_zone", "value"],
        ),
        responses= {404: 'No s\'ha pogut actualitzar el valor de la dispersio', 200: ExistingBuldingEnergyAndEmissionsDispersionsSerializer})
    def update(self, request, pk=None):
        d = ExistingBuldingEnergyAndEmissionsDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone'])
        if d.exists:
            d.dispersion = request.data['value']
            d.save()
            serializer = ExistingBuldingEnergyAndEmissionsDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut actualitzar el valor de la dispersio', 404)


    #Actualizar valores de la dispersion
    @swagger_auto_schema(
        operation_description='Obté el valor de la dispersió per un edifici existent', 
        manual_parameters=[
            openapi.Parameter(
                'type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el tipus d\'edifici',
            ),
            openapi.Parameter(
                'climatic_zone',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la zona climatica de la zona de l\'edifici',
            ),
        ],
        responses= {204: 'No s\'ha pogut obtenir el valor de la dispersio', 200: openapi.Schema(type = openapi.TYPE_NUMBER, format = openapi.FORMAT_FLOAT), 402: "Already liked!"})
    def retrieve(self, request, pk=None):
        d = ExistingBuldingEnergyAndEmissionsDispersions.objects.filter(building_type=request.data['type'], climatic_zone = request.data['climatic_zone']).values('dispersion')
        if d.exists:
            serializer = ExistingBuldingEnergyAndEmissionsDispersionsSerializer(d)
            return Response(serializer.data, 200)
        else:
            return Response('No s\'ha pogut obtenir el valor de la dispersio', 204)

class UserView(ViewSet):

    @swagger_auto_schema(
        operation_description='Crea un usuari', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el nom d\'usuari, la contrasenya i el email de l\'usuari',
            properties= {
                'username': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                    description='Proporciona el nom d\'usuari',
                                    example= 'username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la contrasenya',
                                    example= 'a37dfv7f'),
                'email': openapi.Schema(type=openapi.TYPE_NUMBER,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona l\'email',
                                    example= 'exemple@gmail.com'),
            },
            required=["username", "password", "email"],
        ),
        responses= { 404: 'No s\'ha pogut crear l\'usuari', 200: UserSerializer})
    def create(self, request, pk=None):
        u = User(username=request.data['username'], password=request.data['password'], email=request.data['email'])
        if u.DoesNotExist:
            return Response ('No s\'ha pogut crear l\'usuari', 404)
        else:
            serializer = UserSerializer(u)
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Actualitza la informació d\'un usuari', 
        manual_parameters=[
            openapi.Parameter(
                'email',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona l\'email',
            ),
            openapi.Parameter(
                'password',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la contrasenya',
            ),
        ],
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def update(self, request):
        u = User.objects.filter(email = request.data['email'])
        u.password = request.data['password']
        u.save()
        serializer = UserSerializer(u)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Actualitza la informació d\'un usuari', 
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: FileSerializer})
    def retrieve(self, request, pk = None):
        u = User.objects.filter(pk = pk)
        serializer = FileSerializer(u)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Actualitza la informació d\'un usuari', 
        manual_parameters=[
            openapi.Parameter(
                'username',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona l\'usuari a esborrar',
            ),
        ],
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def delete(self, request):
        u = User.objects.filter(username = request.data['username'])
        result = u.delete()
        return Response(result)

class FileView(ViewSet):

    @swagger_auto_schema(
        operation_description='Crea un fitxer', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el nom del fitxer, la seva descripcio i l\'usuari al que pertany',
            properties= {
                'name': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona el nom',
                                    example= 'username'),
                'description': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la descripcio',
                                    example= 'descripcio d\'exemple'),
                'username': openapi.Schema(type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el nom d\'usuari',
                                    example= 'exemple'),
            },
            required=["name", "description", "username"],
        ),
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def create(self, request, pk=None):
        u = File(name=request.data['name'], description=request.data['description'], username=request.data['username'])
        serializer = FileSerializer(u)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Actualitza la informació d\'un usuari', 
        manual_parameters=[
            openapi.Parameter(
                'name',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona el nom',
            ),
            openapi.Parameter(
                'descripcio',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona la descripcio',
            ),
        ],
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def update(self, request):
        u = File.objects.filter(name = request.data['name'], descripcio = request.data['descripcio'])
        u.password = request.data['password']
        u.save()
        serializer = FileSerializer(u)
        return Response(serializer.data)

    @swagger_auto_schema(
            operation_description='Obte els calculs d\'un fitxer', 
            manual_parameters=[
                openapi.Parameter(
                    'file',
                    in_=openapi.IN_PATH,
                    type=openapi.TYPE_STRING,
                    required=True,
                    description='Proporciona l\'email',
                ),
            ],
            responses= {401: 'You provided no api key', 404: 'contribution not found', 200: CalculSerializer})
    def retrieve(self, request, pk = None):
        c = File.objects.filter(pk=pk)
        serializer = UserSerializer(c)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Esborra un fitxer', 
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def delete(self, request, pk=None):
        u = File.objects.filter(pk = pk)
        result = u.delete()
        return Response(result)


class CalculSet(ViewSet):

    @swagger_auto_schema(
        operation_description='Crea un calcul', 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='Proporciona el tipus, data, valor, calificacio, consum i fitxer del calcul',
            properties= {
                'type': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona el tipus',
                                    example= 'username'),
                'date': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la data',
                                    example= '21/02/2022'),
                'value': openapi.Schema(type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor del calcul',
                                    example= 1.5),
                'calification': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona la calificacio del calcul',
                                    example= 'A'),
                'consumption': openapi.Schema(type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_FLOAT,
                                    description='Proporciona el valor del consum',
                                    example= 1.5),
                'file': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='Proporciona el id del fitxer',
                                    example= '3g4v456gv'),          
            },
            required=["type", "date", "value","calification","consumption","file"],
        ),
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def create(self, request, pk=None):
        c = Calcul(type=request.data['type'], date=request.data['date'], value=request.data['value'],calification=request.data['calification'], consumption=request.data['consumption'], file=request.data['file'])
        serializer = CalculSerializer(c)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Actualitza la informació d\'un usuari', 
        manual_parameters=[
            openapi.Parameter(
                'email',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona l\'email',
            ),
        ],
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def retrieve(self, request):
        c = Calcul.objects.filter(file=request.data['file'])
        serializer = UserSerializer(c)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Esborra un fitxer', 
        manual_parameters=[
            openapi.Parameter(
                'id',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Proporciona l\'usuari a esborrar',
            ),
        ],
        responses= {401: 'You provided no api key', 404: 'contribution not found', 200: 'Dispersions d\'energia i dimensions creades correctament'})
    def delete(self, request):
        c = Calcul.objects.filter(name = request.data['id'])
        result = c.delete()
        return Response(result)
