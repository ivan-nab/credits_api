from rest_framework import routers
from banks_api.views import CreditRequestViewSet

router = routers.DefaultRouter()
router.register('requests', CreditRequestViewSet, basename='requests')

urlpatterns = router.urls
