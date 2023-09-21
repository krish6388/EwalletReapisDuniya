from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('wallet/', wallet, name='wallet'),
    path('success/', success, name='success'),
    path('verified/', verified, name='verified'),
    path('checkout/', checkout, name='checkout'),
]