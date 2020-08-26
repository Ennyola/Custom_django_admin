from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
# Register your models here.

admin.site.site_header = "Django User Administration"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'email', 'set_active_buttons', 'is_active']
    list_display_links = ['username', 'email']
    list_filter = ['date_joined']
    search_fields = ['username', 'email']


    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path('is_active/<user>', self.change_active)
        ]
        return custom_urls + urls

    def change_active(self, request, user):
        print(user)

        user = User.objects.get(username = user)
        if user.is_active:
            user.is_active = False
            user.save()
            self.message_user(request, 'User is now inactive')
        else:
            user.is_active = True
            user.save()
            self.message_user(request, 'User is now active')
        return redirect('../')

        

    def set_active_buttons(self, obj):
        return format_html(
            f'<a class = "button" href ="is_active/{obj.username}"> Change Active </a>'
        )
   

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)