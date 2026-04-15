"""AI processing service using Groq API for SEO content enhancement."""

from groq import Groq
from django.conf import settings


TITLE_PROMPT = """You are an expert travel blogger who creates content for high-performing travel accommodation, event, and activity booking websites that are search engine optimized. Rephrase the "{PropertyName}" title into a more SEO-friendly title. Use only the provided data without introducing new information or assumptions. The output should be in plain text. The text should be SEO-optimized for keywords related to the location. Incorporate the location naturally within the content."""

DESCRIPTION_PROMPT = """You are an expert travel blogger who creates content for high-performing travel accommodation, event and activity booking websites that are search engine optimized. Rephrase the "{PropertyDescription}" description into a more SEO-friendly and engaging paragraph. Use only the provided data without adding new assumptions. Output MUST be HTML with exactly ONE <p> tag only."""


def get_groq_client() -> Groq:
    """Create and return a Groq client using Django settings."""
    return Groq(api_key=settings.GROQ_API_KEY)


def enhance_title(title: str) -> str:
    """
    Send title to Groq and return SEO-optimized plain text title.

    Args:
        title: Original property title.

    Returns:
        SEO-enhanced title as plain text.

    Raises:
        Exception: On Groq API failure.
    """
    client = get_groq_client()
    prompt = TITLE_PROMPT.replace("{PropertyName}", title)

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()


def enhance_description(description: str) -> str:
    """
    Send description to Groq and return SEO-optimized HTML description.

    Args:
        description: Original property description.

    Returns:
        SEO-enhanced description as HTML with exactly one <p> tag.

    Raises:
        Exception: On Groq API failure.
    """
    client = get_groq_client()
    prompt = DESCRIPTION_PROMPT.replace("{PropertyDescription}", description)

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()


def enhance_content(title: str, description: str) -> dict:
    """
    Enhance both title and description using Groq AI.

    Args:
        title: Original property title.
        description: Original property description.

    Returns:
        Dict with enhanced 'title' and 'description'.

    Raises:
        Exception: On Groq API failure.
    """
    enhanced_title = enhance_title(title)
    enhanced_description = enhance_description(description)

    return {
        "title": enhanced_title,
        "description": enhanced_description,
    }