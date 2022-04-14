from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from drive.api.serializer import *
from drive.models import *


class DriverViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers


# class TellMeViewSet(mixins.ListModelMixin,
#                     mixins.RetrieveModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = TellMe.objects.all()
#     serializer_class = TellMeSerializer
#
#
# class ILeftMeViewSet(mixins.ListModelMixin,
#                      mixins.RetrieveModelMixin,
#                      viewsets.GenericViewSet):
#     queryset = TellMe.objects.all()
#     serializer_class = ILeftSerializer
