from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    # primary key
    id = models.BigAutoField(primary_key=True, editable=False)

    GENDER = [("Male", "Male"), ("Female", "Female")]

    def get_upload_path(self, filename):
        return "images/{0}/{1}".format(self.user.username, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = PhoneNumberField(blank=False)
    about = models.CharField(max_length=450, blank=True)
    gender = models.CharField(
        "Gender", choices=GENDER, max_length=10, blank=False, default="Male"
    )
    image = models.ImageField(
        default="default.png",
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(["png", "jpg"])],
    )

    def get_absolute_url(self):
        return reverse('chat:chat-userprofile', kwargs={'pk': self.user.id})

    def __str__(self):
        return f"{self.user.username} Profile"

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
