from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView

from VideoRental.models import VideoTape


class VideoTapeListView(ListView):
    model = VideoTape
    paginate_by = 100

    context_object_name = "videotapes"


class VideoTapeDetailView(DetailView):
    model = VideoTape

