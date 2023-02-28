from rest_framework import serializers
from . models import Property

class PropertySerializer(serializers.ModelSerializer):
     class Meta:
            model = Property
            fields = (
               'id',
               'seller',
               'address',
               'city',
               'state',
               'zip_code',
               'property_type',
               'price',
               'beds',
               'baths',
               'description',
               'image_urls',
               'posted',
               'created_at',
               'updated_at',
               'status',
            )
            extra_kwargs = {
         "seller": {"read_only": True},
      }
         