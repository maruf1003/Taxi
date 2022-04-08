from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from drive.api.serializer import DriverSerializers
from drive.models import Driver


class DriverViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
