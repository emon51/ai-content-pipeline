"""API views for the content pipeline."""

from botocore.exceptions import ClientError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PipelineInputSerializer
from .services.csv_parser import parse_and_validate_csv
from .services.storage import upload_json, download_json
from .services.ai_processor import enhance_content, build_title_prompt, build_description_prompt


class PipelineProcessView(APIView):
    """
    POST /api/v1/process/

    Full pipeline:
      1. Validate form input
      2. Parse single-row CSV → extract id, title, description
      3. Inject CSV data into prompt templates
      4. Store modified prompts + id + site_name as input.json
      5. Send modified prompts to Groq AI
      6. Store raw AI response as output.json
      7. Store processed id + title + description as {id}.json
    """

    def post(self, request):

        # Step 1: Validate form input
        serializer = PipelineInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data

        # Step 2: Parse single-row CSV
        try:
            csv_row = parse_and_validate_csv(validated["csv_file"])
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        site_name          = validated["site_name"]
        title_prompt       = validated["title_prompt"]
        description_prompt = validated["description_prompt"]
        csv_id             = csv_row["id"]
        csv_title          = csv_row["title"]
        csv_description    = csv_row["description"]

        # Step 3 & 4: Build modified prompts and store as input.json
        modified_title_prompt       = build_title_prompt(title_prompt, csv_title)
        modified_description_prompt = build_description_prompt(description_prompt, csv_description)

        input_payload = {
            "id":                          csv_id,
            "site_name":                   site_name,
            "modified_title_prompt":       modified_title_prompt,
            "modified_description_prompt": modified_description_prompt,
        }

        input_key = f"{site_name}/details/input/input.json"
        try:
            upload_json(input_key, input_payload)
        except Exception as e:
            return Response(
                {"error": f"Input storage failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Step 5: Send to Groq AI
        try:
            ai_result = enhance_content(
                title_prompt=title_prompt,
                description_prompt=description_prompt,
                csv_title=csv_title,
                csv_description=csv_description,
            )
        except Exception as e:
            return Response(
                {"error": f"AI processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Step 6: Store raw AI response as output.json
        raw_output = {
            "id":          csv_id,
            "site_name":   site_name,
            "title":       ai_result["title"],
            "description": ai_result["description"],
        }

        output_key = f"{site_name}/details/output/output.json"
        try:
            upload_json(output_key, raw_output)
        except Exception as e:
            return Response(
                {"error": f"Output storage failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Step 7: Store processed result as {id}.json
        id_payload = {
            "id":          csv_id,
            "title":       ai_result["title"],
            "description": ai_result["description"],
        }

        id_key = f"{site_name}/details/{csv_id}.json"
        try:
            upload_json(id_key, id_payload)
        except Exception as e:
            return Response(
                {"error": f"ID file storage failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "message":        "Pipeline completed successfully.",
                "input_stored_at":  input_key,
                "output_stored_at": output_key,
                "id_file_stored_at": id_key,
                "ai_result": {
                    "title":       ai_result["title"],
                    "description": ai_result["description"],
                },
            },
            status=status.HTTP_200_OK,
        )

class PropertyDetailView(APIView):
    """
    GET /api/v1/<site_name>/details/<id>/

    Retrieve the generated JSON file for a specific property ID.

    URL Params:
        site_name: The site identifier (e.g. rentbyowner.com).
        id:        The property ID (e.g. BC-12199453).

    Returns:
        JSON content of {site_name}/details/{id}.json from MinIO.
    """

    def get(self, request, site_name, id):
        key = f"{site_name}/details/{id}.json"

        try:
            data = download_json(key)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
                return Response(
                    {"error": f"No file found for ID '{id}' under site '{site_name}'."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {"error": f"Storage error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data, status=status.HTTP_200_OK)