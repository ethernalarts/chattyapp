from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext as _
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


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)

    def validate_passwords(self, password1, password2):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two passwords don't match."))
        return password1, password2

    def validate_password_for_user(self, user, password2):
        self.user = user
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two passwords don't match."))
        return password2

    def clean(self):
        self.validate_passwords("new_password1", "new_password2")
        self.validate_password_for_user(self.user, "new_password2")
        return super().clean()

    # def clean(self):
    #     cleaned_data = super(PasswordResetConfirmForm, self).clean()
    #
    #     password = cleaned_data.get("new_password1")
    #     password_confirm = cleaned_data.get("new_password2")
    #
    #     if password and password_confirm:
    #         if password != password_confirm:
    #             raise forms.ValidationError("Your passwords do not match.")
    #     return cleaned_data

    def save(self, commit=True):
        """
        Saves the new password.
        """
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    # def clean_new_password1(self):
    #     """
    #     Custom validation for the new password.
    #     """
    #     password = self.cleaned_data.get('new_password1')
    #     validate_password(password, self.user)
    #     return password
