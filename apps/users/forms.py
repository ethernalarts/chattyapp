from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField()

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
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    phone_number = PhoneNumberField(region="NG")

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'phone_number', 'about', 'image']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 6}),
        }
