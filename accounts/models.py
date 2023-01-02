import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from accounts.manager import UserManager

# Create your models here.

ROLE_CHOICES = (
    ("buyer", "Buyer"),
    ("seller", "Seller")
)

PROPERTY_TYPE_CHOICES = (
    ("residential property", "Residential Property"),
    ("Commercial property", "Commercial Property"),
    ("Industrial property", "Industrial Property"),
    ("agricultural property", "Agricultural Property"),
    ("recreational property", "Recreational Property"),
    ("special-use property", "Special-use Property"),
    ("land", "Land")
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
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def __str__(self) -> str:
        return self.email


# class Property(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     zip_code = models.CharField(max_length=20)
#     property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     beds = models.PositiveIntegerField()
#     baths = models.DecimalField(max_digits=10, decimal_places=1)
#     description = models.TextField(blank=True)
#     image_urls = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.address}, {self.city}, {self.state}"


