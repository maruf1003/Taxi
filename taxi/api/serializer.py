from rest_framework import serializers

from taxi.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

