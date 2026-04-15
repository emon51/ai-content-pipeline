"""API views for the content pipeline."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PipelineInputSerializer
from .services.csv_parser import parse_and_validate_csv
from .services.storage import upload_json


class PipelineProcessView(APIView):
    """
    POST /api/process/
    Accepts site_name, title, description, and a CSV file.
    Parses CSV, stores raw input to MinIO.
    """

    def post(self, request):
        serializer = PipelineInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data

        try:
            ids = parse_and_validate_csv(validated["csv_file"])
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        site_name = validated["site_name"]

        payload = {
            "site_name": site_name,
            "title": validated["title"],
            "description": validated["description"],
            "ids": ids,
        }

        # Step 3: Store raw input in MinIO
        input_key = f"{site_name}/details/input/input.json"

        try:
            upload_json(input_key, payload)
        except Exception as e:
            return Response(
                {"error": f"Storage failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Input stored successfully.", "stored_at": input_key, "payload": payload},
            status=status.HTTP_200_OK,
        )