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
            'is_staff',
        ]

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = [
            'inner_message',
            'outer_message',
            'color',
            'border',
            'font',
        ]