from django.contrib import admin
from .models import SocialProfile, Post, LikePost, FollowersCount


# Register your models here.
admin.site.register(SocialProfile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
