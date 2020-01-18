from django.contrib import admin
from banking.models import TransactionHistory, StripeCustomer, ConnectStripeAccount

admin.site.register(TransactionHistory)
admin.site.register(StripeCustomer)
admin.site.register(ConnectStripeAccount)
