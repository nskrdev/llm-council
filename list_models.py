#!/usr/bin/env python3
"""
List all available GitHub Copilot models.
Run this script to see which models you can use in your council.
"""

import asyncio
import sys
from backend.github_models import list_available_models
from backend.github_auth import GitHubAuth
from backend.config import GITHUB_CLIENT_ID


async def main():
    print("=" * 70)
    print("  GitHub Copilot - Available Models")
    print("=" * 70)
    print()

    # Load token
    auth = GitHubAuth(GITHUB_CLIENT_ID)
    token = auth.load_token()
    if not token:
        print("❌ ERROR: No GitHub token found!")
        print()
        print("Please authenticate first:")
        print("  1. Run: ./start.sh")
        print("  2. Open http://localhost:5173")
        print("  3. Login with GitHub")
        print()
        sys.exit(1)

    print("✓ Token loaded successfully")
    print("⏳ Fetching available models from GitHub Copilot API...\n")

    # Fetch models
    models = await list_available_models(token)

    if models is None or not models:
        print("❌ Failed to fetch models.")
        print("   This could mean:")
        print("   - Your token has expired")
        print("   - Network connectivity issue")
        print("   - GitHub API is down")
        print("\n   Try authenticating again:")
        print("   1. Run: ./start.sh")
        print("   2. Open http://localhost:5173")
        print("   3. Login with GitHub")
        sys.exit(1)

    print(f"✓ Found {len(models)} available models:\n")
    print("-" * 70)

    # Categorize models
    categories = {
        "OpenAI GPT": [],
        "Anthropic Claude": [],
        "Google Gemini": [],
        "xAI Grok": [],
        "Meta Llama": [],
        "Other": [],
    }

    for model in sorted(models):
        model_lower = model.lower()

        if "gpt" in model_lower or "o1" in model_lower:
            categories["OpenAI GPT"].append(model)
        elif "claude" in model_lower:
            categories["Anthropic Claude"].append(model)
        elif "gemini" in model_lower:
            categories["Google Gemini"].append(model)
        elif "grok" in model_lower:
            categories["xAI Grok"].append(model)
        elif "llama" in model_lower:
            categories["Meta Llama"].append(model)
        elif "embedding" not in model_lower:  # Skip embedding models
            categories["Other"].append(model)

    # Print categorized
    for category, model_list in categories.items():
        if model_list:
            print(f"\n🤖 {category}:")
            for model in model_list:
                print(f"   • {model}")

    print()
    print("-" * 70)
    print(f"\n💡 To use these models, edit: backend/config.py")
    print(f"\n   Example:")
    print(f"   COUNCIL_MODELS = [")
    print(
        f'       {{"provider": "github", "model": "{models[0] if models else "gpt-4o"}"}},'
    )
    print(
        f'       {{"provider": "github", "model": "{models[1] if len(models) > 1 else "claude-sonnet-4.5"}"}},'
    )
    print(f"   ]")
    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
