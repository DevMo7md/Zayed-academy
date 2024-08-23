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
        

        paymob_manager = PaymobCardManager()
        integration_id = 4602060  # Your Payment Integration id to spicify what payment is it like (cards, or mobile wallet, etc..)
        amount = 120  # amount that you want the user to pay
        currency = "EGP"  # currency USD or EGP , etc..
        payment_key = paymob_manager.getPaymentKey(amount=amount, currency=currency, integration_id=integration_id)

        payment_url = f"https://accept.paymob.com/api/acceptance/iframes/853728?payment_token={payment_key}"

        subscription.start_date = datetime.now()
        subscription.end_date = subscription.start_date + timedelta(days=30)
        subscription.save()
        return redirect(payment_url)

    return render(request, 'Subscription/subscribe.html')


@login_required
def payment_success(request):
    
    return render(request, 'subscription/success.html')

#https://accept.paymob.com/api/acceptance/iframes/853728?payment_token={payment_key_obtained_previously}

