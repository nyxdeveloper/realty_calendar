from django.contrib import admin

from .models import Rent
from .models import Flat


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('user', 'flat', 'start', 'end', 'total_cost', 'tenant')
    search_fields = ['tenant__name', 'tenant__phone', 'comment', 'tenant__email', 'flat__short_name', 'flat__address']


admin.site.register(Flat)
