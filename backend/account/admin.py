from django.contrib import admin
from .models import SchoolUser, Profile, ProfileLogin, Class
from django.forms import TextInput, Textarea
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(SchoolUser)
class AddUserAdmin(admin.ModelAdmin):
    search_fields = ( 'first_name', )
    # list_filter = ('email', )
    list_display = ( 'first_name', 'last_name')

admin.site.register([ProfileLogin, Profile, Class])
# admin.site.register
