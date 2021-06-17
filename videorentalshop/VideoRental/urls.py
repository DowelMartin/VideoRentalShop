from django.urls import path
from VideoRental.views import VideoTapeListView

app_name = "videotapes"
urlpatterns = [path("", VideoTapeListView.as_view(), name="list"),]
