from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    def get_upload_path(self, filename):
        return "images/{0}/{1}".format(self.user.username, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to=get_upload_path)

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to be displayed
