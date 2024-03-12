from django.contrib import admin
from .models import CorporateSubscription, UserSubscription

@admin.register(CorporateSubscription)
class CorporateSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'type', 'year', 'amount', 'phone', 'email')
    search_fields = ('org_name', 'phone', 'email')
    list_filter = ('type', 'year')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('contact', 'type', 'year', 'amount', 'phone', 'email')
    search_fields = ('contact', 'phone', 'email')
    list_filter = ('type', 'year')
