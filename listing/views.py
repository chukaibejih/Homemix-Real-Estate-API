from rest_framework import viewsets, pagination, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle 
from .models import Property
from .serializers import PropertySerializer
from common.permissions import IsSellerOReadOnly


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "limit"  # items per page


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated, IsSellerOReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['address', 'city', 'state', 'zip_code', 'property_type']
    pagination_class = CustomPageNumberPagination
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PropertySerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        print(serializer.errors)
        return super().perform_create(serializer)