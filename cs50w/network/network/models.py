from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="followers")

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.username,
            "following": len([following.pk for following in self.following.all()]),
            "followers": len([follower.pk for follower in self.followers.all()]),
        }


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=255)
    likes = models.ManyToManyField("User", related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user.username,
            "content": self.content,
            "likes": len([like.pk for like in self.likes.all()]),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
