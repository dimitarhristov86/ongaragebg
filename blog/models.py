from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Categorie(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog-home')


class Post(models.Model):
    title = models.CharField(max_length=258)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='no_image.png', upload_to='posts_images')
    categories = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


