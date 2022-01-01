from django.contrib import admin

from wallet.models import Wallet, Transfer

admin.site.register(Wallet)
admin.site.register(Transfer)
