from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField()

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get("password1")
    #     password2 = cleaned_data.get("password2")
    #
    #     if password1 != password2:
    #         msg = "Passwords do not match."
    #         self.add_error("password1", msg)
    #         self.add_error("password2", msg)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
