from django.contrib import admin

from core.loading import get_model

AttributeOption = get_model('products', 'AttributeOption')
AttributeOptionGroup = get_model('products', 'AttributeOptionGroup')
Product = get_model('products', 'Product')
ProductAttribute = get_model('products', 'ProductAttribute')
ProductAttributeValue = get_model('products', 'ProductAttributeValue')
ProductClass = get_model('products', 'ProductClass')


class AttributeInline(admin.TabularInline):
    model = ProductAttributeValue


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2


class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_digital', 'track_stock')
    inlines = [ProductAttributeInline]

class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('get_title', 'upc', 'get_product_class',
                    'attribute_summary', 'created')
    # list_filter = ['structure', 'is_discountable']
    inlines = [AttributeInline, ]
    #prepopulated_fields = {"slug": ("name",)}
    search_fields = ['upc', 'name']

    def get_queryset(self, request):
        qs = super(ProductAdmin, self).queryset(request)
        return (
            qs
            .select_related('product_class')
            .prefetch_related(
                'attribute_values',
                'attribute_values__attribute'))


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'product_class', 'type')
    prepopulated_fields = {"code": ("name", )}


class OptionAdmin(admin.ModelAdmin):
    pass


class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption


class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline, ]


admin.site.register(ProductClass, ProductClassAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(AttributeOptionGroup, AttributeOptionGroupAdmin)
