from django.urls import path
from rest_framework.routers import SimpleRouter
from accounts.views import UserViewSet, RegisterView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns += router.urls