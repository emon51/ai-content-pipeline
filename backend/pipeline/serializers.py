"""Serializers for pipeline input validation."""

from rest_framework import serializers


class PipelineInputSerializer(serializers.Serializer):
    """Validates the incoming form data from the frontend."""

    site_name = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=500)
    description = serializers.CharField()
    csv_file = serializers.FileField()

    def validate_csv_file(self, value):
        """Ensure uploaded file has a .csv extension."""
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("Uploaded file must be a .csv.")
        return value