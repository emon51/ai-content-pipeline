"""API views for the content pipeline."""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PipelineInputSerializer
from .services.csv_parser import parse_and_validate_csv
from .services.storage import upload_json
from .services.ai_processor import enhance_content
from .services.id_generator import generate_per_id_files


class PipelineProcessView(APIView):
    """
    POST /api/process/
    Full pipeline:
      1. Validate input
      2. Parse CSV
      3. Store raw input to MinIO
      4. Enhance content via Groq AI
      5. Store AI response to MinIO
      6. Generate per-ID JSON files in MinIO
    """

    def post(self, request):
        # Step 1: Validate input
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

        # Step 6: Generate per-ID JSON files
        try:
            id_keys = generate_per_id_files(site_name, ids, ai_result)
        except Exception as e:
            return Response(
                {"error": f"Per-ID file generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message": "Pipeline completed successfully.",
                "input_stored_at": input_key,
                "ai_response_stored_at": ai_output_key,
                "per_id_files": id_keys,
                "ai_result": ai_result,
            },
            status=status.HTTP_200_OK,
        )