import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from accounts.manager import UserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

ROLE_CHOICES = (
    ("buyer", "Buyer"),
    ("seller", "Seller")
)



class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    premium = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Buyer")
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return self.email


# class Token(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     refresh_token = models.TextField()

#     def save(self, *args, **kwargs):
#         self.refresh_token = str(RefreshToken.for_user(self.user))
#         super().save(*args, **kwargs)

