from django.contrib import admin
from .models import (
    CustomUser,
    AdvertiseInfo,
    Passport,
    UserRequisites,
)


class AdvertiseInfoInline(admin.TabularInline):
    model = AdvertiseInfo
    extra = 0
    can_delete = False
    verbose_name = 'Пакет рекламной информации'
    verbose_name_plural = 'Пакеты рекламной информации'


class PassportInline(admin.StackedInline):
    model = Passport
    extra = 0
    can_delete = False
    verbose_name = 'Паспорт'
    verbose_name_plural = 'Паспорта'


class UserRequisitesInline(admin.TabularInline):
    model = UserRequisites
    extra = 1
    verbose_name = 'Реквизит'
    verbose_name_plural = 'Реквизиты'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_email_verified')
    list_filter = ('is_email_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'last_name', 'first_name', 'phone_number')
    inlines = [AdvertiseInfoInline]
    fieldsets = (
        ('Общая информация', {'fields': (
            'email', 'username', 'first_name', 'last_name', 'middle_name', 'phone_number', 'is_email_verified')}),
        ('Допуски', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ('user', 'series', 'number', 'release_date', 'issued', 'unit_code')
    search_fields = ('series', 'number', 'user__username', 'user__email')
    list_filter = ('release_date',)


@admin.register(UserRequisites)
class UserRequisitesAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'bic', 'user_account', 'card_number')
    search_fields = ('bank_name', 'bic', 'user__username', 'user__email')
    list_filter = ('bank_name',)
