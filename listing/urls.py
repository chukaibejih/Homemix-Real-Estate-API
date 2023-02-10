from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import PropertyViewSet

router = SimpleRouter()
router.register('properties', PropertyViewSet, basename='properties')

urlpatterns = [

]

urlpatterns += router.urls
