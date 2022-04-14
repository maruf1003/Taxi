import hashlib
import json
from datetime import datetime

from django.contrib.sites import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from drive.api.authorization import click_authorization
from drive.api.serializer import ClickUzSerializer
from drive.models import Order, Transaction
from rest_framework.renderers import JSONRenderer

INVALID_AMOUNT = -2
INVALID_ACTION = -4
TRANSACTION_NOT_FOUND = -6
ORDER_NOT_FOUND = -5
PREPARE = '0'
COMPLETE = '1'
A_LACK_OF_MONEY = '-5017'
A_LACK_OF_MONEY_CODE = -9
AUTHORIZATION_FAIL = 'AUTHORIZATION_FAIL'
AUTHORIZATION_FAIL_CODE = -1
ORDER_FOUND = True


class ClickUzMerchantAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    VALIDATE_CLASS = None
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = ClickUzSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        METHODS = {
            PREPARE: self.prepare,
            COMPLETE: self.complete
        }

        merchant_trans_id = serializer.validated_data['merchant_trans_id']
        amount = serializer.validated_data['amount']
        action = serializer.validated_data['action']

        if click_authorization(**serializer.validated_data) is False:
            return Response({
                "error": AUTHORIZATION_FAIL_CODE,
                "error_note": AUTHORIZATION_FAIL
            })
        if len(merchant_trans_id) > 10:
            return Response({
                "error": -5,
                "error_note": "Int large"
            })

        order = Order.objects.filter(pk=merchant_trans_id).first()
        if order:
            result = METHODS[action](**serializer.validated_data, response_data=serializer.validated_data)
            return Response(result)
        return Response({"error": "Order not found"})

    def prepare(self, click_trans_id: str, merchant_trans_id: str, amount: str, sign_string: str, sign_time: str,
                response_data: dict,
                *args, **kwargs) -> dict:
        """
        :param click_trans_id:
        :param merchant_trans_id:
        :param amount:
        :param sign_string:
        :param response_data:
        :param args:
        :return:
        """
        transaction = Transaction.objects.create(
            click_trans_id=click_trans_id,
            merchant_trans_id=merchant_trans_id,
            amount=amount,
            action=PREPARE,
            sign_string=sign_string,
            sign_datetime=sign_time,
        )
        response_data.update(merchant_prepare_id=transaction.id)
        return response_data

    def complete(self, click_trans_id, amount, error, merchant_prepare_id,
                 response_data, action, *args, **kwargs):
        """
        :param click_trans_id:
        :param merchant_trans_id:
        :param amount:
        :param sign_string:
        :param error:
        :param merchant_prepare_id:
        :param response_data:
        :param action:
        :param args:
        :return:
        """
        try:
            transaction = Transaction.objects.get(pk=merchant_prepare_id)

            if error == A_LACK_OF_MONEY:
                response_data.update(error=A_LACK_OF_MONEY_CODE)
                transaction.action = A_LACK_OF_MONEY
                transaction.status = Transaction.CANCELED
                transaction.save()
                return response_data

            if transaction.action == A_LACK_OF_MONEY:
                response_data.update(error=A_LACK_OF_MONEY_CODE)
                return response_data

            if transaction.amount != amount:
                response_data.update(error=INVALID_AMOUNT)
                return response_data

            if transaction.action == action:
                response_data.update(error=INVALID_ACTION)
                return response_data

            transaction.action = action
            transaction.status = Transaction.FINISHED
            transaction.save()
            response_data.update(merchant_confirm_id=transaction.id)
            order = Order.objects.filter(pk=transaction.merchant_trans_id).first()
            order.status = 1
            order.save()
            return response_data
        except Transaction.DoesNotExist:
            response_data.update(error=TRANSACTION_NOT_FOUND)
            return response_data


#   Scan card and pay
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cards_verify(request):
    try:
        time_now = int(datetime.datetime.utcnow().timestamp())
        hash = hashlib.sha1((str(time_now) + 'password').encode("utf-8")).hexdigest()
        token = "5875:" + hash + ":" + str(time_now)

        url = "https://api.click.uz/v2/merchant/card_token/verify/"

        card_token = request.data["card_token"]
        sms_code = request.data["sms_code"]
        amount = request.data["amount"]

        payload = json.dumps({
            "service_id": "1234",
            "card_token": card_token,
            "sms_code": sms_code
        })
        headers = {
            'Auth': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response = json.loads(response.text)
        error_code = response.get("error_code", 500)
        if error_code == 0:
            url_payment = "https://api.click.uz/v2/merchant/card_token/payment"

            payload = json.dumps({
                "service_id": 1234,
                "card_token": card_token,
                "amount": amount,
                "transaction_parameter": 202598
            })
            headers = {
                'Auth': token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response_payment = requests.request("POST", url_payment, headers=headers, data=payload)
            response_payment = json.loads(response_payment.text)
            error_code = response.get("error_code", 500)

            if error_code == 0:
                url_delete = "https://api.click.uz/v2/merchant/card_token/7024/" + card_token
                payload = {}
                headers = {
                    'Auth': token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                response = requests.request("DELETE", url_delete, headers=headers, data=payload)
            return Response(response_payment)
        return Response(response)
    except KeyError:
        res = {
            "status": 0,
            "msg": ""
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def cards_create(request):
    try:
        card_number = request.data["card_number"]
        expire_date = request.data["expire_date"]
        time_now = int(datetime.datetime.utcnow().timestamp())
        hash = hashlib.sha1((str(time_now) + 'possword').encode("utf-8")).hexdigest()
        token = "5875:" + hash + ":" + str(time_now)

        url = "https://api.click.uz/v2/merchant/card_token/request"

        payload = json.dumps({
            "service_id": "1234",
            "card_number": card_number,
            "expire_date": expire_date
        })
        headers = {
            'Auth': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return Response(json.loads(response.text))
    except KeyError:
        res = {
            "status": 0,
            "msg": ""
        }
        return Response(res)
