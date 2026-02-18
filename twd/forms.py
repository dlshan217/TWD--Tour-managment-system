from django import forms
from .models import *

from .models import Usersign_up

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'inputmode':'tel'}))

    class Meta:
        model = Usersign_up
        fields = ['username', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder':'you@example.com', 'autocomplete':'email'}),
        }

class User_signupform(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'password-input',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = Usersign_up
        fields = ['username', 'password', 'email', 'phone']


class Userlogin(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'password-input',
            'autocomplete': 'current-password'
        })
    )

    class Meta:
        model = Usersign_up
        fields = ['username', 'password']


class Vendorregistorform(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'password-input',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = Vendorregister
        fields = ['businessname', 'businnesregistornumber', 'email', 'password', 'phone']


class Vendorlogin(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'class': 'password-input',
            'autocomplete': 'current-password'
        })
    )

    class Meta:
        model = Vendorregister
        fields = ['email', 'password']


class vpackageform(forms.ModelForm):
    class Meta:
        model = Packagecreate
        fields = ['title', 'description', 'date', 'image', 'price']



class Bookingdetailsform(forms.ModelForm):
    booking_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    number_of_people = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # We keep fullname & phone fields in form for display, but server overwrites them
    fullname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Bookingdetails
        fields = ['fullname', 'phone', 'number_of_people', 'booking_date']
    

from .models import Usersign_up  

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Usersign_up
        fields = ['username', 'email', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'phone': forms.TextInput(attrs={'class': 'input'}),
        }

