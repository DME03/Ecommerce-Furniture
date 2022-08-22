from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
  

# Create your models here.

# ---------------- FURNITURE WEBPAGE ---------------------------
class Category(models.Model):

    name= models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# ---------------- FURNITURE ITEMS ---------------------------
        
class FurnitureItem(models.Model):
  
    title = models.CharField(max_length=200)
    furniture_image= models.ImageField(upload_to='images')
    price= models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items') 

    def __str__(self):
        return self.title

# ----------------MY CART------------------------------
class MyCart(models.Model):
    item_selected= models.ForeignKey(FurnitureItem, on_delete=models.CASCADE)
    cart_user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity= models.IntegerField(null=True, default=1)
    quantity_price= models.IntegerField(null=True)

# ----------------BUYER REGISTRATION MODEL--------------------

# Valitdation Error Function
def validate_city(value):
    if value == 'S':
        raise ValidationError("City is mandatory to fill.")
    else:
        return value

class BuyerProfile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number= models.IntegerField()

    interest= models.CharField(max_length=200, null=True)

    city = models.CharField(
    max_length = 20,
    choices= [('S','Select'),('M','Mumbai'),('K','Kolkata'),('B','Bengaluru'),('G','Gujarat')],
    default='Select',
    validators=[validate_city]
)   

    def __str__(self): 
        return self.user.username
# ----------------------------------------------------


# ----------------SELLER REGISTRATION MODEL--------------------

# Valitdation Error Function
def validate_city_seller(value):
    if value == 'S':
        raise ValidationError("City is mandatory to fill.")
    else:
        return value

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number= models.IntegerField()

    selling_item = models.CharField(max_length=70)

    fulfilled_by = models.CharField(max_length=20)

    city = models.CharField(
    max_length = 20,
    choices= [('S','Select'),('M','Mumbai'),('K','Kolkata'),('B','Bengaluru'),('G','Gujarat')],
    default='Select',
    validators=[validate_city_seller]
)   

    def __str__(self): 
        return self.user.username
# ----------------------------------------------------


# -------------CUSTOMER SUBSCRIBE MODEL--------------
class SubscriberProfile(models.Model):
    name = models.CharField(max_length=20, null=True)
    user_email = models.EmailField(max_length=254)
# ----------------------------------------------------

#--------------CONTACT US MODEL----------------------
class ContactProfile(models.Model):
    user_name= models.CharField(max_length=20)
    phone_number = models.IntegerField()
    user_email= models.EmailField(max_length=200)
    user_message= models.CharField(max_length=500)
#-----------------------------------------------------


class OrderDetail(models.Model):

    id = models.BigAutoField(primary_key=True)
    customer_email= models.EmailField(verbose_name='Customer Email')
    product= models.ForeignKey(to =MyCart, verbose_name='Product',  on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent= models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)