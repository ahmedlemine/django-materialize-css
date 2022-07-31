from autoslug import AutoSlugField
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation



class CustomPostManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-added')


class CustomCommentManger(models.Manager):
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
    
    @property
    def comments(self):
        return Comment.objects.filter(post=self)
    
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count() 

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    objects = CustomCommentManger()

    def __str__(self):
        return f"{self.user} on {self.post}"