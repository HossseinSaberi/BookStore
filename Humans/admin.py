from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Author, Translator

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
