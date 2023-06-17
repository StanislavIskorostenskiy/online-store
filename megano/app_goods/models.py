from django.db import models
from app_users.models import UserProfile


class Image(models.Model):
    src = models.ImageField(
        upload_to="app_goods/images/product_avatars/",
        default="app_goods/images/default.png",
        verbose_name="Ссылка картинки",
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")

    def __str__(self):
        return self.src.url


class Tag(models.Model):
    name = models.CharField("Name", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Spec(models.Model):
    name = models.CharField("Name", max_length=100, null=True, blank=True)
    value = models.CharField("Value", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    title = models.CharField("Title", max_length=200)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, related_name="subcategory_image", verbose_name="Фото",
                              null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, related_name="category_image", verbose_name="Фото",
                              null=True)
    subcategories = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    RATE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    text = models.TextField("Text", max_length=1000)
    date = models.DateField("Date", auto_now=True)
    rate = models.CharField("Rate", max_length=100, choices=RATE)
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    email = models.EmailField(default="anonim@mail.ru")


class Product(models.Model):
    title = models.CharField("Title", max_length=100, null=True, blank=True)
    price = models.FloatField(default=1.0)
    description = models.TextField("Description", max_length=10000)
    fullDescription = models.TextField("Full description", max_length=10000)
    tags = models.ManyToManyField(Tag, related_name="tag")
    specifications = models.ManyToManyField(Spec, related_name="specifications")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    count = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    freeDelivery = models.BooleanField(default=True)
    rating = models.FloatField(default=1, blank=True)
    images = models.ManyToManyField(Image, related_name="activePhoto", verbose_name="Фото")
    reviews = models.ManyToManyField(Review, related_name="product_reviews")

    def __str__(self):
        return self.title

    def get_price(self, sale_obj):
        if sale_obj.product is not None:
            return sale_obj.salePrice
        return self.price


class PopularProduct(models.Model):
    products = models.ManyToManyField(Product, related_name="popular")


class Catalog(models.Model):
    title = models.CharField("Title", max_length=200, null=True)
    items = models.ManyToManyField(Product, related_name="items")
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, related_name="catalog_image", verbose_name="Фото",
                              null=True)


class SaleItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="sale_products")
    price = models.IntegerField(default=1.0)
    salePrice = models.IntegerField(default=1.0)
    dateFrom = models.DateField(default=None)
    dateTo = models.DateField(default=None)
    title = models.CharField("Title", max_length=100, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name="sale_images")


class Sale(models.Model):
    items = models.ManyToManyField(SaleItem, related_name="items")


class Banner(models.Model):
    products = models.ManyToManyField(Product, related_name="banners_products")
    images = models.ManyToManyField(Image, related_name="banner_image", verbose_name="Фото")


class ProductLimited(models.Model):
    products = models.ManyToManyField(Product, related_name="limitedProducts")
