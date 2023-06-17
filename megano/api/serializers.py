from rest_framework import serializers
from app_goods.models import Product, Tag, Review, Spec, Category, Image, Subcategory, Catalog, PopularProduct, \
    Sale, SaleItem, Banner, ProductLimited
from app_orders.models import Order, Payment
from app_orders.cart import Cart
from app_users.models import UserProfile, Avatar
from django.contrib.auth.models import User


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [f.name for f in Image._meta.fields]

    def get_src(self, obj):
        return obj.src.url


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = [f.name for f in Avatar._meta.fields]

    def get_src(self, obj):
        return obj.src.url


class SubcategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Subcategory
        fields = [f.name for f in Subcategory._meta.fields]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer()
    image = ImageSerializer()

    class Meta:
        model = Category
        fields = [f.name for f in Category._meta.fields]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [f.name for f in Tag._meta.fields]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [f.name for f in Review._meta.fields]


class SpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spec
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    specifications = SpecSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = UserProfile
        fields = ["fullName", "email", "phone", "avatar"]


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }


class PasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(max_length=200)
    newPassword = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return validated_data


class ShortProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count',
                  'date', 'title', 'description',
                  'freeDelivery', 'images', 'tags',
                  'rating', 'reviews']


class CatalogSerializer(serializers.ModelSerializer):
    items = ShortProductSerializer(many=True)

    class Meta:
        model = Catalog
        fields = ['items']


class PopularProductSerializer(serializers.ModelSerializer):
    products = ShortProductSerializer(many=True)

    class Meta:
        model = PopularProduct
        fields = ['products']


class OrderSerializer(serializers.ModelSerializer):
    products = ShortProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = SaleItem
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class ProductLimitedSerializer(serializers.ModelSerializer):
    products = ShortProductSerializer(many=True)

    class Meta:
        model = ProductLimited
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
