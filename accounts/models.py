from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, default='new user', blank=True)
    bio = models.CharField(max_length=250, default='', blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/user_avatar.png')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(150, 150)],
                                      format='JPEG',
                                      options={'quality': 60})

    
    def __str__(self):
        return self.user.username
    

    def get_user_initials(self):
        return self.name[0]


#auto create user profile after user signup
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)