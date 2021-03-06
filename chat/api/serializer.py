from rest_framework import serializers
from chat.models import Thread, Message, Particpaint
from taxi.api.serializer import CustomUserMessageSerializer


class ThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = "__all__"

    def get_last_message(self, obj):
        message = Message.objects.filter(thread=obj).order_by("-created_at").first()
        if message:
            return {
                "message": message.text,
                "created_at": message.created_at
            }
        else:
            "not message"

    def get_unread_count(self, obj):
        particpaint = Particpaint.objects.filter(thread=obj, user=self.context["request"].user).first()
        if particpaint:
            return Message.objects.filter(created_at__gt=particpaint.last_read).count()
        else:
            return 0


class MessageSerializer(serializers.ModelSerializer):
    user_message = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d/%b/%Y")
    updated_at = serializers.DateTimeField(format="%d/%b/%Y")

    class Meta:
        model = Message
        fields = ['id', 'user_message', 'created_at', 'updated_at', 'text', 'thread', ]

    def get_user_message(self, obj):
        return CustomUserMessageSerializer(obj.user, many=False, context={"request": self.context[
            'request']}).data  # chatda ikki user yozishganda kim tomonidan yozishayotganini korsatish uchun
