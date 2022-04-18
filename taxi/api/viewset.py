from rest_framework.permissions import AllowAny

from taxi.api.serializer import UserSerializer, FaqSerializer
from taxi.models import CustomUser, Faq
from rest_framework import viewsets, mixins


class UserViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class FaqViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
