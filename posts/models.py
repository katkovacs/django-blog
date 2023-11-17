from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

import misaka

# Create your models here.
User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    post_pic = models.ImageField(upload_to='posts/images/')
    message = models.TextField(blank=True, default='')
    message_html = models.TextField(editable=False, blank=True, default='')

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
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
