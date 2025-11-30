#!/usr/bin/env python3
"""
Test if a specific model works with GitHub Copilot API.
Usage: python test_model.py <model-name>
Example: python test_model.py gemini-2.5-pro
"""

import asyncio
import sys
from backend.github_models import query_github_model
from backend.github_auth import GitHubAuth
from backend.config import GITHUB_CLIENT_ID


async def test_model(model_name: str):
    """Test if a model works with the GitHub Copilot API."""

    # Load token
    auth = GitHubAuth(GITHUB_CLIENT_ID)
    token = auth.load_token()

    if not token:
        print("❌ ERROR: No GitHub token found!")
        print("\nPlease authenticate first:")
        print("  1. Run: ./start.sh")
        print("  2. Open http://localhost:5173")
        print("  3. Login with GitHub\n")
        sys.exit(1)

    print(f"🧪 Testing model: {model_name}")
    print("-" * 60)

    # Simple test message
    messages = [{"role": "user", "content": "Say 'Hello' in exactly 1 word."}]

    print("⏳ Querying model...\n")

    result = await query_github_model(
        model=model_name, messages=messages, access_token=token, timeout=30.0
    )

    if result is None:
        print(f"❌ FAILED: Model '{model_name}' is not available or returned an error.")
        print("\nPossible reasons:")
        print("  • Model name is incorrect")
        print("  • Model not enabled in GitHub settings")
        print("  • Model requires GitHub Copilot Pro+")
        print("\nTo see available models, run: python list_models.py")
        return False

    print(f"✅ SUCCESS: Model '{model_name}' works!")
    print(f"\nResponse: {result.get('content', 'No content')}")
    print("\n" + "-" * 60)
    print(f"You can now use this in backend/config.py:")
    print(f'  {{"provider": "github", "model": "{model_name}"}}')
    print()
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_model.py <model-name>")
        print("\nExamples:")
        print("  python test_model.py gemini-2.5-pro")
        print("  python test_model.py gpt-5")
        print("  python test_model.py claude-sonnet-4.5")
        print("\nTo see all available models: python list_models.py")
        sys.exit(1)

    model_name = sys.argv[1]
    asyncio.run(test_model(model_name))
