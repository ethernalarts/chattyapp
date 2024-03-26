from django.db import models
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField


class SpeekUser(models.Model):
    GENDER = [("Male", "Male"), ("Female", "Female")]

    def get_upload_path(self, filename):
        return "images/{0}/{1}".format(self.username, filename)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=True)
    password = models.CharField(max_length=32)
    phone_number = PhoneNumberField(blank=True)
    about = models.CharField(max_length=1000, blank=True)
    gender = models.CharField(
        "Gender", choices=GENDER, max_length=100, blank=False, default="Male"
    )
    image = models.ImageField(
        default="default.png",
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(["png", "jpg"])],
    )

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
