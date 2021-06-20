from django.urls import path
from VideoRental.views import (
    VideoTapeListView, VideoTapeDetailView, VideoTapeCreateView, VideoTapeUpdateView, VideoTapeDeleteView,
    ReservationListView, ReservationCreateView, RentalListView, RentalCreateView )

app_name = "videotapes"
urlpatterns = [path("", VideoTapeListView.as_view(), name="list"),
               path("reservations/", ReservationListView.as_view(), name="reservation_list"),
               path("rentals/", RentalListView.as_view(), name="rental_list"),
               path("create/", VideoTapeCreateView.as_view(), name="create"),
               path("create_reservation/", ReservationCreateView.as_view(), name="create_reservation"),
               path("create_rental/", RentalCreateView.as_view(), name="create_rental"),
               path("<str:slug>/", VideoTapeDetailView.as_view(), name="detail"),
               path("<str:slug>/update/", VideoTapeUpdateView.as_view(), name="update"),
               path("<str:slug>/delete/", VideoTapeDeleteView.as_view(), name="delete"),
               ]
