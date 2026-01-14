from django.urls import path
from . import views

app_name = "videos"

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_video, name="upload"),
    path("video/<int:pk>/", views.video_detail, name="detail"),
    path("video/<int:pk>/delete/", views.delete_video, name="delete"),
]
