from django.forms import ModelForm
from VideoRental.models import VideoTape

class VideoTapeForm(ModelForm):
    class Meta:
        model = VideoTape
        fields = '__all__'
