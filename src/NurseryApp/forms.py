from django import forms
from django.core.validators import EmailValidator


class SignupUserForm(forms.Form):
    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    email = forms.EmailField(validators=[EmailValidator])

    def clean(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('passwords are not the same')
        return data
