from django.contrib import admin
from .models import *


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    pass


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
