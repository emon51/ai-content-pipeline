"""AI processing service using Groq API for SEO content enhancement."""

from groq import Groq
from django.conf import settings


def get_groq_client() -> Groq:
    """Create and return a Groq client using Django settings."""
    return Groq(api_key=settings.GROQ_API_KEY)


def build_title_prompt(title_prompt: str, csv_title: str) -> str:
    """
    Inject CSV row title into the title prompt template.

    Args:
        title_prompt: Prompt template containing {PropertyName} placeholder.
        csv_title:    Property title from CSV row.

    Returns:
        Fully constructed title prompt string.
    """
    return title_prompt.replace("{PropertyName}", csv_title)


def build_description_prompt(description_prompt: str, csv_description: str) -> str:
    """
    Inject CSV row description into the description prompt template.

    Args:
        description_prompt: Prompt template containing {PropertyDescription} placeholder.
        csv_description:    Property description from CSV row.

    Returns:
        Fully constructed description prompt string.
    """
    return description_prompt.replace("{PropertyDescription}", csv_description)


def enhance_title(modified_prompt: str) -> str:
    """
    Send fully constructed title prompt to Groq and return SEO title.

    Args:
        modified_prompt: Title prompt with {PropertyName} already replaced.

    Returns:
        SEO-enhanced title as plain text.

    Raises:
        Exception: On Groq API failure.
    """
    client = get_groq_client()

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": modified_prompt}],
        temperature=0.7,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()


def enhance_description(modified_prompt: str) -> str:
    """
    Send fully constructed description prompt to Groq and return SEO HTML description.

    Args:
        modified_prompt: Description prompt with {PropertyDescription} already replaced.

    Returns:
        SEO-enhanced description as HTML with exactly one <p> tag.

    Raises:
        Exception: On Groq API failure.
    """
    client = get_groq_client()

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": modified_prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()


def enhance_content(
    title_prompt: str,
    description_prompt: str,
    csv_title: str,
    csv_description: str,
) -> dict:
    """
    Build modified prompts by injecting CSV data, then enhance via Groq AI.

    Args:
        title_prompt:       Raw title prompt template from frontend.
        description_prompt: Raw description prompt template from frontend.
        csv_title:          Property title extracted from CSV row.
        csv_description:    Property description extracted from CSV row.

    Returns:
        Dict with keys:
            - modified_title_prompt:       Final prompt sent to AI for title.
            - modified_description_prompt: Final prompt sent to AI for description.
            - title:                       AI-enhanced SEO title.
            - description:                 AI-enhanced SEO HTML description.
    """
    modified_title_prompt       = build_title_prompt(title_prompt, csv_title)
    modified_description_prompt = build_description_prompt(description_prompt, csv_description)

    enhanced_title       = enhance_title(modified_title_prompt)
    enhanced_description = enhance_description(modified_description_prompt)

    return {
        "modified_title_prompt":       modified_title_prompt,
        "modified_description_prompt": modified_description_prompt,
        "title":                       enhanced_title,
        "description":                 enhanced_description,
    }