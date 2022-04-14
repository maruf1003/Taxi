from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drive.api.serializer import *
from drive.models import *
import math
from django.contrib.gis.db.models.functions import GeometryDistance


#
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # token uchun
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
@api_view(["POST"])
@permission_classes([AllowAny])
def set_location(request):
    x1 = request.data["x1"]
    y1 = request.data["y1"]
    driver_id = request.data["driver_id"]

    ref_location = Point(float(x1), float(y1), srid=4326)
    driver = Driver.objects.filter(pk=driver_id).first()
    if driver:
        driver.longitude = x1,
        driver.latitude = y1,
        driver.point = ref_location,
        driver.save()
        Location.object.create(
            longitude=x1,
            latitude=y1,
            point=ref_location,
            driver=driver
        ).save()
    return Response({"status": 1})


@api_view(["POST"])
@permission_classes([AllowAny])
def get_drivers(request):
    qs = Driver.objects.all()
    x1 = request.data["x1"]
    y1 = request.data["y1"]

    ref_location = Point(float(x1), float(y1), srid=4326)

    qs = qs.annotate(distance=GeometryDistance("point", ref_location)).order_by('distance')

    return Response({"status": 1, "data": DriverSerializers(qs, many=True, context={'request': request}).data})


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
            "car_type": Car_typeSerializers(car_type, many=True, context={"request": request, 'langht': langht}).data,
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tell_me(request):
    try:
        data_time = request.data.get('data_time')
        place = request.data.get('place')
        accident = request.data.get('accident')
        driver_id = request.data.get('driver_id')
        user_id = request.data.get('user_id')
        photo = request.data.get('photo')
        upload = request.FILES['photo']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        tellme = TellMe.objects.create(
            data_time=data_time,
            place=place,
            accident=accident,
            photo=file,
            driver_id=driver_id,
            user_id=user_id,
        ).save()
        res = {
            'status': 1,
            'msg': 'self tellme',
        }
        return Response(res)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'error'
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tell_us(request):
    try:
        massage = request.data.get('massage')
        driver_id = request.data.get('driver_id')
        user_id = request.data.get('user_id')
        tell_us = TellMe.objects.create(
            massage=massage,
            driver_id=driver_id,
            user_id=user_id,
        ).save()
        res = {
            'status': 1,
            'msg': 'self tell_us',
        }
        return Response(res)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'error'
        }
        return Response(res)
