from django.urls import path
from VideoRental.views import VideoTapeListView
from VideoRental.views import VideoTapeDetailView

app_name = "videotapes"
urlpatterns = [path("", VideoTapeListView.as_view(), name="list"), path("<str:slug>/", VideoTapeDetailView.as_view(), name="detail")]
