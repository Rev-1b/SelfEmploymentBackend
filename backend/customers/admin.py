from django.contrib import admin

from .models import *


class CustomerContactsInline(admin.TabularInline):
    model = CustomerContacts
    extra = 1


class CustomerRequisitesInline(admin.TabularInline):
    model = CustomerRequisites
    extra = 1


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'additional_id', 'customer_name', 'customer_type', 'user')
    list_filter = ('customer_type',)
    search_fields = ('customer_name', 'additional_id', 'user__username')
    ordering = ['additional_id']
    fieldsets = (
        ('Основная информация', {
            'fields': ('additional_id', 'user', 'customer_name', 'customer_type')
        }),
        ('Дополнительная информация', {
            'fields': ('post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address',
                       'okpo', 'okved', 'place_of_residence', 'ogrnip')
        }),
    )
    inlines = [CustomerContactsInline, CustomerRequisitesInline]


@admin.register(CustomerContacts)
class CustomerContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'contact_name', 'contact_type', 'contact_info')
    list_filter = ('contact_type',)
    search_fields = ('contact_name', 'contact_info', 'customer__customer_name')
    ordering = ['customer']


@admin.register(CustomerPassport)
class CustomerPassportAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'series', 'number', 'release_date', 'issued', 'unit_code')
    search_fields = ('series', 'number', 'customer__customer_name')
    ordering = ['customer']


@admin.register(CustomerRequisites)
class CustomerRequisitesAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'bank_name', 'bic', 'bank_account', 'customer_account_number')
    search_fields = ('bank_name', 'bic', 'customer__customer_name')
    ordering = ['customer']