from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drive.api.serializer import *
from drive.models import *
import math


#
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # token uchun
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#

from django.contrib.gis.db.models.functions import GeometryDistance
@api_view(["POST"])
@permission_classes([AllowAny])
def get_drivers(request):
    qs = Location.objects.all()
    x1 = request.data["x1"]
    y1 = request.data["y1"]

    ref_location = Point(float(x1), float(y1), srid=4326)

    qs = qs.annotate(distance=GeometryDistance("point", ref_location)).order_by('distance')

    return Response({"status":1, "data":LocationSerializers(qs, many=True, context={'request':request}).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_creat(request):
    try:
        x1 = request.data["x1"]
        x2 = request.data["x2"]
        y1 = request.data["y1"]
        y2 = request.data["y2"]
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        status = request.data["status"]
        # name = request.data["name"]

        order = Order.objects.create(
            from_longitude=x1,
            from_latitude=y1,
            to_longitude=x2,
            to_latitude=y2,
            status=status,
            user_id=request.user.id,
        )
        order.save()
        langht = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) * 100
        car_type = Car_type.objects.all()
        res = {
            "order": OrderCreatSerializers(order, many=False).data,
            "car_type": Car_typeSerializers(car_type, many=True, context={"request":request,'langht': langht}).data,
            "langht": "%.7f" % langht,

        }
        print(request.user)
        return Response(res)
    except KeyError:
        res = {
            "status": 0,
            "error": "Key error"
        }
    return Response(res)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def distance(request):
#     try:
#         x1 = request.data.get('x1')
#         x2 = request.data.get('x2')
#         y1 = request.data.get('y1')
#         y2 = request.data.get('y2')
#         x1 = float(x1)
#         x2 = float(x2)
#         y1 = float(y1)
#         y2 = float(y2)
#         if request.data.get != 0:
#             langht = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) * 100
#             res = {
#                 "langht": "%.7f" % langht,
#             }
#         else:
#             res = {
#                 "msg": "kordinatalarni kiriting"
#             }
#         return Response(res)
#
#     except KeyError:
#         res = {
#             "status": 0,
#             "error": "Key error"
#         }
#     return Response(res)
