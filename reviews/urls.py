from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

#namespace: reviews
app_name = 'reviews'

# Create a router and register our viewset with it
router = DefaultRouter()
router.register(r'', ReviewViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]