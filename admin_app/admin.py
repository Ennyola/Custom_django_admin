from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.core.mail import send_mail
# Register your models here.

admin.site.site_header = "Django User Administration"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'email', 'set_active_buttons', 'is_active']
    list_display_links = ['username', 'email']
    list_filter = ['date_joined']
    # search_fields = ['username', 'email']
    change_list_template = "admin/admin_app/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('is_active/<user>', self.change_active),
            path ('send_mails/', self.send_mails )
        ]
        return custom_urls + urls

    def change_active(self, request, user):
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

    def send_mails(self, request):
        subject = request.POST.get("mail-subject", None)
        message = request.POST.get("mail-body", None)
        users = User.objects.all()
        mails = [user.email for user in users]
        send_mail(subject, message, 'medunoyeeni@gmail.com', mails, fail_silently=True)
        


        self.message_user(request, "Mails Sent successfully")
        return redirect('../')     

    def set_active_buttons(self, obj):
        return format_html(
            f'<a class = "button" href ="is_active/{obj.username}"> Change Active </a>'
        )
   

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)