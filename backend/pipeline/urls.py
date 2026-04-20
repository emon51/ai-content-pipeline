"""URL routes for the pipeline app."""

from django.urls import path
from .views import PipelineProcessView, PropertyDetailView

urlpatterns = [
    path("process/",                          PipelineProcessView.as_view(), name="pipeline-process"),
    path("<str:site_name>/details/<str:id>/", PropertyDetailView.as_view(),  name="property-detail"),
]