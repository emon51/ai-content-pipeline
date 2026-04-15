"""Service to generate and store per-ID JSON files in MinIO."""

from .storage import upload_json


def generate_per_id_files(site_name: str, ids: list[str], ai_result: dict) -> list[str]:
    """
    Generate one JSON file per ID using the AI-enhanced content.

    Each file is stored at:
        {site_name}/details/{id}.json

    Args:
        site_name: The site name (used as S3 prefix).
        ids: List of unique property IDs from CSV.
        ai_result: Dict with enhanced 'title' and 'description' from Groq.

    Returns:
        List of S3 keys where files were stored.

    Raises:
        botocore.exceptions.ClientError: On S3 upload failure.
    """
    stored_keys = []

    for property_id in ids:
        data = {
            "id": property_id,
            "title": ai_result["title"],
            "description": ai_result["description"],
        }

        key = f"{site_name}/details/{property_id}.json"
        upload_json(key, data)
        stored_keys.append(key)

    return stored_keys