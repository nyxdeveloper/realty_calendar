from django.contrib import admin

from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'blacklist', 'comment')
    list_filter = ['blacklist']
    search_fields = ['name', 'phone', 'comment', 'email']
