from django.urls import path, include
from rest_framework.routers import SimpleRouter
from accounts.views import UserViewSet, CustomTokenObtainPairViewSet, ConfirmEmailView, RetriveReferralView
from rest_framework_simplejwt.views import TokenRefreshView

router = SimpleRouter()
register = UserViewSet.as_view({"post":"create"})

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm-email/<uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('login/', CustomTokenObtainPairViewSet.as_view(), name='token-obtain-pair'),
    path('referral/<str:referral_id>/', RetriveReferralView.as_view(), name='retrieve_referral'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path("reset-password/", include("django_rest_passwordreset.urls", namespace="password_reset")),
]


router.register('users', UserViewSet, basename='users')

urlpatterns += router.urls