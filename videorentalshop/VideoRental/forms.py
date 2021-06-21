import datetime

import wtforms
import wtforms.widgets
from cfgv import ValidationError
from django.forms import ModelForm, HiddenInput
from VideoRental.models import VideoTape, Reservation, Rental

from videorentalshop.users.models import User


class VideoTapeForm(ModelForm):
    class Meta:
        model = VideoTape
        fields = '__all__'


class ReservationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(id=self.request.user.id)
        self.fields['user'].initial = User.objects.get(id=self.request.user.id)
        self.fields['user'].widget = HiddenInput()

    class Meta:
        model = Reservation
        fields = ['videotape', 'user']


class RentalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RentalForm, self).__init__(*args, **kwargs)
        self.fields['time_of_rent'].widget = HiddenInput()
        self.fields['return_helper'].widget = HiddenInput()

    class Meta:
        model = Rental
        fields = '__all__'

