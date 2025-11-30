"""GitHub Device Flow OAuth authentication."""

import httpx
import time
from typing import Optional, Dict, Any
import json
import os


class GitHubAuth:
    """Handle GitHub Device Flow authentication."""

    # GitHub OAuth endpoints
    DEVICE_CODE_URL = "https://github.com/login/device/code"
    ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"

    def __init__(self, client_id: str):
        """
        Initialize GitHub auth handler.

        Args:
            client_id: Your GitHub OAuth app client ID
        """
        self.client_id = client_id
        self.token_file = os.path.expanduser("~/.llm-council-github-token.json")

    async def start_device_flow(self) -> Dict[str, str]:
        """
        Start the device authorization flow.

        Returns:
            Dict with device_code, user_code, verification_uri, expires_in, interval
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.DEVICE_CODE_URL,
                data={
                    "client_id": self.client_id,
                    "scope": "user:email",  # Add more scopes if needed
                },
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    async def poll_for_token(
        self, device_code: str, interval: int = 5, timeout: int = 300
    ) -> Optional[str]:
        """
        Poll GitHub for access token after user authorizes.

        Args:
            device_code: Device code from start_device_flow
            interval: Seconds between polling attempts
            timeout: Maximum time to wait in seconds

        Returns:
            Access token if successful, None if timeout or denied
        """
        start_time = time.time()

        async with httpx.AsyncClient() as client:
            while time.time() - start_time < timeout:
                response = await client.post(
                    self.ACCESS_TOKEN_URL,
                    data={
                        "client_id": self.client_id,
                        "device_code": device_code,
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    },
                    headers={"Accept": "application/json"},
                )

                data = response.json()

                # Check for successful authorization
                if "access_token" in data:
                    # Save token locally
                    self._save_token(data["access_token"])
                    return data["access_token"]

                # Check for errors
                error = data.get("error")
                if error == "authorization_pending":
                    # User hasn't authorized yet, keep waiting
                    await self._async_sleep(interval)
                    continue
                elif error == "slow_down":
                    # We're polling too fast, increase interval
                    interval += 5
                    await self._async_sleep(interval)
                    continue
                elif error == "expired_token":
                    # Device code expired
                    return None
                elif error == "access_denied":
                    # User denied authorization
                    return None
                else:
                    # Unknown error
                    print(f"Unknown error during token polling: {error}")
                    return None

        # Timeout reached
        return None

    async def _async_sleep(self, seconds: int):
        """Async sleep helper."""
        import asyncio

        await asyncio.sleep(seconds)

    def _save_token(self, token: str):
        """Save token to local file."""
        try:
            with open(self.token_file, "w") as f:
                json.dump({"access_token": token}, f)
            # Set restrictive permissions (owner read/write only)
            os.chmod(self.token_file, 0o600)
        except Exception as e:
            print(f"Warning: Could not save token to {self.token_file}: {e}")

    def load_token(self) -> Optional[str]:
        """Load previously saved token from local file."""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, "r") as f:
                    data = json.load(f)
                    return data.get("access_token")
        except Exception as e:
            print(f"Warning: Could not load token from {self.token_file}: {e}")
        return None

    def clear_token(self):
        """Remove saved token."""
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
        except Exception as e:
            print(f"Warning: Could not remove token file: {e}")


async def verify_github_token(token: str) -> bool:
    """
    Verify that a GitHub token is valid.

    Args:
        token: GitHub access token

    Returns:
        True if token is valid, False otherwise
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
            )
            return response.status_code == 200
    except Exception:
        return False
