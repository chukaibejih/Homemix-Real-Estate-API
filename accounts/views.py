from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.response import Response
from accounts.serializers import (
    RegisterSerializer,
    TokenObtainPairSerializer,
    UserSerializer,
    )
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Use the TokenObtainPairSerializer to generate the access and refresh tokens
        token_serializer = TokenObtainPairSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data

        return Response({
            "user": serializer.data,
            "tokens": tokens
        })        