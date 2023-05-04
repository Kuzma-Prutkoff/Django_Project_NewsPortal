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

# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         group_for_all = Group.objects.get(name="BoTaNy")
#         user.groups.add(group_for_all)
#         return user

# При регистрации нвого юзера ему придет на почту письмо, либо текстом-либо html кодом(если поддерживается)
from django.core.mail import EmailMultiAlternatives
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/post">НАШЕМ Чудо-Портале</a>!'
        )
        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[user.email],)
        msg.attach_alternative(html, "text/html")
        msg.send()
        return user

# письмо менеджеру о регистрации нового юзера в сеттинге настройки почт манагеров
# from allauth.account.forms import SignupForm
# from django.core.mail import mail_managers
# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         mail_managers(subject='Новый пользователь!', message=f'Пользователь {user.username} зарегистрировался на сайте.')
#         return user

# письмо админу о регистрации нового юзера в сеттинге настройки почт админов
# from allauth.account.forms import SignupForm
# from django.core.mail import mail_admins
# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#         mail_admins(subject='Новый пользователь!', message=f'Пользователь {user.username} зарегистрировался на сайте.')
#         return user