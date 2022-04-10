from django.contrib import admin
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

router.register(r'residentialBuildingClassification', views.ResidentialBuildingClassificationSet, 'residentialBuildingClassification')
router.register(r'nonResidentialBuildingClassification', views.NonResidentialBuildingSet, 'nonResidentialBuildingClassification')
router.register(r'newBuildingDemand', views.NewBuildingDemandSet, 'newBuildingDemand')
router.register(r'newBuildingEnergyConsumption', views.NewBuildingEnergyConsumptionSet, 'newBuildingEnergyConsumption')
router.register(r'newBuildingEmissions', views.NewBuildingEmissionsSet, 'newBuildingEmissions')
router.register(r'existingBuildingDemand', views.ExistingBuildingDemandSet, 'existingBuildingDemand')
router.register(r'existingBuildingEnergyConsumption', views.ExistingBuildingEnergyConsumptionSet, 'existingBuildingEnergyConsumption')
router.register(r'existingBuildingEmissions', views.ExistingBuildingEmissionsSet, 'existingBuildingEmissions')
router.register(r'newBuildingDemandDispersions', views.NewBuildingDemandDispersionsSet, 'newBuildingDemandDispersions')
router.register(r'newBuildingEnergyAndEmissionsDispersions', views.NewBuildingEnergyAndEmissionsDispersionsSet, 'newBuildingEnergyAndEmissionsDispersions')
router.register(r'existingBuildingDemandDispersions', views.ExistingBuildingDemandDispersionsSet, 'existingBuildingDemandDispersions')
router.register(r'exisitingBuildingEnergyAndEmissionsDispersions', views.ExistingBuildingEnergyAndEmissionsDispersionsSet, 'existingBuildingEnergyAndEmissionsDispersions')


urlpatterns = router.urls