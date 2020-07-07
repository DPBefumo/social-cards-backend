from django.shortcuts import render
from users.models import User
from .models import Card
from .serializers import UserSerializer, CardSerializer
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import filters
from rest_framework import viewsets, permissions, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class =[permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile_page(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_follows(self, request):
        follows = request.user.followed_user.filter()
        serializer = UserSerializer(follows, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_followers(self, request):
        followers = request.user.followers.filter()
        serializer = UserSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_cards(self, request):
        cards = request.user.cards.all()
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def follower_cards(self, request):
        cards = request.user.followers.all()
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

class FollowedView(views.APIView):
    permission_class =[permissions.IsAuthenticated]

    def post(self, request, format=None):
        name_of_user = request.data['user']
        user_to_follow = User.objects.get(username=name_of_user)
        current_user = request.user
        current_user.followed_user.add(user_to_follow)
        return Response({"followed_user_count": current_user.followed_user.count()})