import uuid
from shortuuid.django_fields import ShortUUIDField 
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from accounts.manager import UserManager
from .utils import get_referral_code

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
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_referral_code()
            print(self.referral_code)
        super().save(*args, **kwargs)


class Referral(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred = models.ForeignKey(User, on_delete=models.CASCADE)
    date_referred = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.referrer} referred {self.referred}"

