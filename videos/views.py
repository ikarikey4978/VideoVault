from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden, HttpResponseNotAllowed

from .forms import VideoUploadForm
from .models import Video
from .utils import compute_sha256_of_uploaded_file


def home(request):
    videos = Video.objects.order_by("-uploaded_at")
    form = VideoUploadForm()
    return render(request, "videos/home.html", {"videos": videos, "form": form})


@login_required
def upload_video(request):
    if request.method != "POST":
        return redirect("videos:home")

    form = VideoUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Upload failed. Please fix the errors.")
        videos = Video.objects.order_by("-uploaded_at")
        return render(request, "videos/home.html", {"videos": videos, "form": form})

    uploaded_file = request.FILES["file"]
    file_hash = compute_sha256_of_uploaded_file(uploaded_file)

    existing = Video.objects.filter(file_hash=file_hash).first()
    if existing:
        messages.warning(
            request,
            f"Duplicate video detected. Already uploaded by {existing.uploaded_by} "
            f"on {existing.uploaded_at}.",
        )
        return redirect("videos:home")

    video = form.save(commit=False)
    video.uploaded_by = request.user
    video.file_hash = file_hash
    video.size = uploaded_file.size

    try:
        video.save()
    except IntegrityError:
        messages.warning(request, "Duplicate detected while saving. The file was not saved.")
        return redirect("videos:home")

    messages.success(request, "Video uploaded successfully.")
    return redirect("videos:home")


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, "videos/detail.html", {"video": video})


@login_required
def delete_video(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    video = get_object_or_404(Video, pk=pk)

    if request.user != video.uploaded_by and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to delete this video.")

    try:
        if video.file:
            video.file.delete(save=False)
        video.delete()
    except Exception:
        messages.error(request, "An error occurred while deleting the video.")
        return redirect("videos:detail", pk=pk)

    messages.success(request, "Video deleted successfully.")
    return redirect("videos:home")
