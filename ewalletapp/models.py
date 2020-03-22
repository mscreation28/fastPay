from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10,blank=True,null=True)
    birth_date = models.DateField(null=True, blank=True)
    amount = models.IntegerField(blank=True, null=True)
    debit = models.IntegerField(blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    profile_pic=models.ImageField(upload_to='images/',default="images/profile_pic.jpg")

    def __str__(self):
        return f'{self.user} Profile' 

class Jio(models.Model):
    mobile_number=models.IntegerField(blank=True,null=True)
    amount=models.IntegerField(blank=True, null=True)
    state=models.CharField(max_length=10)
    id=models.IntegerField(primary_key=True)
    recharge_date=models.DateField(auto_now_add=True)

class Vodafone(models.Model):
    mobile_number=models.IntegerField(blank=True,null=True)
    amount=models.IntegerField(blank=True, null=True)
    state=models.CharField(max_length=10)
    id=models.IntegerField(primary_key=True)
    recharge_date=models.DateField(auto_now_add=True)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t_type=models.CharField(max_length=100)
    amount=models.IntegerField()
    receiver=models.CharField(max_length=25)
    time=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} Transaction' 

