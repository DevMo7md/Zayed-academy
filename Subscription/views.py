from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscription
from LP_app.models import *
from datetime import datetime, timedelta
import requests
from django.conf import settings
from .payment_manager import PaymobCardManager

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
        #student = Student.objects.get(user=request.user)
        paymob_manager = PaymobCardManager()
        integration_id = 4602060  # Your Payment Integration id to spicify what payment is it like (cards, or mobile wallet, etc..)
        amount = request.POST.get('amount')  # amount that you want the user to pay
        currency = "EGP"  # currency USD or EGP , etc..
        payment_key = paymob_manager.getPaymentKey(amount=amount, currency=currency, integration_id=integration_id)

        payment_url = f"https://accept.paymobsolutions.com/api/acceptance/iframes/853728?payment_token={payment_key}"
        
        subscription.start_date = datetime.now()
        subscription.end_date = subscription.start_date + timedelta(days=30)
        subscription.save()
        return redirect(payment_url)
    return render(request, 'subscription/success.html')


@login_required
def initiate_payment(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        paymob_manager = PaymobCardManager()
        integration_id = 4602060  # Your Payment Integration id to spicify what payment is it like (cards, or mobile wallet, etc..)
        amount = request.POST.get('amount')  # amount that you want the user to pay
        currency = "EGP"  # currency USD or EGP , etc..
        payment_key = paymob_manager.getPaymentKey(amount=amount, currency=currency, integration_id=integration_id)

        payment_url = f"https://accept.paymobsolutions.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_key}"
        return redirect(payment_url)

    return render(request, 'subscription/subscribe.html')
