from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Tag, Brand, Product
)

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.image_a.url))

    thumbnail.short_description = 'photo'

    list_display = ('thumbnail', 'name',
                    'category', 'price', 'rating', 'brand')
    list_display_links = ('name', 'thumbnail')
    search_fields = ['name', 'description', 'brand', 'category']
    
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_display_links = ('name', 'category')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Brand)
