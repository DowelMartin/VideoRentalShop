from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from VideoRental.models import VideoTape, Reservation, Rental
from VideoRental.forms import VideoTapeForm, ReservationForm, RentalForm


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


class ReservationListView(ListView):
    model = Reservation
    paginate_by = 100

    context_object_name = "reservations"


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""
        kwargs = super(ReservationCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class RentalListView(ListView):
    model = Rental

    context_object_name = "rentals"


class RentalCreateView(CreateView):
    model = Rental
    form_class = RentalForm



