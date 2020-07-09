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
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This ViewSet displays the users of the application.  The main view is of all users of 
    the app.  Using the @action decorator, url paths have been added to be able to display 
    the logged in user's profile page, who the user follows, and who follows the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =[permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'patch'])
    def profile_page(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_follows(self, request):
        follows = request.user.followed_users.filter()
        serializer = UserSerializer(follows, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def friends(self, request):
        followers = request.user.followers.filter()
        serializer = UserSerializer(followers, many=True, context={'request': request})
        return Response(serializer.data)


class CardViewSet(viewsets.ModelViewSet):
    """
    This ViewSet displays the cards that have been added to the page. The main view 
    is of the cards for the logged in user. Using the @action decorator, url paths have 
    been created to have a view for displaying all of the cards on the app and the 
    cards of users that the logged in user follows.
    """
    serializer_class = CardSerializer
    permission_classes =[permissions.IsAuthenticated]

    def get_queryset(self):
        cards = self.request.user.cards.all()
        return cards

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def all_cards(self, request):
        cards = Card.objects.all()
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def follower_cards(self, request):
        cards = request.user.followed_users.all()
        page = self.paginate_queryset(cards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data)


class FollowedListView(views.APIView):
    """
    This view is to display who the logged in user follows.
    """
    permission_classes =[permissions.IsAuthenticated]

    def get(self, request, format=None):
        followers = [user.username for user in request.user.followed_users.all()]
        return Response(followers)

    def post(self, request, format=None):
        name_of_user = request.data['user']
        user_to_follow = User.objects.get(username=name_of_user)
        current_user = request.user
        current_user.followed_users.add(user_to_follow)
        return Response({"followed_user_count": current_user.followed_users.count()})


class FollowedDetailView(views.APIView):
    """
    This view is to allow the logged in user to unfollow another user.  
    """
    permission_classes =[permissions.IsAuthenticated]

    def get(self, request, name_of_user, format=None):
        follower_to_view = User.objects.get(username=name_of_user)
        serializer = UserSerializer(follower_to_view, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, name_of_user, format=None):
        user_to_unfollow = User.objects.get(username=name_of_user)
        current_user = request.user
        current_user.followed_users.remove(user_to_unfollow)
        return Response(request.data)


