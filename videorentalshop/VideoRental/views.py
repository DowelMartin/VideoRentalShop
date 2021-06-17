from django.shortcuts import render
from django.views.generic.list import ListView

from VideoRental.models import VideoTape


class VideoTapeListView(ListView):
    model = VideoTape
    paginate_by = 100

    context_object_name = "videotapes"
