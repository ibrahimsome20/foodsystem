from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from .serializers import CatogerySerializer,CartItemSerializer,FoodSerializer

# user=Usern.objects.()

# cattegory=Catogery.objects.all()


@csrf_exempt
def admin_login_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if username == "admin" and password == "1234":
                return JsonResponse({
                    "success": True,
                    "message": "Login successful",
                    
                
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid credentials",
                    
                }, status=401)

        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "error": "Method not allowed"
    }, status=405)


@api_view(['GET'])
def get_food(request):
    foodget=Food.objects.all()
    spilizer=Food_get(foodget,many=True)
    return Response(spilizer.data)

@api_view(['DELETE'])
def delete_food(request,id):
    try:
        food=Food.objects.get(id=id)
        if food :
            food.delete()
            return Response({"message":'item deleted succefully',},status=200)
        else :
            return Response({"message":'error happen !'})
    except  Food.DoesNotExist:
        return Response({'messages':'items does not exist'})  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Catogery


@api_view(['GET'])
def get_categories(request):
    categories = Catogery.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Category added"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def edit_category(request, id):
    category = Catogery.objects.get(id=id)
    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Category updated"})
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_category(request, id):
    Catogery.objects.get(id=id).delete()
    return Response({"message": "Category deleted"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# -------- Category --------
@api_view(['GET','POST'])
def category_list(request):
    if request.method == 'GET':
        return Response(CatogerySerializer(Catogery.objects.all(), many=True).data)

    serializer = CatogerySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# -------- Food --------
@api_view(['GET','POST'])
def food_list(request):
    if request.method == 'GET':
        return Response(FoodSerializer(Food.objects.all(), many=True).data)

    serializer = FoodSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_food(request, id):
    Food.objects.get(id=id).delete()
    return Response({'message': 'Deleted'})


# -------- Cart --------
@api_view(['POST'])
def add_to_cart(request):
    session_id = request.data['session_id']
    food_id = request.data['food']
    quantity = request.data.get('quantity',1)

    cart, _ = Cart.objects.get_or_create(session_id=session_id)
    CartItem.objects.create(cart=cart, food_id=food_id, quantity=quantity)

    return Response({'message': 'Added to cart'})


@api_view(['GET'])
def cart_items(request, session_id):
    cart = Cart.objects.get(session_id=session_id)
    items = CartItem.objects.filter(cart=cart)
    return Response(CartItemSerializer(items, many=True).data)


# -------- Order --------
@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

import stripe
stripe.api_key = "sk_test_xxx"

@api_view(['POST'])
def create_payment(request):
    intent = stripe.PaymentIntent.create(
        amount=int(request.data['amount'] * 100),
        currency='usd',
    )
    return Response({'client_secret': intent.client_secret})


# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Username
from .serializers import UsernameSerializer

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("user_name")
        last_name = data.get("last_name")
        email = data.get("email_user")
        phone = data.get("phone_user")
        password = data.get("password_user")

        if Username.objects.filter(email_user=email).exists():
            return JsonResponse({"success": False, "message": "Email already exists"}, status=400)
        if Username.objects.filter(phone_user=phone).exists():
            return JsonResponse({"success": False, "message": "Phone already exists"}, status=400)

        user = Username.objects.create(
            user_name=username,
            last_name=last_name,
            email_user=email,
            phone_user=phone,
            password_user=password  # لاحقًا يمكن تشفيرها
        )
        return JsonResponse({"success": True, "message": "User registered successfully"})
    
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email_or_phone = data.get("email_or_phone")
        password = data.get("password_user")

        try:
            user = Username.objects.get(
                (models.Q(email_user=email_or_phone) | models.Q(phone_user=email_or_phone))
            )
            if user.password_user == password:
                return JsonResponse({"success": True, "message": "Login successful", "user_id": user.id})
            else:
                return JsonResponse({"success": False, "message": "Invalid password"}, status=401)
        except Username.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found"}, status=404)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)


@api_view(['GET'])
def get_users(request):
    users = Username.objects.all()
    serializer = UsernameSerializer(users, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_user_orders(request):
    user_id = request.GET.get('user')
    if not user_id:
        return Response({"error": "User ID required"}, status=400)
    orders = Order.objects.filter(user_name_id=user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)