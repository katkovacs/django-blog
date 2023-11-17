from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

import misaka

# Create your models here.
user_model = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(user_model, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    post_pic = models.ImageField(upload_to='posts/images/')
    message = models.TextField(blank=True, default='')
    message_html = models.TextField(editable=False, blank=True, default='')
    likes = models.ManyToManyField(user_model, blank=True, related_name='user_likes')

    def __str__(self) -> str:
        result = self.message[:50]
        if len(self.message) > 49:
            result += '...'
        return result
    
    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',
                       kwargs={
                           'slug': self.user.username,
                           'pk': self.pk})

    def like(self, user_profile):
        if user_profile.user not in self.likes.all():
            self.likes.add(user_profile.user)
            user_profile.likes.add(self)

    def unlike(self, user_profile):
        if user_profile.user in self.likes.all():
            self.likes.remove(user_profile.user)
            user_profile.likes.remove(self)

    @property
    def is_liked(self, user):
        return user in self.likes.all()
    
    @property
    def like_count(self):
        return self.likes.count()
 
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
