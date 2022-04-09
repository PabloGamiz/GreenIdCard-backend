from rest_framework import serializers
from .models import (ClassificationResidentialBuilding, ClassificationNotResidentialBuilding, NewBuildingDemand, NewBuildingEnergyConsume, NewBuildingEmissions, ExistingBuildingDemand, ExistingBuildingEnergyConsume, ExistingBuildingEmissions, NewBuldingDemandDispersions, NewBuldingEnergyAndEmissionsDispersions, ExistingBuldingDemandDispersions, ExistingBuldingEnergyAndEmissionsDispersions, User, File, Calcul)
from rest_framework.serializers import ModelSerializer

class ClassificationResidentialBuildingSerializer(ModelSerializer):
    
    class Meta:
        model = ClassificationResidentialBuilding
        fields = ('calification','min_C1','max_C1','min_C2','max_C2')


class ClassificationNotResidentialBuildingSerializer(ModelSerializer):
    class Meta:
        model = ClassificationNotResidentialBuilding
        fields = ('calification','min_C','max_C')

class NewBuildingDemandSerializer(ModelSerializer):
    class Meta:
        model = NewBuildingDemand
        fields = ('building_type','climatic_zone','heating_mean','refrigeration')

class NewBuildingEnergyConsumeSerializer(ModelSerializer):
    class Meta:
        model = NewBuildingEnergyConsume
        fields = ('building_type','climatic_zone','heating_mean','refrigeration','ACS')

class NewBuildingEmissionsSerializer(ModelSerializer):
    class Meta:
        model = NewBuildingEmissions
        fields = ('building_type','climatic_zone','heating_mean','refrigeration','ACS')

class ExistingBuildingDemandSerializer(ModelSerializer):
    class Meta:
        model = ExistingBuildingDemand
        fields = ('building_type','climatic_zone','heating_mean','refrigeration')

class ExistingBuildingEnergyConsumeSerializer(ModelSerializer):
    class Meta:
        model = ExistingBuildingEnergyConsume
        fields = ('building_type','climatic_zone','heating_mean','refrigeration','ACS')

class ExistingBuildingEmissionsSerializer(ModelSerializer):
    class Meta:
        model = ExistingBuildingEmissions
        fields = ('building_type','climatic_zone','heating_mean','refrigeration','ACS')

class NewBuldingDemandDispersionsSerializer(ModelSerializer):
    class Meta:
        model = NewBuldingDemandDispersions
        fields = ('building_type','climatic_zone','dispersion')

class NewBuldingEnergyAndEmissionsDispersionsSerializer(ModelSerializer):
    class Meta:
        model = NewBuldingEnergyAndEmissionsDispersions
        fields = ('building_type','climatic_zone','dispersion')

class ExistingBuldingDemandDispersionsSerializer(ModelSerializer):
    class Meta:
        model = ExistingBuldingDemandDispersions
        fields = ('building_type','climatic_zone','dispersion')

class ExistingBuldingEnergyAndEmissionsDispersionsSerializer(ModelSerializer):
    class Meta:
        model = ExistingBuldingEnergyAndEmissionsDispersions
        fields = ('building_type','climatic_zone','dispersion')

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'password', 'email')

class FileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = File
        fields = ('id','name', 'description', 'user')

class CalculSerializer(ModelSerializer):
    file = FileSerializer(read_only=True)
    class Meta:
        model = Calcul
        fields = ('id','type', 'date', 'value', 'calification', 'consumption', 'file')