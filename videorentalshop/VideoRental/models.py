from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from VideoRental.utils import generate_slug


class VideoTape(models.Model):
    """Product model class"""
    title = models.CharField(max_length=256, verbose_name=_("VideoTape Title"))
    slug = models.SlugField(max_length=256, unique=True, editable=False)
    description = models.TextField(verbose_name=_("VideoTape Description"))
    thumbnail = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.title.strip()
            for candidate in generate_slug(base):
                if not VideoTape.objects.filter(slug=candidate).exists():
                    self.slug = candidate
                    break
            else:
                raise Exception("Can't create new Project object")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
