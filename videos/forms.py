from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "file"]

    def clean_file(self):
        f = self.cleaned_data.get("file")
        if not f:
            raise forms.ValidationError("No file provided.")
        max_mb = 500
        if f.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"File too large. Max {max_mb} MB allowed.")
        return f
