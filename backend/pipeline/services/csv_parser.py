"""CSV parsing and validation service."""

import csv
import io


def parse_and_validate_csv(file) -> list[str]:
    """
    Parse uploaded CSV file and return a deduplicated list of IDs.

    Expected CSV format:
        id,title,description
        BC-12199453,Some Title,Some Description

    Args:
        file: InMemoryUploadedFile from request.FILES

    Returns:
        List of unique ID strings.

    Raises:
        ValueError: If CSV is missing 'id' column or has no valid rows.
    """
    try:
        decoded = file.read().decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("CSV file must be UTF-8 encoded.")

    reader = csv.DictReader(io.StringIO(decoded))

    if "id" not in (reader.fieldnames or []):
        raise ValueError("CSV must contain an 'id' column.")

    ids = []
    for row in reader:
        raw_id = row.get("id", "").strip()
        if raw_id:
            ids.append(raw_id)

    if not ids:
        raise ValueError("CSV contains no valid ID rows.")

    # Deduplicate while preserving order
    seen = set()
    unique_ids = []
    for id_ in ids:
        if id_ not in seen:
            seen.add(id_)
            unique_ids.append(id_)

    return unique_ids