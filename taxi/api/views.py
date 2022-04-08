from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from taxi.api.serializer import *
from taxi.models import CustomUser
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from django.core.mail import send_mail
import random
from django.core.mail import EmailMessage

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # token uchun
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



def send_sms(mail, text):
    email = EmailMessage('Veri', text,from_email="marufkulmatov10@gmail.com", to=[mail])
    email.send()
# User log in (avtorizatsiya 1-martta royxatdan otganda)
@api_view(['POST'])
@permission_classes([AllowAny, ])
def save_register(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not login_view:
            res = {
                'status': 0,
                'msg': 'Login empty',
            }
            return Response(res)

        user = CustomUser.objects.filter(username=username).first()
        sms_code = random.randint(1000, 9999)

        if not user:
            user = CustomUser.objects.create(
                username=username,
                email=email,
            )
        elif user:
            send_sms(email, "Sizning tasdiqlash codingiz: " + str(sms_code))

            res = {
                'msg': 'User exits',
                'status': 0,
            }
            return Response(res)
        user.set_password(str(password))
        user.sms_code = sms_code
        user.email = email
        user.save()
        send_sms(email, "Sizning tasdiqlash codingiz: " + str(sms_code))

        if user:
            result = {
                'status': 1,
                'msg': 'Sms sended',
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

@api_view(["POST"])
@permission_classes([AllowAny])
def accept_confirmation(request):  # user tomonidan code orqali tasdiqlash
    try:
        sms_code = request.data['sms_code']
        username = request.data['username']
        user = CustomUser.objects.filter(username=username).first()
        if user and str(user.sms_code) == str(sms_code):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.save()
            res = {
                "status": 1,
                "msg": "successful",
                "user": UserSerializer(user, many=False, context={"request": request}).data,
                "token": token
            }
        else:
            res = {
                "status": 0,
                "msg": "EROR",
            }
        return Response(res)
    except KeyError:
        res = {
            "status": 0,
            "error": "Key error"
        }
    return Response(res)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    try:
        login = request.data['login']
        password = request.data['password']
        # user name va paroli biz kiritgan qiymatlarga teng bo'lsa login qilamiz (kirishga ruxsat berilsdi)
        user = CustomUser.objects.filter(username=login).first()
        if user and user.check_password(password):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            res = {
                "status": 1,
                "msg": "Login",
                "user": UserSerializer(user, many=False).data,
                "token": token
            }
        else:
            res = {
                "status": 0,
                "error": "login or password error"
            }
        return Response(res)

    except KeyError:
        res = {
            "status": 0,
            "error": "Key error"
        }
    return Response(res)


# UP_DATE USER
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    user = request.user
    if user:
        if 'image' in request.FILES:
            upload = request.FILES['image']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            user.image = file
        user.name = first_name
        user.last_name = last_name
        user.save()
        res = {
            "status": 1,
            "error": "changed successfully"
        }
    else:
        res = {
            "status": 0,
            "error": "wrong changed"
        }
    return Response(res)


# passwordni'ni yangilash
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_password(request):
    try:
        password = request.data['password']
        old_password = request.data['old_password']
        user = request.user
        if user and user.check_password(old_password):
            user.set_password(password)
            user.save()
            res = {
                "password changed successfully"
            }
        else:
            res = {
                "status": 0,
                "error": "wrong password"
            }
        return Response(res)
    except KeyError:
        res = {
            "status": 0,
            "error": "Key error"
        }

    return Response(res)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])    # zakazdan song xaydovchining dannylarini korado
# def driver_view(request):
#     user_id = request.GET.get("user_id")
#     user = CustomUser.objects.filter(pk=user_id).first()
#     if user:
#         res = {
#             "status": 1,
#             "user": User_driverSerializer(user, many=False).data,
#         }
#     else:
#         res = {
#             "status": 0,
#             "msg": "Key error"
#         }
#     return Response(res)
