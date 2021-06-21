import datetime

import wtforms
import wtforms.widgets
from cfgv import ValidationError
from django.forms import ModelForm, HiddenInput
from VideoRental.models import VideoTape, Reservation, Rental

from videorentalshop.users.models import User


class VideoTapeForm(ModelForm):
    """VideoTape model form for creating VideoTapes."""
    class Meta:
        model = VideoTape
        fields = '__all__'


class ReservationForm(ModelForm):
    """Reservation model form for booking VideoTapes."""
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that current user is the only available option & checks if there
        are VideoTapes available for booking.
        """
        self.request = kwargs.pop('request')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['videotape'].queryset = VideoTape.objects.filter(quantity__gt=0)
        self.fields['user'].queryset = User.objects.filter(id=self.request.user.id)
        self.fields['user'].initial = User.objects.get(id=self.request.user.id)
        self.fields['user'].widget = HiddenInput()

    class Meta:
        model = Reservation
        fields = ['videotape', 'user']


class RentalForm(ModelForm):
    """Rental model form for renting VideoTapes."""
    def __init__(self, *args, **kwargs):
        """Checks if current reservation is not already completed (VideoTape rented)."""
        super(RentalForm, self).__init__(*args, **kwargs)
        self.fields['return_helper'].widget = HiddenInput()
        self.fields['reservation'].queryset = Reservation.objects.filter(isrented=False)

    class Meta:
        model = Rental
        fields = ['reservation', 'return_helper', 'isreturned']

