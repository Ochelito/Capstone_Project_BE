"""
URL configuration for upshere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),
   
    #JWT endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   # Include the API URLs for each app
    path('api/bookings/', include(('bookings.urls', 'bookings'), namespace='bookings')),  # Assuming you have a bookings app for booking management
    path('api/lessons/', include(('lessons.urls', 'lessons'), namespace='lessons')),  # Assuming you have a lessons app for lesson management
    path('api/reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),  # Assuming you have a reviews app for review management
    path('api/skills/', include(('skills.urls', 'skills'), namespace='skills')),  # Assuming you have a skills app for skill management
    path('api/users/', include(('users.urls', 'users'), namespace='users')),  # Assuming you have a users app for user management
]
