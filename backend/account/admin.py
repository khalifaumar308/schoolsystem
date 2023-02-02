from django.contrib import admin
from .models import SchoolUser, Profile, ProfileLogin, Class, Attendance
from django.forms import TextInput, Textarea
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(SchoolUser)
class AddUserAdmin(admin.ModelAdmin):
    search_fields = ( 'first_name', )
    # list_filter = ('email', )
    list_display = ( 'first_name', 'last_name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # search_fields = ( 'first_name', )
    # list_filter = ('email', )
    list_display = ( 'user', 'attendance')


admin.site.register([ProfileLogin, Profile, Class])
# admin.site.register
