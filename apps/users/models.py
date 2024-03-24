from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    def get_upload_path(self, filename):
        return "images/{0}/{1}".format(self.user.username, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(default='default.png', upload_to=get_upload_path)

    def __str__(self):
        return f'{self.user.username} Profile'  # show how we want it to be displayed

        # Override the save method of the model
    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)  # Open image
    #
    #     # resize image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)  # Resize image
    #         img.save(self.image.path)  # Save it again and override the larger image