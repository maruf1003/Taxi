from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from taxi.api.serializer import UserSerializer
from taxi.models import CustomUser
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from django.core.mail import send_mail
import random

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # token uchun
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER




# User log in (avtorizatsiya 1-martta royxatdan otganda)
@api_view(["POST"])
@permission_classes([AllowAny])  # ([HammagaRuxsat])
def save_registr(request):
    try:
        email = request.POST["email"]
        password = request.POST["password"]
        username = request.POST["username"]
        user = CustomUser.objects.filter(username=username).first()  # bu yerda unikal ma'lumot tekshiriladi
        if user:  # agar user kiritgan email'ga o'xshagan email bolsa-
            res = {
                "status": 0,
                "error": "User alerdy exits"  # -unda bunday user bor degan yozuv qaytaramiz
            }  # bolmasam-
            return Response(res)
        user = CustomUser.objects.create(  # -yangi user yaratamiz
            email=email,
            # aslida username unikal bolishi kerak
            username=username,
        )
        user.set_password(password)  # password tekshirish (password=password)
        sms_code = random.randint(1000, 9999)  # registratsiyadan song tasdiqlash uchun yuboriladigan cod
        user.sms_code = sms_code
        user.save()

        # token yasash
        payload = jwt_payload_handler(user)  # token uchun
        token = jwt_encode_handler(payload)
        send_mail("Taxi",
                  "SIzning tasdiqlash kodingiz " + str(sms_code), settings.EMAIL_HOST_USER, [email],
                  fail_silently=False)
        res = {
            "status": 1,
            "msg": "sms send",
            # "user": UserSerializer(user, many=False).data,  # user ma'lumotlari qaytarilayapti
            # "token": token
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
