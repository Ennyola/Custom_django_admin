from django.contrib import admin
from django.contrib.auth.models import User, Group
# Register your models here.

admin.site.site_header = "Django User Administration"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'email']
    list_filter = ['date_joined']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)