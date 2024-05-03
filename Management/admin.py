from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserLastActivity, Address, Profile

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_account_enable')
    list_filter = ('username', 'email', 'is_staff', 'is_active', 'is_account_enable')
    fieldsets = (
        (None, {'fields': (('username', 'email'), 'password')}),
        ('Permissions',
         {
             'fields': (("is_staff", "is_active", "is_superuser", 'is_account_enable'), "groups", "user_permissions")
         }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('username', 'email'), ("password1", "password2"), ("is_account_enable","is_active", "is_staff", "is_superuser"), "groups",
                "user_permissions"
            )}
        ),
    )
    search_fields = ('username__istartswith', 'email__istartswith')


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0  # Number of empty forms to display for adding new addresses
    fieldsets = (
        (None, {'fields': (('name', 'zip_code'), 'address_detail',)}),
    )


class ProfileAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Profile
    inlines = [AddressInline]
    list_display = ('firstname', 'lastname', 'age', 'avatar', 'bio', 'user')
    list_filter = ('firstname', 'lastname', 'age', 'avatar', 'bio', 'user')
    fieldsets = (
        (None, {'fields': (('user', 'age'),('firstname', 'lastname'),)}),
        ('Details',
         {
             'fields': ('avatar', 'bio')
         }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('user', 'firstname'), ('lastname', 'age'),
                ('avatar', "bio")
            )}
         ),
    )
    search_fields = ('firstname__istartswith', 'lastname__istartswith')
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserLastActivity)