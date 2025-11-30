"""Unified interface for querying different LLM providers."""

import asyncio
from typing import List, Dict, Any, Optional
from .openrouter import query_model as query_openrouter_model
from .github_models import query_github_model
from .config import OPENROUTER_API_KEY


# Global storage for user's GitHub token (set during authentication)
_github_token: Optional[str] = None


def set_github_token(token: str):
    """Set the GitHub access token for API calls."""
    global _github_token
    _github_token = token


def get_github_token() -> Optional[str]:
    """Get the current GitHub access token."""
    return _github_token


async def query_model(
    provider: str, model: str, messages: List[Dict[str, str]], timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a model from any supported provider.

    Args:
        provider: Provider name ("github", "openrouter")
        model: Model identifier
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    if provider == "github":
        token = get_github_token()
        if not token:
            print(f"Error: No GitHub token available for model {model}")
            return None
        return await query_github_model(model, messages, token, timeout)

    elif provider == "openrouter":
        if not OPENROUTER_API_KEY:
            print(f"Error: No OpenRouter API key configured for model {model}")
            return None
        return await query_openrouter_model(model, messages, timeout)

    else:
        print(f"Error: Unknown provider '{provider}' for model {model}")
        return None


async def query_models_parallel(
    model_configs: List[Dict[str, str]], messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models from different providers in parallel.

    Args:
        model_configs: List of dicts with 'provider' and 'model' keys
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping "provider/model" to response dict (or None if failed)
    """
    # Create tasks for all models
    tasks = []
    model_keys = []

    for config in model_configs:
        provider = config["provider"]
        model = config["model"]

        # Create unique key for this model
        model_key = f"{provider}/{model}"
        model_keys.append(model_key)

        # Create query task
        task = query_model(provider, model, messages)
        tasks.append(task)

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map model keys to their responses
    return {key: response for key, response in zip(model_keys, responses)}


def format_model_display_name(provider: str, model: str) -> str:
    """
    Format a model name for display in the UI.

    Args:
        provider: Provider name
        model: Model identifier

    Returns:
        Formatted display name
    """
    if provider == "github":
        return f"GitHub: {model}"
    elif provider == "openrouter":
        # For OpenRouter, the model already includes provider info
        return model
    else:
        return f"{provider}/{model}"
