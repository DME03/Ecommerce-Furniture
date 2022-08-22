from django.contrib import admin
from .models import Category, ContactProfile, BuyerProfile, MyCart, SubscriberProfile, SellerProfile, FurnitureItem
from .forms import Buyer_User_Form, Seller_User_Form

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    model = BuyerProfile
    add_form = Buyer_User_Form
    list_display = ("id", "user","phone_number","interest","city")

@admin.register(SellerProfile)
class SellerUserAdmin(admin.ModelAdmin):
    model = SellerProfile
    add_form = Seller_User_Form
    list_display = ("id", "user","phone_number","selling_item","fulfilled_by","city")


@admin.register(SubscriberProfile)
class SubscriberAdmin(admin.ModelAdmin):
    model = SubscriberProfile
    list_display= ('name','user_email')

@admin.register(ContactProfile)
class ContactAdmin(admin.ModelAdmin):
    model= ContactProfile
    list_display = ('user_name','phone_number','user_email','user_message')

@admin.register(FurnitureItem)
class FurnitureItemsAdmin(admin.ModelAdmin):
    class Meta:
        model= FurnitureItem
        list_diplay = ('id','title','price')

admin.site.register(Category)

@admin.register(MyCart)
class MyCartAdmin(admin.ModelAdmin):    
        list_diplay = ('id','user','item_selected','quantity')