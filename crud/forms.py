from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from .models import Admins

class RegisterForm(forms.ModelForm):
    registration_key = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Admins
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'style': 'width:100%; padding:8px; border-radius:4px; border:1px solid #6D2932; background:#E8D8C4; color:#561C24;'
            })

    def clean_registration_key(self):
        key = self.cleaned_data.get('registration_key')
        if key != settings.REGISTRATION_KEY:
            raise forms.ValidationError('Invalid registration key.')
        return key

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
    
    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.password = self.cleaned_data['password']  # hash this in production!
        if commit:
            admin.save()
        return admin
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'style': 'width:100%; padding:8px; border-radius:4px; border:1px solid #6D2932; background:#E8D8C4; color:#561C24;'
            })