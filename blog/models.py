from unicodedata import category
from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.id})"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    visits = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    categories = models.ManyToManyField(Category,
                                        blank=True,
                                        null=True,
                                        related_name="posts")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments")

    def __str__(self):
        return self.text
