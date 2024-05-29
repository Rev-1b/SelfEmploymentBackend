from django.contrib import admin
from .models import *


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    pass


@admin.register(Additional)
class AdditionalAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseAttachment)
class BaseAttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Act)
class ActAdmin(admin.ModelAdmin):
    pass


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    pass
