from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'rsvp', RSVPViewSet, basename='rsvp')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]