# Custom authentication backend for email-based login

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        usermodel = get_user_model()

        # Check if the provided input is an email address
        if "@" in username:
            try:
                user = usermodel.objects.get(email=username)
            except usermodel.DoesNotExist:
                return None
            else:
                # Verify the password
                if user.check_password(password):
                    return user
                return None

        # if the provided input is not an email address
        try:
            user = usermodel.objects.get(username=username)
        except usermodel.DoesNotExist:
            return None
        else:
            # Verify the password
            if user.check_password(password):
                return user
            return None
