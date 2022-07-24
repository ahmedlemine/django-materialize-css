from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.dispatch import receiver
# from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    # add additional fields in here
    pass

    def __str__(self):
        return self.email

# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     age = models.IntegerField(null=True, blank=True)
#     nickname = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.user.username

# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)