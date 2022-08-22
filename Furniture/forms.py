from django import forms
from django.contrib.auth.models import User
from .models import BuyerProfile, SellerProfile
from django.contrib.auth.forms import AuthenticationForm


# ---------------Buyer Form---------------------------
class Buyer_Registration_Form(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        
        error_messages= {
            'password':{'required' : 'Password is mandatory.'}
        }

        widgets = {
            'password': forms.PasswordInput(),
        }

    
class Buyer_User_Form(forms.ModelForm):
    class Meta:
        model= BuyerProfile
        fields= ['phone_number','city']

# ---------------END Buyer Form---------------------------
    

# -----------------Seller Form----------------------------
class Seller_Registration_Form(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        
        error_messages= {
            'password':{'required' : 'Password is mandatory.'}
        }

        widgets = {
            'password': forms.PasswordInput(),
        }


class Seller_User_Form(forms.ModelForm):
    class Meta:
        model= SellerProfile
        fields= ['phone_number','city']

# -----------------END Seller Form-------------------------


# -----------------AUTHENTICATION FORM-------------------------
class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

# -----------------END AUTHENTICATION FORM-------------------------
