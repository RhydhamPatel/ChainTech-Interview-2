from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response({"error": "Only the organizer can update this event."}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response({"error": "Only the organizer can delete this event."}, status=403)
        return super().destroy(request, *args, **kwargs)

class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        user = request.user
        status = request.data.get('status')
        rsvp = RSVP.objects.create(event=event, user=user, status=status)
        return Response({'message': 'RSVP created successfully'})

    def update(self, request, event_id, user_id):
        rsvp = get_object_or_404(RSVP, event_id=event_id, user_id=user_id)
        rsvp.status = request.data.get('status')
        rsvp.save()
        return Response({'message': 'RSVP updated successfully'})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        review = Review.objects.create(
            event=event, 
            user=request.user, 
            rating=request.data.get('rating'), 
            comment=request.data.get('comment')
        )
        return Response({'message': 'Review added successfully'})

    def list(self, request, event_id):
        reviews = Review.objects.filter(event_id=event_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)