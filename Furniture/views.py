from re import M
from wsgiref.handlers import CGIHandler
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http.response import HttpResponseNotFound, JsonResponse
from django.urls import reverse
# from requests import request
from Furniture.models import Category, ContactProfile, MyCart, SubscriberProfile, BuyerProfile, SellerProfile, FurnitureItem,OrderDetail
from .forms import Buyer_Registration_Form, Buyer_User_Form, MyAuthenticationForm, Seller_Registration_Form, Seller_User_Form
from django.views.generic import TemplateView,DetailView,ListView
from django.contrib.auth import login, authenticate 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here. 

## ==========================STRIP CHECKOUT=============================

# ------------------------PRODUCT DETAIL--------------------------
class ProductDetailView(DetailView):
    model = MyCart
    template_name = "furniture/checkout/product_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


# ------------------------PRODUCT CHECKOUT--------------------------
@csrf_exempt
def create_checkout_session(request, id):
    if id == 'all_price':
        request_data = request.user.email
        # ALL PRODUCT PRICE
        all_price=0
        all_items = MyCart.objects.filter(cart_user_name=request.user)
        for i in all_items:
            all_price+=i.quantity_price
        # print(all_price)
        # product = get_object_or_404(MyCart, pk=id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side
            customer_email = request_data,
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                        'name': "All Products",
                        },
                        'unit_amount': all_price* 100,
                        
                    },
                    'quantity': 1,
                }
            ],
            
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )
        print('request.build_absolute_uri __________________________',request.build_absolute_uri)
        order = OrderDetail()
        order.customer_email = request_data
        order.stripe_payment_intent = checkout_session['payment_intent']
        order.amount = int(all_price * 100)
        order.save()

        # return JsonResponse({'data': checkout_session})
        return JsonResponse({'sessionId': checkout_session.id})
    else:
        request_data = json.loads(request.body)
        print("===============================ok================")
        product = get_object_or_404(MyCart, pk=id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side
            customer_email = request_data['email'],
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                        'name': product.item_selected,
                        },
                        'unit_amount': int(product.quantity_price * 100),
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )

        order = OrderDetail()
        order.customer_email = request_data['email']
        order.product = product
        order.stripe_payment_intent = checkout_session['payment_intent']
        order.amount = int(product.quantity_price * 100)
        order.save()

        # return JsonResponse({'data': checkout_session})
        return JsonResponse({'sessionId': checkout_session.id})
    

# ------------------------CHECKOUT SUCCESS--------------------------
class PaymentSuccessView(TemplateView):
    template_name = "furniture/checkout/payment_success.html"

    def get(self, request, *args, **kwargs):
        current_user  = request.user
        val = current_user
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        print(session,"ok_session_id=====================")
        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        print(order.product,"ok_order=====================")
        if (order.product == None):
            order= get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
            order.save()
            pi= MyCart.objects.filter(cart_user_name=current_user)
            pi.delete()
        else:
            order.has_paid = True
            order.save()
            pi= MyCart.objects.get(pk=order.product.id)
            pi.delete()
        return render(request, self.template_name, {'firstnm':val})

class PaymentFailedView(TemplateView):
    template_name = "furniture/checkout/payment_failed.html"

## ===========================END STRIP CHECKOUT=======================


# ------------------------DELETE MYCART DATA------------------------
def delete_data(request,id): 
    # if request.method == "POST":
    pi= MyCart.objects.get(pk=id)
    pi.delete()
    return redirect('b_cart')


# -------------------------MY CART FUNCTION------------------------------
def buy_now(request, id):
    current_user  = request.user
    val = current_user
    query_set= MyCart.objects.filter(cart_user_name=current_user) 
    item= FurnitureItem.objects.filter(id=id).first()
    item_prac= MyCart.objects.filter(cart_user_name=current_user).filter(item_selected=item).first()
    
    #  IGNORE THIS NOW..THIS ONE IS FOR QUANTITY INCREMENT
    if(query_set and item_prac):    
        if(item == item_prac.item_selected):
            quantity_incre=item_prac.quantity+1
            modify_price = item_prac.item_selected.price*quantity_incre
            MyCart.objects.filter(item_selected=item).update(quantity=quantity_incre, quantity_price= modify_price)

    else:
        cart= MyCart.objects.create(item_selected=item, cart_user_name=val, quantity_price=item.price )
        cart.save()
    return redirect('b_furni')


# ============================= QUANTITY AND PRICE MODIFY =============================

# ---------------------------- DECREMENT NEGATIVE SIGN------------------------------
@login_required
def quantity_price_modify_decre(request,id):
    # print(id)

    # QUANTITY AND PRICE MODIFY
    item= MyCart.objects.filter(id=id).first()
    # print(item.quantity)
    # print(item.quantity_price)
    if (item.quantity > 1):
        MyCart.objects.filter(item_selected=item.item_selected).update(quantity=item.quantity-1, quantity_price= item.quantity_price - item.item_selected.price)
        
    else:
        pi= MyCart.objects.get(pk=id)
        pi.delete()

    return redirect('b_cart')

# ---------------------------- INCREMENT POSITIVE SIGN------------------------------
@login_required
def quantity_price_modify_incre(request,id):
    # print(id)

    # QUANTITY AND PRICE MODIFY
    item= MyCart.objects.filter(id=id).first()
    # print(item.quantity)
    # print(item.quantity_price)

    MyCart.objects.filter(item_selected=item.item_selected).update(quantity=item.quantity+1, quantity_price= item.quantity_price + item.item_selected.price)

    return redirect('b_cart')


# -------------------------SEARCH FUNCTION--------------------------------

def search(request): 
    query = None
    result = []

    if request.method == 'POST':
        current_user  = request.user
        val = current_user.username
        all_cart_items= MyCart.objects.filter(cart_user_name=current_user)
        cnt=0
        for i in all_cart_items:
            cnt+=1
        query = request.POST.get('search')
        # print("-------------------7---------------->>>",query)
        request.session['search'] = query

        # print("-----------------2------------------>>>",query)
        if (query):
            query=query.lower()
            result = FurnitureItem.objects.filter(category__name=query)
            if not (result):
                result= FurnitureItem.objects.filter(title__icontains = query)
                if not (result):
                    result= FurnitureItem.objects.filter(price__icontains = query)

        # print(type(result),"-----------------------------------------------------")

        # print("------------------------",result)    

        return render(request, 'furniture/buyer/buyer_search.html',{'query':query,'result': result,'firstnm':val,'cnt':cnt,'all_cart_items':all_cart_items})
        
    current_user  = request.user
    val = current_user.username
    query = request.session['search']   
    return render(request, 'furniture/buyer/buyer_search.html',{'query':query ,'firstnm':val})



# ----------------FUNCTION FOR PAGINATION OF FURNITURE AND FILTER---------------------------

@login_required
def category(request,id, name):
    current_user  = request.user
    val = current_user.username
    all_cart_items= MyCart.objects.filter(cart_user_name=current_user)
    cnt=0
    for i in all_cart_items:
        cnt+=1
    categories = Category.objects.all()

    all_items =   FurnitureItem.objects.filter(category__id=id)
    cat= name
    # cat = Category.objects.filter(name="Sofa")
    # print("-==-==-=-=-=-=-=-=-=-=-=-",cat) 
    # print("===================>>",all_items)
    # print(all_items)
    # print("---------
    paginator = Paginator(all_items, 3)
       
    page_number= request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    # print("==========================>", products)
    
    return render(request, 'furniture/buyer/buyer_category.html',{"all_items":cat, 'page_obj':page_obj,'categories': categories,'firstnm':val,'cnt':cnt,'all_cart_items':all_cart_items})

@login_required()
def buyer_furniture(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        # print("-------------------1---------------->>>",query)
        request.session['search'] = query
        return redirect('search')
    categories = Category.objects.all()
    current_user  = request.user
    val = current_user.username
    all_cart_items= MyCart.objects.filter(cart_user_name=current_user)
    cnt=0
    for i in all_cart_items:
        cnt+=1
    all_items =   FurnitureItem.objects.all()
    # paginator = Paginator(all_items, 6)
    # page_number= request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    return render(request, 'furniture/buyer/buyer_furniture.html',{'firstnm':val,'page_obj':all_items, "categories":categories,"cnt":cnt,'all_items':all_cart_items})  

# ----------------END FUNCTION FOR PAGINATION OF FURNITURE AND FILTER---------------------------

# ----------------BUYER CART DETAILS----------------------------------------

@login_required()   
def buyer_cart(request):
    current_user  = request.user
    val = current_user.username
    all_cart_items= MyCart.objects.filter(cart_user_name=current_user)
    cnt=0
    for i in all_cart_items:
        cnt+=1
    # ALL PRODUCT PRICE
    all_price=0
    all_items = MyCart.objects.filter(cart_user_name=current_user)
    for i in all_items:
        all_price+=i.quantity_price
    # print(all_price)dhyeybrotherbig19

    cart_items_name = MyCart.objects.filter(cart_user_name=current_user)
    
    return render(request, 'furniture/buyer/buyer_cart.html',{'firstnm':val,'cart_items':cart_items_name,'all_price':all_price,'stripe_publishable_key':settings.STRIPE_PUBLISHABLE_KEY,'cnt':cnt})
    # return render(request, 'furniture/buyer/buyer_cart.html',{'firstnm':val})



@login_required()
def buyer_contact(request):
    current_user  = request.user
    val = current_user.username
    all_cart_items= MyCart.objects.filter(cart_user_name=current_user)
    cnt=0
    for i in all_cart_items:
        cnt+=1
    return render(request, 'furniture/buyer/buyer_contact.html',{'firstnm':val,'cnt':cnt})



def log_out(request):
    logout(request)
    return redirect('home')

# SELLER REGISTRATION FORM
def seller_reg(request):
    if request.method== "POST":
        frm = Seller_Registration_Form(request.POST)
        sel_form= Seller_User_Form(request.POST)
        selling_item = request.POST.getlist('selling_item[]')
        fulfilled_by= request.POST.get('fulfilled_by')
        x =','.join(selling_item)
        selling_item=str(x)

        if  frm.is_valid() and sel_form.is_valid():
            # print(request.POST.get('agree'))
            user =  frm.save()
            sel = sel_form.save(commit=False)  
            sel.user = user
            sel.selling_item=selling_item
            sel.fulfilled_by= fulfilled_by
            sel.save()

            fn= frm.cleaned_data['first_name']
            pw =frm.cleaned_data['password']
            user.set_password(pw)
            user.save()
            
            frm = Seller_Registration_Form()
            return redirect("success_reg_sel",firstnm= fn)

    else:
        frm= Seller_Registration_Form()
        sel_form = Seller_User_Form()

    return render(request, 'furniture/seller/seller_reg.html',{'form':frm,'seller_form':sel_form})

def success_reg_sel(request, firstnm):
    return render(request, 'furniture/seller/success_reg_sel.html',{'firstnm':firstnm})

# END SELLER REGISTRATION FORM

# SELLER BASE HTML
@login_required()
def base_seller(request):
    return render(request, 'furniture/seller/seller_home.html')

# SELLER BASE HTML
@login_required()
def base_buyer(request):
    current_user  = request.user
    val = current_user.username
    all_cart_items= MyCart.objects.filter(cart_user_name=current_user)
    cnt=0
    for i in all_cart_items:
        cnt+=1
    return render(request, 'furniture/buyer/buyer_home.html',{'firstnm':val,'cnt':cnt})

# BUYER REGISTRATION FORM
@csrf_exempt
def buyer_reg(request):
    if request.method== "POST":
        fm = Buyer_Registration_Form(request.POST)
        prof_form= Buyer_User_Form(request.POST)
        interest = request.POST.getlist('interest[]')
        x =','.join(interest)
        interest=str(x)

        if fm.is_valid() and prof_form.is_valid():
            # print(request.POST.get('agree')) 
            user = fm.save()

            prof = prof_form.save(commit=False)  
            prof.user = user
            prof.interest=interest

            prof.save()
            fn= fm.cleaned_data['first_name']
            pw = fm.cleaned_data['password'] 
            user.set_password(pw)
            user.save()
            
            fm = Buyer_Registration_Form()
            return redirect("success_reg_buy",firstnm= fn)

    else:
        fm= Buyer_Registration_Form()
        prof_form = Buyer_User_Form()

    return render(request, 'furniture/buyer/buyer_reg.html',{'form':fm,'buyer_form':prof_form})

def success_reg_buy(request, firstnm):
    return render(request, 'furniture/buyer/success_reg_buy.html',{'firstnm':firstnm})

# END BUYER REGISTRATION FORM

# LOGIN FORM
@csrf_exempt

def login(request):
    if request.method =="POST":
        fm= MyAuthenticationForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password= fm.cleaned_data.get('password')
            user= authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                current_user = request.user
                data1= BuyerProfile.objects.all()
                data2= SellerProfile.objects.all()
                # print(data1)
                # print(data2)
                # print(current_user.username,'---------------------------')
                val= current_user.username
                for i in data1:
                    # print(type(i),'...................XSDASDFAFASDFGDFGADSFADS')
                    # print(type(i.user.username),'-------------((()))))------')
                    # print(type(val))
                    if (i.user.username) == (val):
                        return redirect('buyer_home')
                
                for j in data2:
                    if (j.user.username) == (val):
                        return redirect('seller_home')
                        
                # print("IT IS A SELLER.")
                fm=MyAuthenticationForm()
                return redirect("home")
    else:
        fm= MyAuthenticationForm()

    return render(request, 'furniture/login.html', {'form':fm})
# END LOGIN FORM


# WEBSITE STANDARD WEBPAGES
def home(request):
    return render(request, 'furniture/index.html')

def buy_sel(request):
    return render(request, 'furniture/choose_bs.html')

def contact(request):
    return render(request, 'furniture/contact.html')

def about(request):
    return render(request, 'furniture/about.html')

def blog(request):
    return render(request, 'furniture/blog.html')

def furniture(request):
    return render(request, 'furniture/furniture.html')

def email_Subscriber(request):
    if request.method=="POST":
        email = request.POST.get('email')
        name= request.POST.get('name')
        # print("->>>>>>>>>>>>>>>>>>>>>>>hihihihihi>>>>>>>>>>>>>>>>",email)
        sub = SubscriberProfile(user_email=email, name= name)
        sub.save()
        return redirect('home')


def contact_sub(request):
    if request.method =="POST":
        name= request.POST.get('user_name')
        phonenumber= request.POST.get('phone_number')
        email= request.POST.get('user_email')
        message= request.POST.get('user_message')
        contact_submit= ContactProfile(user_name=name, phone_number=phonenumber, user_email=email,user_message=message)
        contact_submit.save()
        messages.success(request, "Your message has been successfully sent!!")
    return redirect('contact')

# END STANDARD WEBPAGES