from django.urls import path
from rest_framework import routers
from .views import PurchaseViewSet, BillViewSet

router = routers.DefaultRouter()
router.register('purchases', PurchaseViewSet , basename='purchases')

urlpatterns = [
                  path('token/', BillViewSet.as_view({'post': 'post', 'get': 'get'}))
              ] + router.urls
