from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView

from VideoRental.models import VideoTape
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from VideoRental.forms import VideoTapeForm
from django.urls import reverse_lazy


class VideoTapeListView(ListView):
    model = VideoTape
    paginate_by = 100

    context_object_name = "videotapes"


class VideoTapeDetailView(DetailView):
    model = VideoTape


class VideoTapeCreateView(CreateView):
    model = VideoTape
    form_class = VideoTapeForm


class VideoTapeUpdateView(UpdateView):
    model = VideoTape
    form_class = VideoTapeForm

class VideoTapeDeleteView(DeleteView):
    model = VideoTape
    success_url = reverse_lazy("videotapes:list")
