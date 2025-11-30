"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# API Keys and Authentication
# ============================================================================

# OpenRouter API key (optional - for paid models)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# GitHub OAuth Client ID (required for GitHub Copilot models)
# You can override this by setting GITHUB_CLIENT_ID in .env
# Default Client ID for public distribution (you'll add yours here)
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "Ov23liTtv37ffCvVFZuH")

# ============================================================================
# Model Configuration
# ============================================================================

# Council members - list of model configurations
# Format: {"provider": "github|openrouter", "model": "model-id"}
#
# Available models via GitHub Copilot API (verified Nov 30, 2025):
#
# OpenAI GPT Series:
# - gpt-5 (Latest GPT-5)
# - gpt-5-mini (Smaller/faster GPT-5)
# - gpt-4.1 (GPT-4.1)
# - gpt-4o (GPT-4 Optimized - multiple versions available)
# - gpt-4o-mini (Smaller/faster GPT-4o)
# - gpt-4-o-preview (GPT-4o preview)
# - gpt-4 (GPT-4 base)
# - gpt-3.5-turbo (GPT-3.5 Turbo)
#
# Anthropic Claude Series:
# - claude-sonnet-4.5 (Latest Claude Sonnet 4.5)
# - claude-sonnet-4 (Claude Sonnet 4)
# - claude-haiku-4.5 (Fast Claude Haiku 4.5)
#
# Google Gemini Series:
# - gemini-2.5-pro (Gemini 2.5 Pro)
#
# xAI Grok:
# - grok-code-fast-1 (Grok optimized for code)
#
# Note: Full list retrieved via GitHub Copilot API
# Some models may require enabling in: https://github.com/settings/copilot

COUNCIL_MODELS = [
    # Active models - diverse set of top performers from different companies
    {"provider": "github", "model": "claude-sonnet-4.5"},  # Anthropic Claude Sonnet 4.5
    {"provider": "github", "model": "gemini-2.5-pro"},  # Google Gemini 2.5 Pro
    {"provider": "github", "model": "gpt-5"},  # OpenAI GPT-5
    {"provider": "github", "model": "grok-code-fast-1"},  # xAI Grok (code-optimized)
    # Popular alternatives (commented out - uncomment to add to council)
    # {"provider": "github", "model": "gpt-4.1"},  # OpenAI GPT-4.1
    # {"provider": "github", "model": "gpt-4o"},  # OpenAI GPT-4o
    # {"provider": "github", "model": "gpt-5-mini"},  # Smaller GPT-5
    # {"provider": "github", "model": "gpt-4o-mini"},  # Smaller GPT-4o
    # {"provider": "github", "model": "claude-sonnet-4"},  # Claude Sonnet 4
    # {"provider": "github", "model": "claude-haiku-4.5"},  # Fast Claude Haiku
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = {"provider": "github", "model": "claude-sonnet-4.5"}

# Alternative: Use OpenRouter for specific models (requires OPENROUTER_API_KEY in .env)
# Uncomment if you want to mix GitHub Copilot models with OpenRouter models
# COUNCIL_MODELS = [
#     {"provider": "github", "model": "claude-sonnet-4.5"},
#     {"provider": "github", "model": "gemini-2.0-flash-exp"},
#     {"provider": "openrouter", "model": "anthropic/claude-sonnet-4.5"},
#     {"provider": "openrouter", "model": "google/gemini-2.0-flash"},
#     {"provider": "openrouter", "model": "openai/gpt-4o"},
# ]
# CHAIRMAN_MODEL = {"provider": "openrouter", "model": "google/gemini-2.0-flash"}

# ============================================================================
# API Endpoints
# ============================================================================

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GITHUB_MODELS_API_URL = "https://api.githubcopilot.com/chat/completions"

# ============================================================================
# Storage
# ============================================================================

# Data directory for conversation storage
DATA_DIR = "data/conversations"
