from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


from .models import User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'is_active',
     
    )
    list_filter = ('is_active', )


