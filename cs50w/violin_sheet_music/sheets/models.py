from django.db import models
from django.contrib.auth.models import AbstractUser

from sheets.validators import validate_audio_file


# Create your models here.
class User(AbstractUser):
    pass


class Sheet(models.Model):
    name = models.CharField(max_length=150)
    sheet_url = models.URLField(default=None)
    img = models.ImageField(upload_to="sheet_images/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img.url,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Attempt(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    sheet = models.ManyToManyField("Sheet", related_name="attempts")
    ratings = models.ManyToManyField("User", related_name="ratings")
    rating = models.IntegerField(default=0)
    audio = models.FileField(
        upload_to="sheet_attempts/",
        validators=[validate_audio_file],
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "sheet": self.sheet.all(),
            "ratings": self.ratings.all(),
            "rating": self.rating,
            "audio": self.audio,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
