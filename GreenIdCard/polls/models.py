from django.db import models

# Create your models here.

class ClassificationResidentialBuilding(models.Model):
    calification = models.CharField(max_length=4, primary_key = True)
    min_C1 = models.FloatField(null=False)
    max_C1 = models.FloatField(null=False)
    min_C2 = models.FloatField(null=True)
    max_C2 = models.FloatField(null=True)

class ClassificationNotResidentialBuilding(models.Model):
    calification = models.CharField(max_length=4, primary_key = True)
    min_C = models.FloatField(null=False)
    max_C = models.FloatField(null=False)

class NewBuildingDemand(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    heating_mean = models.FloatField()
    refrigeration = models.FloatField()

    class Meta:
        unique_together = [["building_type", "climatic_zone"]]

class NewBuildingEnergyConsume(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    heating_mean = models.FloatField()
    refrigeration = models.FloatField()
    ACS = models.FloatField()

    class Meta:
        unique_together = [["building_type", "climatic_zone"]]

class NewBuildingEmissions(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    heating_mean = models.FloatField()
    refrigeration = models.FloatField()
    ACS = models.FloatField()

    class Meta:
        unique_together = [["building_type", "climatic_zone"]]

class ExistingBuildingDemand(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    heating_mean = models.FloatField()
    refrigeration = models.FloatField()

    class Meta:
        unique_together = [["building_type", "climatic_zone"]]

class ExistingBuildingEnergyConsume(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    heating_mean = models.FloatField()
    refrigeration = models.FloatField()
    ACS = models.FloatField()

    class Meta:
        unique_together = [["building_type", "climatic_zone"]]

class ExistingBuildingEmissions(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    heating_mean = models.FloatField()
    refrigeration = models.FloatField()
    ACS = models.FloatField()

    class Meta:
        unique_together = [["building_type", "climatic_zone"]]

class NewBuldingDemandDispersions(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    dispersion = models.FloatField(null=True)

    unique_together = [["building_type", "climatic_zone"]]

class NewBuldingEnergyAndEmissionsDispersions(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    dispersion = models.FloatField(null=True)

    unique_together = [["building_type", "climatic_zone"]]

class ExistingBuldingDemandDispersions(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    dispersion = models.FloatField(null=True)

    unique_together = [["building_type", "climatic_zone"]]

class ExistingBuldingEnergyAndEmissionsDispersions(models.Model):
    building_type = models.BooleanField()
    climatic_zone = models.CharField(max_length=4)
    dispersion = models.FloatField(null=True)

    unique_together = [["building_type", "climatic_zone"]]

class User(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class File(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Calcul(models.Model):
    type = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    value = models.FloatField()
    calification = models.CharField(max_length=100)
    consumption = models.FloatField()
    file = models.ForeignKey(File, on_delete=models.CASCADE)
