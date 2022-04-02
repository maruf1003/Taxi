from taxi.api.serializer import UserSerializer
from taxi.models import CustomUser
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer





