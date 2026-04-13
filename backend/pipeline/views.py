"""API views for the content pipeline."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PipelineInputSerializer
from .services.csv_parser import parse_and_validate_csv


class PipelineProcessView(APIView):
    """
    POST /api/process/
    Accepts site_name, title, description, and a CSV file.
    Parses and validates input, returns structured data.
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

        payload = {
            "site_name": validated["site_name"],
            "title": validated["title"],
            "description": validated["description"],
            "ids": ids,
        }

        return Response(payload, status=status.HTTP_200_OK)