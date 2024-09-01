import requests
from django.shortcuts import get_object_or_404
from LP_app.models import *



apiKey = 'ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1Rnek1URTJMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuOTVtRlJfcm9xSzlodzlpaU80UVoxUmRaRFZ2T3BiY0RQcFdGbjc0R05POVltbGpxUzZjcV9ZUV81THV2bGFzYzdpcVBLaVhLZUd4Qm40anFtMFp5MlE='




class PaymobCardManager:
    def getPaymentKey(self, amount, currency, integration_id, email, phone_number,first_name, last_name):
        try:
            authanticationToken = self._getAuthanticationToken(api_key=apiKey)

            orderId = self._getOrderId(
                authanticationToken=authanticationToken,
                amount=str(100 * amount),
                currency=currency,
            )

            paymentKey = self._getPaymentKey(
                authanticationToken=authanticationToken,
                amount=str(100 * amount),
                currency=currency,
                orderId=str(orderId),
                integration_id = integration_id,
                email=email,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name
            )
            return paymentKey, orderId
        except Exception as e:
            print("Exc==========================================")
            print(str(e))
            raise Exception()

    def _getAuthanticationToken(self, api_key):
        response = requests.post(
            "https://accept.paymob.com/api/auth/tokens",
            json={
                "api_key": api_key,
            }
        )
        print("auth token")
        print("---------------------------")
        print(response.json())
        print("-----------------------------")
        return response.json()["token"]

    def _getOrderId(self, authanticationToken, amount, currency):
        response = requests.post(
            "https://accept.paymob.com/api/ecommerce/orders",
            json={
                "auth_token": authanticationToken,
                "amount_cents": amount,
                "currency": currency,
                "delivery_needed": False,
                "items": [],
            }
        )
        print("orderid")
        print("---------------------------")
        print(response.json()["id"])
        print("--------------------------")
        return response.json()["id"]

    def _getPaymentKey(self, authanticationToken, orderId, amount, currency, integration_id, email, phone_number, first_name, last_name):
        response = requests.post(
            "https://accept.paymob.com/api/acceptance/payment_keys",
            json={
                "expiration": 3600,
                "auth_token": authanticationToken,
                "order_id": orderId,
                "amount_cents": amount,
                "currency": currency,
                "integration_id": integration_id,
                "billing_data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone_number": phone_number,
                    "apartment": "NA",
                    "floor": "NA",
                    "street": "NA",
                    "building": "NA",
                    "shipping_method": "NA",
                    "postal_code": "NA",
                    "city": "NA",
                    "country": "Egypt",
                    "state": "NA"
                    }
                    }
        )
        print("paymentkey")
        print("---------------------------")
        print(response.json()["token"])
        print("---------------------------")
        return response.json()["token"]
    








class PaymobWalletManager:
    def getPaymentKey(self, amount, currency, integration_id,email, phone_number, name):
        try:
            authanticationToken = self._getAuthanticationToken(api_key=apiKey)

            orderId = self._getOrderId(
                authanticationToken=authanticationToken,
                amount=str(100 * amount),
                currency=currency,
            )

            paymentKey = self._getPaymentKey(
                authanticationToken=authanticationToken,
                amount=str(100 * amount),
                currency=currency,
                orderId=str(orderId),
                integration_id = integration_id,
                email=email,
                phone_number=phone_number,
                name=name,
            )
            return paymentKey,orderId
        except Exception as e:
            print("Exc==========================================")
            print(str(e))
            raise Exception()

    def _getAuthanticationToken(self, api_key):
        response = requests.post(
            "https://accept.paymob.com/api/auth/tokens",
            json={
                "api_key": api_key,
            }
        )
        print("auth token")
        print("---------------------------")
        print(response.json()["token"])
        print("-----------------------------")
        return response.json()["token"]

    def _getOrderId(self, authanticationToken, amount, currency):
        response = requests.post(
            "https://accept.paymob.com/api/ecommerce/orders",
            json={
                "auth_token": authanticationToken,
                "amount_cents": amount,
                "currency": currency,
                "delivery_needed": False,
                "items": [],
            }
        )
        print("orderid")
        print("---------------------------")
        print(response.json()["id"])
        print("--------------------------")
        return response.json()["id"]

    def _getPaymentKey(self, authanticationToken, orderId, amount, currency, integration_id,email, phone_number, first_name, last_name):
        response = requests.post(
            "https://accept.paymob.com/api/acceptance/payment_keys",
            json={
                "expiration": 3600,
                "auth_token": authanticationToken,
                "order_id": orderId,
                "amount_cents": amount,
                "currency": currency,
                "integration_id": integration_id,
                "billing_data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone_number": phone_number,
                    "apartment": "NA",
                    "floor": "NA",
                    "street": "NA",
                    "building": "NA",
                    "shipping_method": "NA",
                    "postal_code": "NA",
                    "city": "NA",
                    "country": "Egypt",
                    "state": "NA"
                    }
                    }
        )
        print("paymentkey")
        print("---------------------------")
        print(response.json()["token"])
        print("---------------------------")
        return response.json()["token"]







#get the url that u will pay throw

def get_wallet_redirect_url(payment_key,wallet_num):
    response = requests.post(
        "https://accept.paymob.com/api/acceptance/payments/pay",
        json={
            "source": {
                "identifier": f"{wallet_num}", 
                "subtype": "WALLET"
            },
            "payment_token": payment_key  
        }
        )
    print("redirect_url")
    print(response.json()['iframe_redirection_url'])

    print("---------------------------")
    return response.json()['iframe_redirection_url']






