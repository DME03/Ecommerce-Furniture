"""EcommerceFurniture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Furniture import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # WEBSITE STANDARD WEBPAGES URLS
    path('',views.home, name="home"),
    path('bs/',views.buy_sel,name= "choose_bs"),
    path('contact/', views.contact, name="contact"),
    path('about/',views.about,name="about"),
    path('blog/',views.blog,name="blog"),
    path('furniture_collec/', views.furniture, name="furniture"),
    path('subs/',views.email_Subscriber,name="subs"),
    path('cont/', views.contact_sub, name="con_sub"),

    # BUYER REGISTRATION/LOGIN URLS
    path('bs/b_reg/',views.buyer_reg, name="buy_reg"),
    path('success/buy/<str:firstnm>',views.success_reg_buy, name="success_reg_buy"),

    # COMMON LOGIN
    path('bs/log/', views.login, name="log"),

    # SELLER REGISTRATION/LOGIN URLS
    path('bs/s_reg/', views.seller_reg, name="sel_reg"),
    path('success/sel/<str:firstnm>',views.success_reg_sel, name="success_reg_sel"),

    # SELLER WEBPAGE URL
    path('seller/', views.base_seller, name= "seller_home"),

    # BUYER WEBPAGE URL
    path('buyer/', views.base_buyer, name= "buyer_home"),
    path('bcontact/',views.buyer_contact, name="b_contact"),
    path('bcart/',views.buyer_cart, name="b_cart"),
    path('bfurni/', views.buyer_furniture , name="b_furni"),
    path('category/<int:id>/<str:name>/', views.category , name="b_cat"),
    path('search/',views.search,name="search"),
    path('buy_cart/<int:id>', views.buy_now, name="buy_now"),
    path('delete/<int:id>', views.delete_data, name= "deletedata"),
    path('quantity_price__decre/<int:id>/', views.quantity_price_modify_decre, name="quantity_price_modify_decre"),
    path('quantity_price__incre/<int:id>/', views.quantity_price_modify_incre, name="quantity_price_modify_incre"),

    # LOGOUT
    path('logout/', views.log_out, name="oklogout"), 




    path('detail/<id>/', views.ProductDetailView.as_view(), name='detail'),

    path('api/checkout-session/<id>/', views.create_checkout_session, name='api_checkout_session'),
    
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),

    path('success/', views.PaymentSuccessView.as_view(), name='success'),


    # path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name="create-checkout-session")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
