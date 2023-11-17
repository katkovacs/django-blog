from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='user_profile/pics', default='user_profile/default_profile_pic.png')
    bio = models.CharField(max_length=200, blank=True, default='')
    slug = models.SlugField(default="", null=False)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save( *args, **kwargs)

        img = Image.open(self.profile_pic.path) # Open image

        # resize image
        if img.height > 80 or img.width > 80:
            output_size = (80, 80)
            img.thumbnail(output_size) # Resize image
            img.save(self.profile_pic.path) # Save it again and override the larger image

    def follow(self, other_user):
        if other_user.user not in self.following.all() and self.user not in other_user.followers.all():
            self.following.add(other_user.user)
            other_user.followers.add(self.user)

    def unfollow(self, other_user):
        if other_user.user in self.following.all() and self.user in other_user.followers.all():
            self.following.remove(other_user.user)
            other_user.followers.remove(self.user)

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

