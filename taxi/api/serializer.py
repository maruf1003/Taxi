from rest_framework import serializers

from taxi.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]
#
# class UserCustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = "__all__"

#
# class User_driverSerializer(serializers.ModelSerializer):  # zakazdan song xaydovchining massiv dagi dannylarini koradi
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'fullname', 'avatar', ]
#
# # class User_passengerSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = CustomUser
# #         fields = ['username', 'fullname', 'avatar', ]
