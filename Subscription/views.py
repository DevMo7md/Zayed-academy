from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscription
from LP_app.models import *
from datetime import datetime, timedelta
import requests
from django.conf import settings

@login_required
def subscribe(request):
    if request.method == 'POST':
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        if created:  # إذا كان الاشتراك جديدًا
            subscription.start_date = datetime.now()
            subscription.end_date = subscription.start_date + timedelta(days=30)
            subscription.save()
        return redirect('subscription_success')
    
    return render(request, 'subscription/subscribe.html')

@login_required
def payment_success(request):
    subscription, created = Subscription.objects.get_or_create(user=request.user)
    if created:  # إذا كان الاشتراك جديدًا
        subscription.start_date = datetime.now()
        subscription.end_date = subscription.start_date + timedelta(days=30)
        subscription.save()
    return render(request, 'subscription/success.html')



@login_required
def initiate_payment(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        # بيانات الدفع
        amount = 100  # المبلغ بالقرش، لذلك 100 يعني 1 جنيه مصري
        auth_token = get_paymob_auth_token()

        # إرسال طلب إنشاء الطلب
        order_data = {
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": amount,
            "currency": "EGP",
            "merchant_order_id": request.user.id,  # رقم المستخدم هو معرّف الطلب
            "items": []
        }
        order_response = requests.post("https://accept.paymob.com/api/ecommerce/orders", json=order_data)
        order = order_response.json()

        # الحصول على رابط الدفع
        payment_key_data = {
            "auth_token": auth_token,
            "amount_cents": amount,
            "expiration": 3600,
            "order_id": order['id'],
            "billing_data": {
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "phone_number": student.phone_num,
                "email": request.user.email,
                "country": "EG",
                "city": "Cairo",
                "street": "Street Name",
                "building": "Building Number",
                "floor": "5",
                "apartment": "5"
            },
            "currency": "EGP",
            "integration_id": settings.PAYMOB_INTEGRATION_ID
        }
        payment_key_response = requests.post("https://accept.paymob.com/api/acceptance/payment_keys", json=payment_key_data)
        payment_key = payment_key_response.json()

        # توجيه المستخدم إلى صفحة الدفع
        payment_url = f"https://accept.paymobsolutions.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_key['token']}"
        return redirect(payment_url)

    return render(request, 'subscription/subscribe.html')


def get_paymob_auth_token():
    auth_data = {
        "api_key": settings.PAYMOB_API_KEY
    }
    response = requests.post("https://accept.paymob.com/api/auth/tokens", json=auth_data)
    return response.json()['token']
