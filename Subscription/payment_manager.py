import requests


apiKey = 'ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1Rnek1URTJMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuOTVtRlJfcm9xSzlodzlpaU80UVoxUmRaRFZ2T3BiY0RQcFdGbjc0R05POVltbGpxUzZjcV9ZUV81THV2bGFzYzdpcVBLaVhLZUd4Qm40anFtMFp5MlE='

class PaymobCardManager:
    def getPaymentKey(self, amount, currency, integration_id):
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
                integration_id = integration_id
            )
            return paymentKey
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
 
    def _getPaymentKey(self, authanticationToken, orderId, amount, currency, integration_id):
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
                    "first_name": "Clifford",
                    "last_name": "Nicolas",
                    "email": "claudette09@exa.com",
                    "phone_number": "+86(8)9135210487",
                    "apartment": "NA",
                    "floor": "NA",
                    "street": "NA",
                    "building": "NA",
                    "shipping_method": "NA",
                    "postal_code": "NA",
                    "city": "NA",
                    "country": "NA",
                    "state": "NA"
                    }
                    }
        )
        print("paymentkey")
        print("---------------------------")
        print(response.json()["token"])
        print("---------------------------")
        return response.json()["token"]
