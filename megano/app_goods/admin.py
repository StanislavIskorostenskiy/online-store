from django.contrib import admin
from app_goods.models import Product, Tag, Review, Spec, Category, Image, Subcategory, Catalog, PopularProduct, \
    SaleItem, Sale, Banner, ProductLimited


class ProductLimitedAdmin(admin.ModelAdmin):
    filter_horizontal = ["products"]
    list_display = [f.name for f in ProductLimited._meta.fields]


admin.site.register(ProductLimited, ProductLimitedAdmin)


class BannerAdmin(admin.ModelAdmin):
    filter_horizontal = ["products"]
    list_display = [f.name for f in Banner._meta.fields]


admin.site.register(Banner, BannerAdmin)


class SalesAdmin(admin.ModelAdmin):
    filter_horizontal = ["items"]
    list_display = [f.name for f in Sale._meta.fields]


admin.site.register(Sale, SalesAdmin)


class SaleItemAdmin(admin.ModelAdmin):
    filter_horizontal = ["images"]
    list_display = [f.name for f in SaleItem._meta.fields]


admin.site.register(SaleItem, SaleItemAdmin)


class CatalogAdmin(admin.ModelAdmin):
    filter_horizontal = ["items"]
    list_display = [f.name for f in Catalog._meta.fields]


admin.site.register(Catalog, CatalogAdmin)


class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ["tags", "specifications", "images", "reviews"]
    list_display = [f.name for f in Product._meta.fields]


admin.site.register(Product, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Tag._meta.fields]


admin.site.register(Tag, TagAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Review._meta.fields]


admin.site.register(Review, ReviewAdmin)


class SpecAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Spec._meta.fields]


admin.site.register(Spec, SpecAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]


admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Subcategory._meta.fields]


admin.site.register(Subcategory, SubcategoryAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Image._meta.fields]


admin.site.register(Image, ImageAdmin)


class PopularProductAdmin(admin.ModelAdmin):
    filter_horizontal = ["products"]
    list_display = [f.name for f in PopularProduct._meta.fields]


admin.site.register(PopularProduct, PopularProductAdmin)
