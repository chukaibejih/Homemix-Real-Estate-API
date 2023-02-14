from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
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

    """
    ConfirmEmailView

    This view is used to confirm the email of a user. It is a subclass of APIView and handles the GET request 
    to confirm the email. The user's information is retrieved using the get_user_model() function and the 
    serialization is done using the ConfirmEmailSerializer class. The view has no permission classes.

    The view decodes the uidb64 and token passed in the request and retrieves the user information. 
    If the user is found and the token is valid, the user's is_active and is_verified flags are set to 
    True and the user information is saved. The view returns a success message on success. 
    In case of an error, an error message is returned with a status code of 400.
    """


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
        return Response({"error": "Email confirmation failed"}, status=400)




class ChangePasswordView(generics.CreateAPIView):

    """
    ChangePasswordView is a subclass of generics.CreateAPIView and is used for changing the password of a user.
    It takes in the data for the old password and the new password, and validates the old password entered.
    If the old password entered is incorrect, it returns an error message with a status code of 400.
    If the old password is correct, it sets the new password and saves the changes to the user object.
    It returns a success message with a status code of 200 upon successful password change.
    """

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

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     user = request.user
    #     Token.objects.get_or_create(user=user)
    #     return response


# class CustomTokenDestroyView(GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         """Invalidate the user's current token."""
#         user = request.user
#         try:
#             token = user.token
#         except Token.DoesNotExist:
#             return Response ({"message": "User has no token"}, status=status.HTTP_400_BAD_REQUEST)
#         token.delete()
#         return Response ({"message": "Logged out successfully"}, status=status.HTTP_200_OK)




class UserViewSet(viewsets.ModelViewSet):

    """
    UserViewSet is a ModelViewSet for handling User operations. It uses the UserSerializer for serializing and 
    deserializing user data.

    The default queryset for this viewset is all the users in the system. However, the viewset has been 
    customized to restrict the queryset based on the requesting user's privilege level. If the user is a 
    staff or a superuser, all users are returned. Otherwise, only active users are returned.

    Additionally, the viewset implements custom serializer and permission classes based on the requested 
    action. If the action is 'create', the RegisterSerializer will be used. If the action is 'destroy', 
    the user must be both authenticated and an admin user.

    Overall, the UserViewSet provides a convenient way to manage users while enforcing privilege and 
    security restrictions.
    """

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
