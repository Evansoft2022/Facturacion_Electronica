from django.contrib import admin
from .models import *

admin.site.register(POS)
admin.site.register(Payment_Form_Invoice_POS)
admin.site.register(Wallet_POS)

