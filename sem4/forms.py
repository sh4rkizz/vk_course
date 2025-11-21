from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", max_length=255, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=255, required=True)

    new_password = forms.CharField(label="Новый пароль", max_length=255, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Повтори пароль", max_length=255, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name"]

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError({"confirm_password": "Пароли не совпадают"})

        return cleaned_data
