from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscription_success/', views.payment_success, name='subscription_success'),

]
