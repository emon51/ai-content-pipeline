"""URL routes for the pipeline app."""

from django.urls import path
from .views import PipelineProcessView

urlpatterns = [
    path("process/", PipelineProcessView.as_view(), name="pipeline-process"),
]