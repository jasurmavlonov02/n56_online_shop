from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from shop.models import Product, Category, Order, Comment
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from import_export import resources


# Register your models here.


@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'image_tag', 'my_order')
    search_fields = ('name', 'price')
    list_filter = ['category', 'quantity', 'rating']
    autocomplete_fields = ['category']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'product', 'is_negative')
    readonly_fields = ['is_negative']


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'product_count')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        ProductInline,
    ]

    def product_count(self, category):
        return category.products.count()


admin.site.site_header = "Apelsin Admin"
admin.site.site_title = "Apelsin Admin"
admin.site.index_title = "Welcome to Apelsin Researcher Portal"
