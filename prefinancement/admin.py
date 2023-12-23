from django.contrib import admin
from prefinancement.models import Account, ClientContruction, ClientTerrain
from userauths.models import User
from import_export.admin import ImportExportModelAdmin

class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ["account_status", "account_status"]
    list_display = ["user", "account_number", "account_status",]
    list_filter = ["account_status"]
    
class ClientTerrainAdmin(ImportExportModelAdmin):
    search_fields = ["full_name"]
    list_display = ["user", "full_name"]
    
class ClientConstructionAdmin(ImportExportModelAdmin):
    search_fields = ["full_name"]
    list_display = ["user", "full_name"]
    
    
admin.site.register(Account, AccountAdminModel)
admin.site.register(ClientTerrain, ClientTerrainAdmin)
admin.site.register(ClientContruction, ClientConstructionAdmin)