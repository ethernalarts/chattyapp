from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            msg = "Passwords do not match."
            self.add_error("password1", msg)
            self.add_error("password2", msg)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileForm(forms.ModelForm):
    phone_number = PhoneNumberField(region="NG", required=False)
    about = forms.CharField(
        max_length=300, required=False, widget=forms.Textarea(attrs={"rows": 6})
    )

    class Meta:
        model = Profile
        fields = ["gender", "phone_number", "about", "image"]

# class PasswordResetForm(PasswordResetForm):
