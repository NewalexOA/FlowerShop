from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class ProductAdminForm(forms.ModelForm):
    image_file = forms.ImageField(label="Изображение", required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image_file']

    def save(self, commit=True):
        instance = super(ProductAdminForm, self).save(commit=False)
        image = self.cleaned_data.get('image_file')

        if image:
            instance.save_image(image)

        if commit:
            instance.save()
        return instance

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, required=True, label='Адрес доставки')
    comment = forms.CharField(widget=forms.Textarea, required=False, label='Комментарий')
