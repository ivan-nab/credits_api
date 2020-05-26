from rest_framework import routers
from partners_api.views import CreditOfferViewSet, ClientCreditFormViewSet, CreditRequestViewSet

router = routers.DefaultRouter()
router.register('offers', CreditOfferViewSet)
router.register('requests', CreditRequestViewSet, basename='out_credit_requests')
router.register('creditforms', ClientCreditFormViewSet, basename='creditforms')

urlpatterns = router.urls
