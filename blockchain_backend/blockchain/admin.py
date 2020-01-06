from django.contrib import admin

from .models import APILog, Account

class APILogAdmin(admin.ModelAdmin):
    list_filter = ["method"]

    list_display = ["method", "timestamp", "args", "result"]


class AccountAdmin(admin.ModelAdmin):
    list_search = ["pubkey"]

    list_display = ["pubkey", "label", "balance_nanoabend", "balance_nanoaeter"]


admin.site.register(APILog, APILogAdmin)
admin.site.register(Account, AccountAdmin)
