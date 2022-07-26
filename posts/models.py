from autoslug import AutoSlugField
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

class CustomPostManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-added')


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(unique=True, always_update=False, populate_from="title")
    body = models.TextField()
    image = models.ImageField(upload_to='images/', default='images/blank.png')
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    added = models.DateTimeField(auto_now_add=True)
    hit_count_generic = GenericRelation(
                HitCount,
                object_id_field='object_pk',
                related_query_name='hit_count_generic_relation'
                )

    objects = CustomPostManger()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs = {'slug': self.slug})