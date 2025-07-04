from django.contrib import admin
from .models import *


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'status', 'deal_amount', 'customer')
    list_filter = ('status',)
    search_fields = ('number',)


@admin.register(Additional)
class AdditionalAdmin(admin.ModelAdmin):
    pass


@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    pass


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass


@admin.register(CheckModel)
class CheckModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserTemplate)
class UserTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass