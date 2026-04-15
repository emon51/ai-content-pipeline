"""API views for the content pipeline."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PipelineInputSerializer
from .services.csv_parser import parse_and_validate_csv
from .services.storage import upload_json
from .services.ai_processor import enhance_content


class PipelineProcessView(APIView):
    """
    POST /api/process/
    Accepts site_name, title, description, and a CSV file.
    Parses CSV, stores raw input, enhances content via Groq AI,
    stores AI response to MinIO.
    """

    def post(self, request):
        serializer = PipelineInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data

        # Step 2: Parse CSV
        try:
            ids = parse_and_validate_csv(validated["csv_file"])
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        site_name = validated["site_name"]
        title = validated["title"]
        description = validated["description"]

        payload = {
            "site_name": site_name,
            "title": title,
            "description": description,
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

        # Step 4: Enhance content via Groq AI
        try:
            ai_result = enhance_content(title, description)
        except Exception as e:
            return Response(
                {"error": f"AI processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Step 5: Store AI response in MinIO
        ai_output_key = f"{site_name}/details/output/ai_response.json"
        try:
            upload_json(ai_output_key, ai_result)
        except Exception as e:
            return Response(
                {"error": f"AI response storage failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": "Content enhanced and stored successfully.",
                "input_stored_at": input_key,
                "ai_response_stored_at": ai_output_key,
                "ai_result": ai_result,
            },
            status=status.HTTP_200_OK,
        )