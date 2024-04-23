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

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','author_name_en', 'author_name_fa')
    list_filter = ('author_name_fa',)
    search_fields = ('author_name_fa__startwith','author_name_en__startwith')
    fieldsets = (('Publish Detail', {
        'fields': (('author_name_en','author_name_fa','author_slug'),('bio',), ('avatar',))
    }
    ),)
    prepopulated_fields = {"author_name_en": ('author_slug',)}
    
    
@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('id','translator_name_en','translator_name_fa')
    list_filter = ('translator_name_fa',)
    search_fields = ('translator_name_en__startwith','translator_name_en__startwith')
    fieldsets = (('Translator Detail', {
        'fields': (('translator_name_en','translator_name_fa','translator_slug'),('bio',), ('avatar',))
    }
    ),)
    prepopulated_fields = {"translator_name_en": ('translator_slug',)}
    

admin.site.site_header = 'BookStore Management'
admin.site.site_title = 'BookStore Management'
admin.site.index_title = 'Welcome To Admin Panel'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserLastActivity)
admin.site.register(Address)