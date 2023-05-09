from django.db import models
from django.contrib.auth.models import User

from utils.slug_generator import unique_slug_generator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, editable=False, unique=True)

    def __str__(self):
        return str(self.user.username)

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self, variable=self.user.username)
        self.clean()
        super().save(*args, **kwargs)

