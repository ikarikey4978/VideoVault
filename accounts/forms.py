from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise forms.ValidationError("Enter a valid password.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return confirm
