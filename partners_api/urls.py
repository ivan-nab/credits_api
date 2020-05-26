from rest_framework import routers
from partners_api.views import CreditOfferViewSet, ClientCreditFormViewSet, CreditRequestViewSet
from partners_api.permissions import SwaggerAccessPolicy
from django.urls import path, re_path



router = routers.DefaultRouter()
router.register('offers', CreditOfferViewSet)
router.register('requests', CreditRequestViewSet, basename='out_credit_requests')
router.register('creditforms', ClientCreditFormViewSet, basename='creditforms')

urlpatterns = router.urls
