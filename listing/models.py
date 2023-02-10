import uuid
from django.utils import timezone
from django.db import models
from accounts.models import User


PROPERTY_TYPE_CHOICES = (
    ("residential property", "Residential Property"),
    ("Commercial property", "Commercial Property"),
    ("Industrial property", "Industrial Property"),
    ("agricultural property", "Agricultural Property"),
    ("recreational property", "Recreational Property"),
    ("special-use property", "Special-use Property"),
    ("land", "Land")
)


class Property(models.Model):


    class Status(models.TextChoices):
        RENTED = 'rented', 'Rented',
        SOLD = 'sold', 'Sold',
        AVAILABLE = 'available', 'Available'


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="properties")
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    beds = models.PositiveIntegerField()
    baths = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image_urls = models.TextField(blank=True)
    posted = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.AVAILABLE)


    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties" 

        ordering = ['-posted']
        indexes = [
            models.Index(fields=['-posted'])
        ]

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"
