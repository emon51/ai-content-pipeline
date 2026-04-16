"""CSV parsing and validation service."""

import csv
import io


def parse_and_validate_csv(file) -> dict:
    """
    Parse uploaded CSV file and return a single row as a dict.

    Expected CSV format:
        id,title,description
        BC-12199453,The Bluefin - Luxury Beach Home!,6-bedroom beach home in Destin.

    Args:
        file: InMemoryUploadedFile from request.FILES

    Returns:
        Dict with keys: id, title, description.

    Raises:
        ValueError: If CSV is missing required columns, has no rows,
                    or contains more than one data row.
    """
    try:
        decoded = file.read().decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("CSV file must be UTF-8 encoded.")

    reader = csv.DictReader(io.StringIO(decoded))

    required_columns = {"id", "title", "description"}
    missing = required_columns - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    rows = [row for row in reader if row.get("id", "").strip()]

    if len(rows) == 0:
        raise ValueError("CSV contains no valid data rows.")

    if len(rows) > 1:
        raise ValueError("CSV must contain exactly one data row.")

    row = rows[0]

    return {
        "id":          row["id"].strip(),
        "title":       row["title"].strip(),
        "description": row["description"].strip(),
    }