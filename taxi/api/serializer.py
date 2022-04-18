from rest_framework import serializers

from taxi.models import CustomUser, Faq, FaqCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'avatar']


class CustomUserMessageSerializer(
    serializers.ModelSerializer):  # chatda ikki user yozishganda kim tomonidan yozishayotganini korsatish uchun
    class Meta:  # ahuning uchun id va username qaytarilyapti
        model = CustomUser
        fields = ["id", "username"]


class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    faqCategory = serializers.SerializerMethodField()

    class Meta:
        model = Faq
        fields = '__all__'

    def get_faqCategory(self, obj):
        return FaqCategorySerializer(obj.faqCategory, many=False, context={"request": self.context["request"]}).data
