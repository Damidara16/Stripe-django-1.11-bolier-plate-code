from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save



class TransactionHistory(models.Model):
    contents = (('Subscription', 'Subscription'),('Tip', 'Tip'),('Points', 'Points'))
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    celeb = models.CharField(max_length=200)
    transction_id = models.CharField(max_length=255)
    transctionType = models.CharField(max_length=20, choices=contents)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255)

    def __str__(self):
        return "{} | user - {} & plan - {} on {}".format(self.transctionType, self.user.username, self.celeb, self.date)

    def save(self, *args, **kwargs):
        if self.transctionType == 'Subscription':
            self.description = "{} | fan - {} & celeb - {} on {}".format(self.transctionType, self.user.username, self.celeb, self.date)
        else:
            None
        return super(TransactionHistory, self).save(*args, **kwargs)

class StripeCustomer(models.Model):
    user = models.ForeignKeyField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class ConnectStripeAccount(models.Model):
    user = models.OneToOneField(User)
    stripe_id = models.CharField(max_length=255)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #to get the charge or subscription info
    #ch = stripe.Charge.retrieve(transction_id, stripe_account=account.id)
    #print(ch)
    #sub = stripe.Subscription.retrieve(transction_id, stripe_account=account.id)

"""def changeStatus(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        user.profile.plan = True
        user.save()

post_save.connect(changeStatus, sender=ConnectStripeAccount)"""
