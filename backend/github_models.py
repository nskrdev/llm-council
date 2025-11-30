"""GitHub Models API client for querying models via GitHub Copilot."""

import httpx
from typing import List, Dict, Any, Optional


async def query_github_model(
    model: str,
    messages: List[Dict[str, str]],
    access_token: str,
    timeout: float = 120.0,
) -> Optional[Dict[str, Any]]:
    """
    Query a model via GitHub Models API.

    Args:
        model: Model identifier (e.g., "gpt-4o", "claude-3.5-sonnet", "o1")
        messages: List of message dicts with 'role' and 'content'
        access_token: GitHub access token from device flow
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    # GitHub Copilot Chat Completions API endpoint
    API_URL = "https://api.githubcopilot.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()

            data = response.json()
            message = data["choices"][0]["message"]

            return {
                "content": message.get("content"),
                "reasoning_details": message.get("reasoning_details"),
            }

    except Exception as e:
        print(f"Error querying GitHub model {model}: {e}")
        return None


async def list_available_models(access_token: str) -> Optional[List[str]]:
    """
    List available models from GitHub Models API.

    Args:
        access_token: GitHub access token

    Returns:
        List of model identifiers, or None if failed
    """
    API_URL = "https://api.githubcopilot.com/models"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL, headers=headers)
            response.raise_for_status()

            data = response.json()
            # Extract model IDs from response
            if "data" in data:
                return [model["id"] for model in data["data"]]
            return []

    except Exception as e:
        print(f"Error listing GitHub models: {e}")
        return None


# Model name mappings - Azure/GitHub format
# Based on GitHub's model marketplace
GITHUB_MODEL_MAPPINGS = {
    # OpenAI models
    "gpt-4o": "gpt-4o",
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4": "gpt-4",
    "o1-preview": "o1-preview",
    "o1-mini": "o1-mini",
    # Anthropic models
    "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
    "claude-sonnet-4.5": "claude-3-5-sonnet-20241022",
    "claude-3-opus": "claude-3-opus-20240229",
    "claude-3-haiku": "claude-3-haiku-20240307",
    # Google models
    "gemini-1.5-pro": "gemini-1.5-pro",
    "gemini-1.5-flash": "gemini-1.5-flash",
    "gemini-2.0-flash": "gemini-2.0-flash-exp",
}
