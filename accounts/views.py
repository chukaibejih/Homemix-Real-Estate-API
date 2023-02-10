from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode

from accounts.serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    ConfirmEmailSerializer,
    )


User = get_user_model()


class ConfirmEmailView(APIView):
    queryset = get_user_model().objects.all()
    serializer_class = ConfirmEmailSerializer
    permission_classes = []

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Email confirmation failed"}, status=400)




class ChangePasswordView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_password = request.data.get("old_password")
        if not request.user.check_password(old_password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)



class CustomTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(is_active=True)

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        if self.action == "destroy":
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return super().get_permissions()


# class RegisterView(generics.GenericAPIView):

#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         # Use the TokenObtainPairSerializer to generate the access and refresh tokens
#         token_serializer = TokenObtainPairSerializer(data=request.data)
#         token_serializer.is_valid(raise_exception=True)
#         tokens = token_serializer.validated_data

#         return Response({
#             "user": serializer.data,
#             "tokens": tokens
#         })        


# class RegisterView(generics.GenericAPIView):
#     pass