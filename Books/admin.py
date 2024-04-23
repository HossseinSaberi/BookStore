from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings
from .models import Book, Publisher, Category, BookCategory, BookPublisher


class BookPublisherInline(admin.StackedInline):
    model = BookPublisher
    extra = 0
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('publisher','translator'),)
        }
        ),
        (None, {
            'classes': ('wide',),
            'fields': (('isbn', 'edition_series'), ('price', 'publisher_data'), ('main_image',))
        }
        ),
        (None,
         {
             'classes': ('wide',),
             'fields': (("cover_type", "size_type", 'page_no'),)
         }))
    # readonly_fields = ('book__author',)


class BookCategoryInline(admin.StackedInline):
    model = BookCategory
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("book_name_fa", 'book_name_en', 'author', 'writen_date')
    list_filter = ("author__author_name_fa",'publisher__publisher_name')
    search_fields = ('book_name_en__istartswith', 'author__author_name_fa__istartswith')
    fieldsets = (
        ('Main Detail', {
            'classes': ('wide',),
            'fields': (('book_name_en', 'book_name_fa',
                        'book_slug', 'author'), ('short_description', 'writen_date'))}),
    )
    prepopulated_fields = {"book_slug": ('book_name_en',)}
    inlines = [BookPublisherInline,BookCategoryInline]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('publisher_name',)
    list_filter = ('publisher_name',)
    search_fields = ("id", 'publisher_name__startwith')
    fieldsets = (('Publish Detail', {
        'fields': (('publisher_name', 'publisher_slug'), ('avatar',))
    }
    ),)
    prepopulated_fields = {"publisher_slug": ('publisher_name',)}
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','is_prize')
    list_filter = ('is_prize','title',)
    search_fields = ("id", 'title__startwith')
    fieldsets = (('Category Detail', {
        'fields': (('title', 'category_slug'), ('bio',), ('is_prize', 'logo'))
    }
    ),)
    prepopulated_fields = {"category_slug": ('title',)}



