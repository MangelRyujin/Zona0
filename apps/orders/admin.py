from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(ReceiveOSP)
admin.site.register(TransferManagerOrderUsers)
admin.site.register(TransferOSP)