from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member
from django.forms import ModelForm
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Member
        fields = ('username', 'first_name', 'last_name')


class SignupForm(UserCreationForm):
    username = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name')


class EditMemberForm(ModelForm):
	class Meta:
		model = Member
		fields = '__all__'
		exclude = ['username', 'items_per_page']
