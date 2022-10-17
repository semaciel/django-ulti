from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from core.models import TrackingModel

User = get_user_model()

# Create your models here.
class SocialProfile(TrackingModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile_bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    # location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(TrackingModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    # created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

class Comment(TrackingModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='post_images')
    comment = models.TextField(max_length=1024)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
