import datetime

import requests
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from VideoRental.utils import generate_slug
from videorentalshop.users.models import User


class VideoTape(models.Model):
    """VideoTape model class"""
    title = models.CharField(max_length=256, verbose_name=_("VideoTape Title"))
    slug = models.SlugField(max_length=256, unique=True, editable=False)
    description = models.TextField(verbose_name=_("VideoTape Description"))
    genres = models.TextField(verbose_name=_("VideoTape Genres"), null=True)
    thumbnail = models.URLField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.title.strip()
            for candidate in generate_slug(base):
                if not VideoTape.objects.filter(slug=candidate).exists():
                    self.slug = candidate
                    break
            else:
                raise Exception("Can't create new VideoTape object")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get url for VideoTape's detail view.

        Returns:
            str: slug for VideoTape detail.

        """
        return reverse("videotapes:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class Reservation(models.Model):
    time_of_booking = models.DateField(editable=False, default=datetime.date.today())
    videotape = models.ForeignKey(VideoTape, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("videotapes:reservation_list")
