from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from app_users.models import UserProfile, Avatar
from app_orders.models import Order, Payment

from app_goods.models import Category, Product, Tag, Review, Catalog, PopularProduct, Sale, SaleItem, Banner, \
    ProductLimited

from api.serializers import UserProfileSerializer, SignInSerializer, SignUpSerializer, CategorySerializer, \
    AvatarSerializer, ProductSerializer, TagSerializer, ReviewSerializer, PasswordSerializer, CatalogSerializer, \
    ShortProductSerializer, PopularProductSerializer, OrderSerializer, SaleItemSerializer, SaleSerializer, \
    ProductLimitedSerializer, CartSerializer, PaymentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from app_orders.cart import Cart
from rest_framework import status
import datetime


class CartDetailView(APIView):
    """APIView для корзины, реализация методов get, post и delete"""

    def get_cart_items(self, cart):
        cart_items = []
        sale = None
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            try:
                sale = SaleItem.objects.get(product=product)
            except Exception as ex:
                assert ex
            cart_items.append(
                {
                    "id": product.id,
                    "category": product.category.id,
                    "price": Product.get_price(product, sale) if sale is not None else float(item["price"]),
                    "count": item["quantity"],
                    "date": product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)"),
                    "title": product.title,
                    "description": product.description,
                    "freeDelivery": product.freeDelivery,
                    "images": [
                        {"src": image.src.url, "alt": image.alt} for image in product.images.all()
                    ],
                    "tags": [
                        {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                    ],
                    "reviews": len(product.reviews.get_queryset()),
                    "rating": product.rating,
                }
            )
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)


@api_view(["GET", "POST"])
def orders(request):
    """APIView для заказа, реализация методов get, post"""
    if request.method == "GET":
        try:
            history_orders = Order.objects.filter(user=request.user)
        except Exception as ex:
            raise ex
        if history_orders is not None:
            serializer = OrderSerializer(history_orders, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    if request.method == "POST":
        order_obj = Order()
        order_obj.user = request.user
        order_obj.totalCost = Cart(request).get_total_price()
        prod_ids = [v["product_id"] for v in Cart(request).cart.values()]
        order_obj.save()
        for id in prod_ids:
            order_obj.products.add(Product.objects.get(id=int(id)))
        order_obj.save()
        data = {"orderId": order_obj.id}
        return JsonResponse(data, status=200)
    return HttpResponse(status=500)


@api_view(["GET", "POST"])
def order(request, id):
    """APIView для получения заказа по id, реализация методов get, post"""
    order_obj = None
    cart = Cart(request)
    try:
        order_obj = Order.objects.get(pk=id)
    except Exception as ex:
        assert ex
    if request.method == 'GET':
        if order_obj is not None:
            order_obj.totalCost = cart.get_total_price()
            order_obj.save()
            serializer = OrderSerializer(order_obj)
            return JsonResponse(serializer.data, status=200, safe=False)
    if request.method == "POST":
        data = request.data
        order_obj.fullName = data["fullName"]
        order_obj.email = data["email"]
        order_obj.phone = data["phone"]
        order_obj.deliveryType = data["deliveryType"]
        order_obj.paymentType = data["paymentType"]
        order_obj.city = data["city"]
        order_obj.address = data["address"]
        order_obj.status = data["status"]
        order_obj.totalCost = cart.get_total_price()
        order_obj.save()
        data = {"orderId": order_obj.id}
        return JsonResponse(data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["POST"])
def payment(request, id):
    """APIView для оплаты, реализация методов get, post"""
    if request.method == "GET":
        try:
            payment = Payment.objects.get(id=id)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PaymentSerializer(payment)
        return JsonResponse(serializer.data, status=200, safe=False)
    if request.method == "POST":
        payment_obj = Payment()
        payment_obj.name = request.data["name"]
        payment_obj.number = request.data["number"]
        payment_obj.year = request.data["year"]
        payment_obj.month = request.data["month"]
        payment_obj.code = request.data["code"]
        payment_obj.save()
        return HttpResponse(200)


@api_view(["GET"])
def banners(request):
    """APIView для получения банеров, реализация методов get"""
    if request.method == "GET":
        banner = Banner.objects.first().products.get_queryset()
        if banner:
            serializer = ShortProductSerializer(banner, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    return HttpResponse(status=500, safe=False)


@api_view(["GET"])
def sales(request):
    """APIView для получения скидок, реализация метода get"""
    if request.method == "GET":
        sales_data = Sale.objects.all().first()
        sale_product = sales_data.items.all()
        serializer = SaleSerializer(sales_data)
        if sale_product:
            for index, obj in enumerate(sale_product):
                dateFrom = datetime.datetime.strptime(str(obj.dateFrom), '%Y-%m-%d').strftime("%m-%d")
                dateTo = datetime.datetime.strptime(str(obj.dateTo), '%Y-%m-%d').strftime("%m-%d")
                obj.price = obj.product.price
                obj.save()
                serializer.data["items"][index]["dateFrom"] = dateFrom
                serializer.data["items"][index]["dateTo"] = dateTo
            return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


@api_view(["POST"])
def profile_avatar(request):
    """APIView для загрузки аватарки, реализация метода post"""
    if request.method == "POST":
        avatar = request.FILES["avatar"]
        avatar_obj = Avatar(src=avatar)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.avatar = avatar_obj
        avatar_obj.save()
        user_profile.save()
        serializer = AvatarSerializer(avatar_obj)
        return JsonResponse(serializer.data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["GET"])
def categories(request):
    """APIView для получения категорий, реализация метода get"""
    if request.method == "GET":
        categories_data = Category.objects.all()
        if categories_data:
            serializer = CategorySerializer(categories_data, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


@api_view(["GET"])
def catalog(request):
    """APIView для получения каталога, реализация методов get"""
    if request.method == "GET":
        catalog_data = Catalog.objects.all()
        if catalog_data:
            serializer = CatalogSerializer(catalog_data, many=True)
            for el in serializer.data:
                for i in el["items"]:
                    i["reviews"] = len(i["reviews"])
            return JsonResponse(*serializer.data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["GET"])
def productsPopular(request):
    """APIView для получения популярных товаров, реализация метода get"""
    if request.method == "GET":
        popular = PopularProduct.objects.first().products.get_queryset()
        if popular:
            serializer = ShortProductSerializer(popular, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(['GET'])
def productsLimited(request):
    """APIView для получения лимитированных товаров, реализация метода get"""
    if request.method == "GET":
        products = ProductLimited.objects.first().products.get_queryset()
        if products:
            serializer = ShortProductSerializer(products, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["POST"])
def signIn(request):
    """APIView для авторизации, реализация метода post"""
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        serializer = SignInSerializer(data=body)
        if user is not None:
            login(request, user)
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


@api_view(["POST"])
def signUp(request):
    """APIView для регистрации, реализация метода post"""
    if request.method == "POST":
        data = list(request.data.keys())[0]
        data = json.loads(data)
        username = data.get("username")
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # User
            user = User.objects.get(username=username)
            # Userprofile
            user_profile = UserProfile(user=user)
            user_profile.save()
            login(request, user)
            return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


def signOut(request):
    logout(request)
    return HttpResponse(status=200)


@api_view(["GET"])
def product(request, id):
    """APIView для товара по id, реализация метода get"""
    if request.method == "GET":
        prod = None
        try:
            prod = Product.objects.get(id=id)
        except Exception as ex:
            assert ex
        if prod is not None:
            if len(prod.reviews.get_queryset()) > 0:
                rating = sum([int(x.rate) for x in prod.reviews.get_queryset()]) / len(prod.reviews.get_queryset())
                prod.rating = round(rating, 1)
                prod.save()
            else:
                prod.rating = 0
            prod.save()
            serializer = ProductSerializer(prod)
            return JsonResponse(serializer.data, status=200, safe=False)
        return Response(status=500)


@api_view(["GET"])
def tags(request):
    """APIView для получения тегов, реализация метода get"""
    if request.method == "GET":
        tgs = Tag.objects.all()
        if tgs:
            serializer = TagSerializer(tgs, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["GET"])
def productReviews(request, id):
    """APIView для получения отзывов, реализация метода get"""
    if request.method == "GET":
        review = Review.objects.filter(product_id=id)
        if review:
            serializer = ReviewSerializer(review, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(['GET', 'POST'])
def profile(request):
    """APIView для получения профиля, реализация методов get, post"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user_id=request.user)
            serializer = UserProfileSerializer(user_profile)
            return JsonResponse(serializer.data, status=200, safe=False)
    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.fullName = request.data["fullName"]
            user_profile.phone = request.data["phone"]
            user_profile.email = request.data["email"]
            user_profile.save()
            serializer.save()
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            print(serializer.errors)
        return HttpResponse(status=400)

    return HttpResponse(status=500)


@api_view(["POST"])
def profilePassword(request):
    """APIView для изменения пароля, реализация методов post"""
    if request.method == "POST":
        data = request.data
        old_password = data["currentPassword"]
        new_password = data["newPassword"]
        user = request.user
        if old_password != new_password:
            serializer = PasswordSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user.set_password(new_password)
                user.save()
                return JsonResponse(serializer.data, status=200, safe=False)
            return HttpResponse(status=500)
