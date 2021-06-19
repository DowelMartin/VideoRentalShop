import datetime

from cfgv import ValidationError
from django.forms import ModelForm
from VideoRental.models import VideoTape, Reservation

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

    class Meta:
        model = Reservation
        fields = ['videotape', 'user']

