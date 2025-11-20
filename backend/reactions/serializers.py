from rest_framework import serializers
from .models import UserReaction

class UserReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReaction
        fields = ['id', 'reaction_type']