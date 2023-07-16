
from django.contrib import admin

from .models import *
# Register your models here.
from django.utils.html import format_html

from django.db import models
import uuid
from bankingsystem.admin_actions import export_as_csv

class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'credit_facility', 'payment_tenure', 'amount', 'requested_at']
    list_filter = ['credit_facility', 'payment_tenure', 'requested_at']
    search_fields = ['user__email', 'amount', 'reason']
    readonly_fields = ['user', 'requested_at']
    
    fieldsets = (
        ('Loan Details', {
            'fields': ('user', 'credit_facility', 'payment_tenure', 'amount', 'reason')
        }),
        ('Additional Information', {
            'fields': ('requested_at',)
        })
    )

admin.site.register(LoanRequest, LoanRequestAdmin)

class CheckDepositAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount']
    list_filter = ['user']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id']
    fieldsets = [
        ('Check Information', {'fields': ['id', 'user', 'amount']}),
        ('Check Images', {'fields': ['front_image', 'back_image']}),
    ]
    ordering = ['-id']

admin.site.register(CHECK_DEPOSIT, CheckDepositAdmin)

class PayBillsAdmin(admin.ModelAdmin):
    list_display = ['user', 'address1', 'city', 'state', 'zipcode', 'nickname', 'delivery_method', 'amount', 'get_date', 'status']
    list_filter = ['delivery_method', 'status']
    search_fields = ['user__username', 'address1', 'city', 'state', 'zipcode', 'nickname']
    ordering = ['-timestamp']
    actions = ['mark_as_paid', 'mark_as_cancelled']

    def get_date(self, obj):
        return f"{obj.year}-{obj.month:02d}-{obj.day:02d}"

    get_date.short_description = 'Date of Delivery'

    def mark_as_paid(self, request, queryset):
        rows_updated = queryset.update(status='completed')
        if rows_updated == 1:
            message_bit = "1 record was"
        else:
            message_bit = f"{rows_updated} records were"
        self.message_user(request, f"{message_bit} successfully marked as paid.")

    mark_as_paid.short_description = "Mark selected bills as paid"

    def mark_as_cancelled(self, request, queryset):
        rows_updated = queryset.update(status='cancelled')
        if rows_updated == 1:
            message_bit = "1 record was"
        else:
            message_bit = f"{rows_updated} records were"
        self.message_user(request, f"{message_bit} successfully marked as cancelled.")

    mark_as_cancelled.short_description = "Mark selected bills as cancelled"

admin.site.register(PayBills, PayBillsAdmin)

admin.site.register(CardDetail)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'amount', 'recipient_account', 'date', 'status', 'current_balance')
    list_filter = ('status', )
    search_fields = ('user__email', 'user__username')
    
    def client_name(self, obj):
        return obj.user.get_full_name()
    client_name.short_description = 'Client Name'
    
    def client_email(self, obj):
        return obj.user.email
    client_email.short_description = 'Client Email'
    
    def recipient_account(self, obj):
        return obj.target
    recipient_account.short_description = 'Recipient Account'
    
    def current_balance(self, obj):
        deposits = obj.user.deposits.aggregate(models.Sum('amount'))['amount__sum'] or 0
        withdrawals = obj.user.withdrawals.aggregate(models.Sum('amount'))['amount__sum'] or 0
        balance = deposits - withdrawals
        return balance
    current_balance.short_description = 'Current Balance'
    
admin.site.register(Withdrawal, WithdrawalAdmin)


class Withdrawal_internationaAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'amount', 'recipient_account', 'date', 'status', 'current_balance')
    list_filter = ('status', )
    search_fields = ('user__email', 'user__username')
    
    def client_name(self, obj):
        return obj.user.get_full_name()
    client_name.short_description = 'Client Name'
    
    def client_email(self, obj):
        return obj.user.email
    client_email.short_description = 'Client Email'
    
    def recipient_account(self, obj):
        return obj.target
    recipient_account.short_description = 'Recipient Account'
    
    def current_balance(self, obj):
        deposits = obj.user.deposits.aggregate(models.Sum('amount'))['amount__sum'] or 0
        withdrawals = obj.user.withdrawals.aggregate(models.Sum('amount'))['amount__sum'] or 0
        balance = deposits - withdrawals
        return balance
    current_balance.short_description = 'Current Balance'
    
admin.site.register(Withdrawal_internationa, Withdrawal_internationaAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'date']
    list_filter = ['status', 'date']

    def save_model(self, request, obj, form, change):
        if change:
            original_obj = Payment.objects.get(pk=obj.pk)
            if original_obj.status != 'COMPLETE' and obj.status == 'COMPLETE':
                obj.update_balance()
            elif original_obj.status == 'COMPLETE' and obj.status != 'COMPLETE':
                obj.user.balance -= original_obj.amount
                obj.user.save()
        elif obj.status == 'COMPLETE':
            obj.update_balance()

        super().save_model(request, obj, form, change)


class CryptoWITHDRAWAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_method', 'amount', 'status', 'date')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'user__email')

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data and form.cleaned_data['status'] == 'COMPLETE':
            obj.update_balance()
        obj.save()

admin.site.register(CryptoWITHDRAW, CryptoWITHDRAWAdmin)

admin.site.register(Payment, PaymentAdmin)
admin.site.add_action(export_as_csv, name='export_selected')
