"""Homemix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view as swagger_get_schema_view 
from drf_yasg import openapi

schema_view = swagger_get_schema_view(
   openapi.Info(
        title="Homemix Real Estate API",
        default_version='1.0',
        description='''Welcome to Homemix, a powerful and flexible Real Estate API that enables users to buy and sell properties with ease. Homemix is a RESTful API that provides endpoints for CRUD operations on real estate listings, making it simple for users to create, read, update, and delete listings.

Homemix offers a comprehensive solution for buying and selling properties, with advanced search and filtering capabilities, secure authentication, and support for multiple media types. With detailed information on property type, address, price, size, number of bedrooms and bathrooms, description, photos, availability, and contact information, Homemix makes it easy for potential buyers to search for properties that meet their specific needs and requirements.

In addition to these features, Homemix now also includes a referral system, providing a unique way for users to invite others to the platform and receive rewards or incentives. Homemix is built with Django Rest Framework (DRF), a powerful and flexible framework for building APIs in Django. This makes it easy to extend and customize the API to meet specific needs, and provides comprehensive documentation and examples to get you started quickly.

With Homemix, you can register as either a buyer or seller, and access secure authentication and authorization through the use of token-based authentication. This ensures that only authorized users have access to sensitive information and the ability to manipulate data.

Homemix is the ideal solution for anyone looking to buy or sell properties with ease, offering a user-friendly interface and advanced features to make the process as smooth and efficient as possible. This documentation will provide a technical overview of the platform, including the technologies used to gather and display pricing data, and how to interact with the API to perform CRUD operations on real estate listings.''',
        contact=openapi.Contact(name="Chukwuka Ibejih", email="chukaibejih@gmail.com"),
        license=openapi.License(name="MIT license"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('listings/', include('listing.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
