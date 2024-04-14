from django.contrib import admin
from apps.accounts.models import Person

# Register your models here.



class PersonAdmin(admin.ModelAdmin):
    list_display = ['get_username','get_email','wanna_be_a_blogger','phone_number','user_company']
    search_fields = ['user__username','user__email','phone_number','user_company']
    list_filter = ['wanna_be_a_blogger','user_company']


    def get_username(self,obj):
        return obj.user.username
    
    def get_email(self,obj):
        return obj.user.email
    
    get_username.short_description = 'Username'
    get_email.short_description = 'Email'

admin.site.register(Person,PersonAdmin)