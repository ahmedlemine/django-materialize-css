from autoslug import AutoSlugField
from django.urls import reverse
from django.db import models

class CustomPostManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-added')


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="title")
    body = models.TextField()
    image = models.ImageField(upload_to='images/', default='images/blank.png')
    added = models.DateTimeField(auto_now_add=True)


    objects = CustomPostManger()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs = {'slug': self.slug})