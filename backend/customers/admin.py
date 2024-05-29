from django.contrib import admin

from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerRequisites)
class CustomerRequisitesAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerContacts)
class CustomerContactsAdmin(admin.ModelAdmin):
    pass
