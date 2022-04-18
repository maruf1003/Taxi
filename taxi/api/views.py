from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from taxi.api.serializer import *
from taxi.models import CustomUser
from rest_framework_jwt.settings import api_settings
import random

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # token uchun
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

import requests


def get_token():
    url = "http://notify.eskiz.uz/api/auth/login"

    payload = {
        'email': 'test@eskiz.uz',
        'password': 'j6DWtQjjpLDNjWEk74Sx'
    }
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    data = data.get('data')
    return data.get('token')


def send_sms(phone, text):
    # email = EmailMessage('Veri', text, from_email="marufkulmatov10@gmail.com", to=[mail])
    #
    # email.send()

    url = "http://notify.eskiz.uz/api/message/sms/send-global"
    token = get_token()
    payload = {
        'mobile_phone': phone,
        'message': text,
        'from': '4546',
        'country_code': 'uz'
    }

    headers = {
        'Authorization': 'Bearer ' + str(token)
    }

    response = requests.request("POST", url, headers=headers, data=payload)


# User log in (avtorizatsiya 1-martta royxatdan otganda)
@api_view(['POST'])
@permission_classes([AllowAny])
def save_register(request):
    try:
        # return Response(send_sms("998908230595", "TEST 1"))
        username = request.data.get('mobile_phone')
        first_name = request.data.get('name')
        # email = request.data.get('email')
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
                first_name=first_name
                # email=email,
            )
        elif user:
            send_sms(username, "Sizning tasdiqlash codingiz: " + str(sms_code))

            res = {
                'msg': 'User exits',
                'status': 0,
            }
            return Response(res)
        user.set_password(str(password))
        user.sms_code = sms_code
        # user.email = email
        user.first_name = first_name
        user.save()
        send_sms(username, "Sizning tasdiqlash codingiz: " + str(sms_code))

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
        username = request.data['mobile_phone']
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
        login = request.data['mobile_phone']
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete(request):
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user:
        user.delete()
    return Response({"status": 1, "msg": "Deleted"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update(request):
    name = request.POST.get("first_name")
    username = request.POST.get("mobile_phone")
    avatar = request.POST.get("avatar")
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user:
        if 'avatar' in request.FILES:
            upload = request.FILES['avatar']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            user.avatar = file
        user.fullname = name
        user.avatar = avatar
        user.username = username
        user.save()
        res = {
            "status": 1,
            "error": "changed successfully",
            "user": UserSerializer(user, many=False).data
        }
    else:
        res = {
            "status": 0,
            "error": "wrong changed"
        }
    return Response(res)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user:
        res = {
            "status": 1,
            "error": "changed successfully",
            "user": UserSerializer(user, many=False).data
        }
    else:
        res = {
            "status": 0,
            "error": "has not like user"
        }
    return Response(res)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_faq(request):
    # faq_id = request.GET("faq_id")
    faq = Faq.objects.all()
    if faq:
        res = {
            "status": 1,
            "msg": "call successfully",
            "Faq": FaqSerializer(Faq, many=False).data
        }
    else:
        res = {
            "status": 0,
            "error": "ERROE!"
        }
    return Response(res)
