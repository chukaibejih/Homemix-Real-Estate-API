from rest_framework import viewsets, pagination, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Property
from .serializers import PropertySerializer


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "limit"  # items per page


class PropertyViewSet(viewsets.ViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['address', 'city', 'state', 'zip_code', 'property_type']
    pagination_class = CustomPageNumberPagination
