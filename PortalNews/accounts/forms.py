from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2",)

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        group_for_all = Group.objects.get(name="BoTaNy")
        user.groups.add(group_for_all)
        return user