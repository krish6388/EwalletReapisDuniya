from django.shortcuts import get_object_or_404, render, HttpResponse
import razorpay
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# RECHARGING WALLET
@api_view(['POST', 'GET'])
def wallet(request):

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        amount = request.POST.get("amount")

        amount = int(amount) * 100

        client = razorpay.Client(auth=('rzp_test_77IDH3xrR0OXbn', 'HS489Vn3xpQXGEweXX2DG4Dn'))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        payment_id = payment['id']
        
        context = {
        'payment_id': payment_id,
        'amount': amount,
        'user_id': user_id,
        'flag': 1
    }
        return render(request, 'recharge.html', context=context)
    
    elif request.method == 'GET':
        return render(request, 'recharge.html')
    return HttpResponse("Wallet")

# VERIFICATION DURING CHECKOUT
@api_view(['POST', 'GET'])
def verified(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        payment_id = request.POST.get('payment_id')

        wallet_obj = Wallet.objects.filter(user_id = user_id)[0]
        credits = int(wallet_obj.amount)
        total = int(request.POST.get('total'))
        
        # TRANSACTION RECORD FOR ADDING CREDITS TO WALLET FOR COMPLETE PAYMENT
        if credits <= total:
            transaction_obj = Transactions(
            user_id = user_id,
            amount = total - credits,
            timestamp = datetime.now(),
            payment_id = payment_id,
            status = "ADDED To Wallet"
        )
            transaction_obj.save()

            wallet_obj.amount = 0
            wallet_obj.save()
        else:
            wallet_obj.amount = wallet_obj.amount - total
            wallet_obj.save()

        # TRANSACTION RECORD FOR COMPLETE PAYMENT
        transaction_obj = Transactions(
            user_id = user_id,
            amount = total,
            timestamp = datetime.now(),
            payment_id = payment_id,
            status = "DEDUCTED"
        )
        transaction_obj.save()

    return render(request, 'success.html')

# @csrf_exempt
@api_view(['POST', 'GET'])
def success(request):
    if request.method == 'POST':

        user_id = request.POST.get("user_id")
        amount = int(request.POST.get("amount"))/100
        payment_id = request.POST.get('payment_id')

        wallet_obj = Wallet.objects.filter(user_id = user_id)
        if not wallet_obj:
            return HttpResponse("No user id found!")
        
        # ADDING CREDITS TO WALLET
        a = wallet_obj[0].amount
        wallet_obj[0].amount =int(a)+ int(amount)
        wallet_obj[0].save()

        # TRANSACTION RECORD FOR ADDING CREDITS TO WALLET 
        transaction_obj = Transactions(
            user_id = user_id,
            amount = amount,
            timestamp = datetime.now(),
            payment_id = payment_id,
            status = "ADDED"
        )
        transaction_obj.save()
    return render(request, 'verified.html')


@api_view(['GET', 'POST'])
def checkout(request):
    if request.method == 'POST':
        total = int(request.POST.get('total'))
        print(total)
        user_id = request.POST.get('user_id')

        wallet_obj = Wallet.objects.filter(user_id = user_id)[0]

        RepairCredits = int(wallet_obj.amount)

        if RepairCredits < total:
            newAmt = total - RepairCredits
        
        else:
            newAmt = 0

        AmtinRs = newAmt * 100
        print(AmtinRs)
        payment_id="Paid by wallet"
        if AmtinRs >0 : 
            client = razorpay.Client(auth=('rzp_test_77IDH3xrR0OXbn', 'HS489Vn3xpQXGEweXX2DG4Dn'))
            payment = client.order.create({'amount': AmtinRs, 'currency': 'INR', 'payment_capture': '1'})
            payment_id = payment['id']
        
        context = {
            'user_id': user_id,
            'total': total,
            'rCredit': RepairCredits,
            'newAmt': newAmt,
            'AmtinRs': AmtinRs, 
            'payment_id': payment_id
        }
        if newAmt == 0:

            # ADDING CREDITS TO WALLET FOR COMPLETE TRANSACTION
            wallet_obj = Wallet.objects.filter(user_id = user_id)[0]
            wallet_obj.amount = wallet_obj.amount - total
            wallet_obj.save()

            # TRANSACTION RECORD FOR DEDUCTING MONEY FOR COMPLETE PAYMENT
            transaction_obj = Transactions(
                user_id = user_id,
                amount = total,
                timestamp = datetime.now(),
                payment_id = payment_id,
                status = "DEDUCTED"
            )
            transaction_obj.save()


            return render(request, 'success.html', context=context)
        else:
            return render(request, 'checkout.html', context=context)
    return render(request, 'useWallet.html')