from django import forms
from phonenumber_field.formfields import PhoneNumberField

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

class SignUpForm(forms.Form):
    phone_number = PhoneNumberField()
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password_confirmation')
        if password != password2:
            raise forms.ValidationError("Password do not match")
        return cleaned_data

