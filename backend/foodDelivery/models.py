from django.db import models
from django.utils import timezone


# Create your models here.

class Username(models.Model):
    user_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email_user=models.EmailField(max_length=200,unique=True)
    phone_user=models.CharField(max_length=11,unique=True)
    password_user=models.CharField(max_length=200)
    register=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f' {self.user_name} {self.last_name}'
    

class Catogery(models.Model):
    name = models.CharField(max_length=100 )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Food(models.Model):
    catogry=models.ForeignKey(Catogery,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=200)
    item_price=models.DecimalField(max_digits=10,decimal_places=2)
    item_description=models.CharField(max_length=200,null=True,blank=True)
    item_image=models.ImageField(upload_to='food-images/')
    item_qauntity=models.CharField(max_length=20)
    is_available=models.BooleanField(default=True)
    item_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.catogry} {self.item_name} {self.item_price}'    
class Cart(models.Model):
    session_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled'),
    )

    user_name = models.ForeignKey(Username,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)






