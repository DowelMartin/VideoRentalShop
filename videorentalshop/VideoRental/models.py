import datetime
import ast

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from VideoRental.utils import generate_slug
from videorentalshop.users.models import User


class VideoTape(models.Model):
    """VideoTape model class"""
    title = models.CharField(max_length=256, verbose_name=_("Title"))
    slug = models.SlugField(max_length=256, unique=True, editable=False)
    description = models.TextField(verbose_name=_("Description"))
    genres = models.TextField(verbose_name=_("Genres"), null=True)
    production_countries = models.TextField(verbose_name=_("Production Countries"), null=True, blank=True)
    release_date = models.DateField(verbose_name=_("Release Date"), null=True, blank=True)
    vote_average = models.FloatField(verbose_name=_("Vote Average"), null=True, blank=True)
    thumbnail = models.URLField(verbose_name=_("Poster"), null=True, blank=True)
    quantity = models.IntegerField(verbose_name=_("Quantity"), validators=[MinValueValidator(1), MaxValueValidator(10)])

    @property
    def correct_genres(self):
        corrected_genres = ast.literal_eval(self.genres)
        list = []
        for genre in corrected_genres:
            correct_genre = genre.get('name')
            list.append(correct_genre)
        return list

    @property
    def correct_production_countries(self):
        corrected_production_countries = ast.literal_eval(self.production_countries)
        list = []
        for count in corrected_production_countries:
            correct_production_country = count.get('name')
            list.append(correct_production_country)
        return list

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
    time_of_booking = models.DateField(editable=False)
    end_of_booking = models.DateField(editable=False)
    videotape = models.ForeignKey(VideoTape, on_delete=models.CASCADE, blank = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False)
    isactive = models.BooleanField(default=True, blank=False)

    @property
    def is_active(self):
        if datetime.date.today() < self.end_of_booking:
            return datetime.date.today() < self.end_of_booking
        elif (datetime.date.today() > self.end_of_booking) and self.isactive is True:
            self.isactive = False
            self.videotape.quantity += 1
            self.save()
            self.videotape.save()
            return datetime.date.today() < self.end_of_booking
        else:
            return datetime.date.today() < self.end_of_booking

    def save(self, *args, **kwargs):
        if not self.pk:
            self.time_of_booking = datetime.date.today()
            self.end_of_booking = self.time_of_booking + datetime.timedelta(days=3)
            self.videotape.quantity -= 1
            self.videotape.save()
        return super(Reservation, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("videotapes:reservation_list")

    def __str__(self):
        return self.videotape.title + ": " + self.user.username
