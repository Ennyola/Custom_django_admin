from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.core.mail import send_mail
# Register your models here.

admin.site.site_header = "Django User Administration"

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_joined', 'email', 'change_active_status', 'is_active', 'change_staff_status', 'is_staff']
    list_display_links = ['username', 'email']
    list_filter = ['date_joined']
    search_fields = ['username', 'email']
    change_list_template = "admin/admin_app/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('is_active/<user>', self.change_active),
            path ('send_mails/', self.send_mails ),
            path('is_staff/<user>', self.is_staff_status)
        ]
        return custom_urls + urls

    # Views for the change_active status functionality
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

    # Views for the change_staff_status functionality
    def is_staff_status(self, request, user):
        user = User.objects.get(username = user)
        if user.is_staff:
            user.is_staff  = False
            user.save()
            self.message_user(request, 'User now has staff status')
        else:
            user.is_staff = True
            user.save()
            self.message_user(request, 'User no longer has staff status')
        return redirect('../')

    # Views handling the sending of mails
    def send_mails(self, request):
        subject = request.POST.get("mail-subject", None)
        message = request.POST.get("mail-body", None)
        from_email = request.user.email
        users = User.objects.all()
        recipient_list = [user.email for user in users]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        self.message_user(request, "Mails Sent successfully")
        return redirect('../')     

    def change_active_status(self, obj):
        return format_html(
            f'<a class = "button" href ="is_active/{obj.username}"> Change Active status</a>'
        )

    def change_staff_status(self, obj):
        return format_html(
            f'<a class = "button" href ="is_staff/{obj.username}"> Change Staff status </a>'
        )
   

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)