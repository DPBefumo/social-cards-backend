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
            # 'image',
            'username',
            'password',
            'bio',
            'followed_user',
            'is_staff',
        ]

class CardSerializer(serializers.HyperlinkedModelSerializer):
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