from django.shortcuts import render
from users.models import User
from .models import Card
from .serializers import UserSerializer, CardSerializer
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import filters
from rest_framework import viewsets, permissions

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class =[permissions.IsAuthenticated]

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer