from django.contrib import admin

from VideoRental.models import VideoTape, Reservation, Rental

admin.site.register(VideoTape)
admin.site.register(Reservation)
admin.site.register(Rental)
