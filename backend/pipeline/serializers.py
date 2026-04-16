"""Request serializers for pipeline input validation."""

from rest_framework import serializers


class PipelineInputSerializer(serializers.Serializer):
    """
    Validates the incoming form data from the frontend.

    Fields:
        site_name:            Target site identifier.
        title_prompt:         SEO title prompt template with {PropertyName} placeholder.
        description_prompt:   SEO description prompt template with {PropertyDescription} placeholder.
        csv_file:             CSV file with exactly one row (id, title, description).
    """

    site_name          = serializers.CharField(max_length=255)
    title_prompt       = serializers.CharField()
    description_prompt = serializers.CharField()
    csv_file           = serializers.FileField()

    def validate_title_prompt(self, value):
        """Ensure title prompt contains the {PropertyName} placeholder."""
        if "{PropertyName}" not in value:
            raise serializers.ValidationError(
                "title_prompt must contain the {PropertyName} placeholder."
            )
        return value

    def validate_description_prompt(self, value):
        """Ensure description prompt contains the {PropertyDescription} placeholder."""
        if "{PropertyDescription}" not in value:
            raise serializers.ValidationError(
                "description_prompt must contain the {PropertyDescription} placeholder."
            )
        return value

    def validate_csv_file(self, value):
        """Ensure uploaded file has a .csv extension."""
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("Uploaded file must be a .csv.")
        return value