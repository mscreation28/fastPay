from django.contrib import admin

from ewalletapp.models import Profile,Jio,Vodafone,Transaction

admin.site.register(Profile)
admin.site.register(Jio)
admin.site.register(Vodafone)
admin.site.register(Transaction)