from django.db import models
from users.models import Teacher

import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, filename)


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=PathAndRename('news_images/'), blank=True, null=True)
    video = models.FileField(upload_to=PathAndRename('news_videos/'), blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.like_set.count()


class Like(models.Model):
    user = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'news')


