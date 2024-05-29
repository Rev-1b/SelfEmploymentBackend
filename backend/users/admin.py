from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertiseInfo)
class AdvertiseInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRequisites)
class UserRequisitesAdmin(admin.ModelAdmin):
    pass