from django.shortcuts import render, redirect
from django.urls import reverse
import requests
import json
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
from content.models import Content
from django.http import HttpResponse
from banking.models import StripeCustomer, ConnectStripeAccount
from django.views.decorators.csrf import csrf_exempt
import stripe

def connectCreation(request, error=None):
    if error:
        message = "Something didnt go right, please try again. If error presist please contact us with error code:" + error
        return render(request, 'pages/5/connect.html', {'messsage':message})
    #in templates after successful creation, change button to edit payout info
    else:
        return render(request, 'pages/5/connect.html')

def confConnect(request):
    Acode = request.GET.get('code')
    if Acode:
        data = [
        ('client_secret', settings.STRIPE_KEY),
        ('code', Acode),
        ('grant_type', 'authorization_code'),
        ]

    response = requests.post('https://connect.stripe.com/oauth/token', data=data)
    if response.status_code == 200:
        a = json.loads(response.text)
        ConnectStripeAccount.objects.create(stripe_id=(a['stripe_user_id']), user=request.user)
        #signal on create connect stripe changes users profile to celeb
    else:
        error_code = response.status_code
        #use the error for logging
        return redirect(reverse('banking:preConnect', kwargs={'error':error_code}))


def precard(request):
    source = request.POST.get('stripeToken')
    #save to user's stripe model
    return render(request, 'pages/5/token.html')


def ViewTransaction(request):
    #use js to fetch more data, click->popup->api call->data
    history = request.user.TransactionHistory.all()
    return render(request, 'banking/history.html', {'history':history})

def modifyCard(request):
    if request.user.stripe_id:
        source = request.POST.get('stripeToken')
        stripe.api_key =  settings.STRIPE_KEY
        a = StripeCustomer.objects.get(user=request.user)
        a.delete()
        stripe.Customer.modify(request.user.StripeCustomer.stripe_id, source=source)
        StripeCustomer.objects.create(user=request.user, stripe_id=customer.id)
        return redirect(reverse('home:home'))
    else:
        source = request.POST.get('stripeToken')
        stripe.api_key =  settings.STRIPE_KEY
        customer = stripe.Customer.create(
          source=source,
          email= request.user.email,
          metadata={'username':request.user.username}
        )
        StripeCustomer.objects.create(user=request.user, stripe_id=customer.id)
        return redirect(reverse('home:home'))
