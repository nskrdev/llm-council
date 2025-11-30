# GitHub Copilot Setup Guide

This guide will help you set up GitHub authentication so you can use your GitHub Copilot subscription with LLM Council.

## Prerequisites

- Active GitHub Copilot subscription (Individual, Pro, or Pro+)
- GitHub account

## Step 1: Create a GitHub OAuth App

1. Go to **GitHub Settings** → **Developer settings** → **OAuth Apps**
   - Direct link: https://github.com/settings/developers

2. Click **"New OAuth App"**

3. Fill in the application details:
   ```
   Application name: LLM Council
   Homepage URL: http://localhost
   Authorization callback URL: http://localhost
   ```
   
   > Note: The callback URL won't actually be used (Device Flow doesn't need it), but GitHub requires you to fill it in.

4. Click **"Register application"**

5. On the next page, find and check the **"Enable Device Flow"** checkbox
   - This is CRITICAL - without it, authentication won't work

6. Copy your **Client ID** (it looks like: `Iv1.a1b2c3d4e5f6g7h8`)

## Step 2: Configure Your Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and paste your Client ID:
   ```bash
   GITHUB_CLIENT_ID=Iv1.YOUR_ACTUAL_CLIENT_ID_HERE
   ```

3. Save the file

## Step 3: Start the Backend

```bash
python -m backend.main
```

The backend should start on port 8001.

## Step 4: Authenticate via the Frontend

1. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

2. Open your browser to `http://localhost:5173`

3. You should see an "Authenticate with GitHub" button

4. Click it and follow the device flow:
   - You'll see a code (e.g., `8F43-6FCF`)
   - Visit https://github.com/login/device
   - Enter the code
   - Authorize the application

5. Once authorized, your token will be saved locally and you can start using the council!

## Step 5: Configure Your Council

Edit `backend/config.py` to choose which models you want in your council:

```python
COUNCIL_MODELS = [
    {"provider": "github", "model": "gpt-4o"},
    {"provider": "github", "model": "claude-3.5-sonnet"},
    {"provider": "github", "model": "gemini-1.5-pro"},
    {"provider": "github", "model": "o1"},
]

CHAIRMAN_MODEL = {"provider": "github", "model": "gemini-1.5-pro"}
```

Available GitHub models (may vary by subscription tier):
- `gpt-4o`, `gpt-4o-mini`, `gpt-4`
- `claude-3.5-sonnet`, `claude-3-opus`
- `gemini-1.5-pro`, `gemini-1.5-flash`
- `o1`, `o1-mini`

> **Note**: Some models require GitHub Copilot Pro+ subscription

## Troubleshooting

### "Client ID not configured"
- Make sure you copied `.env.example` to `.env`
- Verify `GITHUB_CLIENT_ID` is set in `.env`
- Restart the backend after changing `.env`

### "Enable Device Flow" checkbox missing
- Make sure you're on the OAuth App settings page, not the GitHub App page
- The checkbox appears after you create the app

### Authentication fails
- Check that you entered the device code correctly
- Make sure your GitHub account has an active Copilot subscription
- Try logging out and starting the flow again

### Models returning 403/404 errors
- Some models require Pro+ tier
- Check your Copilot subscription level at https://github.com/settings/copilot
- Try with commonly available models like `gpt-4o` or `claude-3.5-sonnet`

## Token Storage

Your GitHub access token is stored locally at:
```
~/.llm-council-github-token.json
```

This file has restrictive permissions (600) for security. To log out and clear it:
- Use the logout button in the UI, or
- Manually delete the file

## Security Notes

- **Never commit `.env` to version control** - it contains your Client ID
- Your access token is stored locally and never sent to any server except GitHub
- The OAuth app only requests minimal permissions (`user:email` scope)
- You can revoke access anytime at https://github.com/settings/applications

## Next Steps

Once authenticated, you can:
1. Start a new conversation
2. Ask questions and watch the 3-stage council process
3. Inspect individual model responses, peer rankings, and the final synthesis
4. Experiment with different model combinations in `config.py`

Enjoy your LLM Council!
