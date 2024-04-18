from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserLastActivity, Address, Profile , Author, Translator

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

    # def display_avatar(self, obj):
    #     # Assuming 'avatar' is a field in your Profile model
    #     if obj.avatar:
    #         return f'<img src="{obj.avatar}" style="max-width: 50px; max-height: 50px;" />'
    #     else:
    #         return 'No Avatar'
    #
    # # Allow HTML rendering in the list display
    # display_avatar.allow_tags = True
    # display_avatar.short_description = 'Avatar'

admin.site.site_header = 'BookStore Management'
admin.site.site_title = 'BookStore Management'
admin.site.index_title = 'Welcome To Admin Panel'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Author)
admin.site.register(Translator)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserLastActivity)
admin.site.register(Address)