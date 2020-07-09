from users.models import User
from .models import Card
from rest_framework import serializers

#Create serializers here
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'password',
            'first_name',
            'last_name',
            'bio',
            'followed_users',
            'cards',
            'is_staff',
        ]

class CardSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    
    class Meta:
        model = Card
        fields = [
            'url',
            'id',
            'author',
            'message',
            'color',
            'border',
            'font',
        ]