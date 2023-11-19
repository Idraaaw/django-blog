from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import UserProfile

User = get_user_model()

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='密码', 
        widget=forms.PasswordInput,
        required=True,
        )
    password2 = forms.CharField(
        label='确认密码', 
        widget=forms.PasswordInput, 
        required=True,
        )
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True,label="电子邮箱")
    first_name = forms.CharField(label='姓氏')
    last_name = forms.CharField(label='名字')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['words','website','qq','wechat','github','bilibili','pic',]
