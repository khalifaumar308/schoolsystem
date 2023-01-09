from django.contrib import admin
from .models import NewUser, OtherUser, TeacherAccount, ProfileLogin
from django.forms import TextInput, Textarea
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(NewUser)
class CustomUSer(UserAdmin):
    model = NewUser
    search_fields = ('username', 'email', 'first_name')
    ordering = ('username', )
    list_filter = ('email', )
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {
            "fields": (
                "email", "username", "first_name", "last_name", 'password'
                
            ),
        }),
        ("Permissions", {'fields': ("is_staff", "is_active")})
    )
    formfield_overrides = {
        NewUser.first_name: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields' : ('email', 'username', 'first_name', 'last_name', 'password1', 'password2','is_staff', 'is_active')
        }),
    )


@admin.register(OtherUser)
class OtherUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'first_name')
    list_filter = ('email', )
    list_display = ('email', 'first_name', 'last_name')


@admin.register(TeacherAccount)
class TeacherAccountAdmin(admin.ModelAdmin):
    # search_fields = ('email', 'first_name')
    # list_filter = ('other_user_value', )
    list_display = ('other_user_value',)

@admin.register(ProfileLogin)
class ProfileLoginAdmin(admin.ModelAdmin):
    pass
    # search_fields = ('email', 'first_name')
    # list_filter = ('username', 'email')
    # list_display = ('email', 'first_name', 'last_name', 'username')


# admin.site.register(NewUser, CustomUSer)