from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        self.fields['username'].help_text = 'Не более 150 символов.<br /> Только буквы, цифры и @/./+/-/_.'
        self.fields['password1'].help_text = (
            'Ваш пароль должен содержать не менее 8 символов.<br />'
            'Ваш пароль не может состоять только из цифр.'
        )
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения.'


