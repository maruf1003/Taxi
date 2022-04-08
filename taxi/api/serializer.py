from rest_framework import serializers

from taxi.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserMessageSerializer(serializers.ModelSerializer):   # chatda ikki user yozishganda kim tomonidan yozishayotganini korsatish uchun
    class Meta:                                                    # ahuning uchun id va username qaytarilyapti
        model = CustomUser
        fields = ["id", "username"]

