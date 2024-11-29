from django.urls import path

from apps.api.views import StationHTMLView, StationListAPIView, UploadFileView

urlpatterns = [
    path("upload/", UploadFileView.as_view(), name="upload-file"),
    path("stations/json/", StationListAPIView.as_view(), name="stations-json"),
    path("stations/html/", StationHTMLView.as_view(), name="stations-html"),
]
