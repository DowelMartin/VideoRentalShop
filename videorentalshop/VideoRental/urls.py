from django.urls import path
from VideoRental.views import (
    VideoTapeListView, VideoTapeDetailView, VideoTapeCreateView, VideoTapeUpdateView)


app_name = "videotapes"
urlpatterns = [path("", VideoTapeListView.as_view(), name="list"),
               path("<str:slug>/", VideoTapeDetailView.as_view(), name="detail"),
               path("create/", VideoTapeCreateView.as_view(), name="create"),
               path("<str:slug>/update/", VideoTapeUpdateView.as_view(), name="update")]
