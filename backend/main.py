"""FastAPI backend for LLM Council."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import json
import asyncio

from . import storage
from . import provider
from .council import (
    run_full_council,
    generate_conversation_title,
    stage1_collect_responses,
    stage2_collect_rankings,
    stage3_synthesize_final,
    calculate_aggregate_rankings,
)
from .github_auth import GitHubAuth, verify_github_token
from .config import GITHUB_CLIENT_ID

app = FastAPI(title="LLM Council API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load saved GitHub token on startup
@app.on_event("startup")
async def startup_event():
    """Load saved tokens on startup."""
    if GITHUB_CLIENT_ID:
        auth = GitHubAuth(GITHUB_CLIENT_ID)
        token = auth.load_token()
        if token:
            # Verify it's still valid
            is_valid = await verify_github_token(token)
            if is_valid:
                provider.set_github_token(token)
                print("✓ Loaded saved GitHub token")
            else:
                print("✗ Saved GitHub token is invalid, clearing")
                auth.clear_token()


class CreateConversationRequest(BaseModel):
    """Request to create a new conversation."""

    pass


class SendMessageRequest(BaseModel):
    """Request to send a message in a conversation."""

    content: str


class PollAuthRequest(BaseModel):
    """Request to poll for GitHub auth token."""

    device_code: str


class ConversationMetadata(BaseModel):
    """Conversation metadata for list view."""

    id: str
    created_at: str
    title: str
    message_count: int


class Conversation(BaseModel):
    """Full conversation with all messages."""

    id: str
    created_at: str
    title: str
    messages: List[Dict[str, Any]]


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "LLM Council API"}


# ============================================================================
# GitHub Authentication Endpoints
# ============================================================================


@app.post("/api/auth/github/start")
async def start_github_auth():
    """
    Start GitHub Device Flow authentication.
    Returns device code and verification URL for user.
    """
    if not GITHUB_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="GitHub Client ID not configured. Please set GITHUB_CLIENT_ID in .env",
        )

    auth = GitHubAuth(GITHUB_CLIENT_ID)

    try:
        flow_data = await auth.start_device_flow()
        return {
            "user_code": flow_data["user_code"],
            "verification_uri": flow_data["verification_uri"],
            "device_code": flow_data["device_code"],
            "expires_in": flow_data["expires_in"],
            "interval": flow_data.get("interval", 5),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start auth flow: {str(e)}"
        )


@app.post("/api/auth/github/poll")
async def poll_github_auth(request: PollAuthRequest):
    """
    Poll for GitHub access token after user authorizes.
    Call this repeatedly until you get a token or error.
    """
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub Client ID not configured")

    auth = GitHubAuth(GITHUB_CLIENT_ID)

    try:
        token = await auth.poll_for_token(request.device_code, interval=5, timeout=5)

        if token:
            # Store token in provider module
            provider.set_github_token(token)

            return {"status": "success", "token": token}
        else:
            return {"status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Polling failed: {str(e)}")


@app.get("/api/auth/github/status")
async def github_auth_status():
    """Check if GitHub token is available and valid."""
    token = provider.get_github_token()

    if not token:
        # Try to load from saved file
        if GITHUB_CLIENT_ID:
            auth = GitHubAuth(GITHUB_CLIENT_ID)
            token = auth.load_token()
            if token:
                provider.set_github_token(token)

    if token:
        # Verify token is still valid
        is_valid = await verify_github_token(token)
        return {"authenticated": is_valid, "provider": "github"}

    return {"authenticated": False}


@app.post("/api/auth/github/logout")
async def github_logout():
    """Clear GitHub authentication."""
    if GITHUB_CLIENT_ID:
        auth = GitHubAuth(GITHUB_CLIENT_ID)
        auth.clear_token()

    provider.set_github_token(None)

    return {"status": "logged_out"}


@app.get("/api/github/models")
async def list_github_models():
    """List all available GitHub Copilot models."""
    from .github_models import list_available_models

    token = provider.get_github_token()
    if not token:
        raise HTTPException(
            status_code=401, detail="Not authenticated with GitHub. Please login first."
        )

    models = await list_available_models(token)

    if models is None:
        raise HTTPException(
            status_code=500, detail="Failed to fetch models from GitHub API"
        )

    # Categorize models
    categorized = {
        "openai": [m for m in models if "gpt" in m.lower() or "o1" in m.lower()],
        "anthropic": [m for m in models if "claude" in m.lower()],
        "google": [m for m in models if "gemini" in m.lower()],
        "xai": [m for m in models if "grok" in m.lower()],
        "other": [
            m
            for m in models
            if not any(
                x in m.lower()
                for x in ["gpt", "o1", "claude", "gemini", "grok", "embedding"]
            )
        ],
    }

    return {"total": len(models), "models": models, "categorized": categorized}


# ============================================================================
# Conversation Endpoints
# ============================================================================


@app.get("/api/conversations", response_model=List[ConversationMetadata])
async def list_conversations():
    """List all conversations (metadata only)."""
    return storage.list_conversations()


@app.post("/api/conversations", response_model=Conversation)
async def create_conversation(request: CreateConversationRequest):
    """Create a new conversation."""
    conversation_id = str(uuid.uuid4())
    conversation = storage.create_conversation(conversation_id)
    return conversation


@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation with all its messages."""
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@app.post("/api/conversations/{conversation_id}/message")
async def send_message(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and run the 3-stage council process.
    Returns the complete response with all stages.
    """
    # Check if conversation exists
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if this is the first message
    is_first_message = len(conversation["messages"]) == 0

    # Add user message
    storage.add_user_message(conversation_id, request.content)

    # If this is the first message, generate a title
    if is_first_message:
        title = await generate_conversation_title(request.content)
        storage.update_conversation_title(conversation_id, title)

    # Run the 3-stage council process
    stage1_results, stage2_results, stage3_result, metadata = await run_full_council(
        request.content
    )

    # Add assistant message with all stages
    storage.add_assistant_message(
        conversation_id, stage1_results, stage2_results, stage3_result
    )

    # Return the complete response with metadata
    return {
        "stage1": stage1_results,
        "stage2": stage2_results,
        "stage3": stage3_result,
        "metadata": metadata,
    }


@app.post("/api/conversations/{conversation_id}/message/stream")
async def send_message_stream(conversation_id: str, request: SendMessageRequest):
    """
    Send a message and stream the 3-stage council process.
    Returns Server-Sent Events as each stage completes.
    """
    # Check if conversation exists
    conversation = storage.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if this is the first message
    is_first_message = len(conversation["messages"]) == 0

    async def event_generator():
        try:
            # Add user message
            storage.add_user_message(conversation_id, request.content)

            # Start title generation in parallel (don't await yet)
            title_task = None
            if is_first_message:
                title_task = asyncio.create_task(
                    generate_conversation_title(request.content)
                )

            # Stage 1: Collect responses
            yield f"data: {json.dumps({'type': 'stage1_start'})}\n\n"
            stage1_results = await stage1_collect_responses(request.content)
            yield f"data: {json.dumps({'type': 'stage1_complete', 'data': stage1_results})}\n\n"

            # Stage 2: Collect rankings
            yield f"data: {json.dumps({'type': 'stage2_start'})}\n\n"
            stage2_results, label_to_model = await stage2_collect_rankings(
                request.content, stage1_results
            )
            aggregate_rankings = calculate_aggregate_rankings(
                stage2_results, label_to_model
            )
            yield f"data: {json.dumps({'type': 'stage2_complete', 'data': stage2_results, 'metadata': {'label_to_model': label_to_model, 'aggregate_rankings': aggregate_rankings}})}\n\n"

            # Stage 3: Synthesize final answer
            yield f"data: {json.dumps({'type': 'stage3_start'})}\n\n"
            stage3_result = await stage3_synthesize_final(
                request.content, stage1_results, stage2_results
            )
            yield f"data: {json.dumps({'type': 'stage3_complete', 'data': stage3_result})}\n\n"

            # Wait for title generation if it was started
            if title_task:
                title = await title_task
                storage.update_conversation_title(conversation_id, title)
                yield f"data: {json.dumps({'type': 'title_complete', 'data': {'title': title}})}\n\n"

            # Save complete assistant message
            storage.add_assistant_message(
                conversation_id, stage1_results, stage2_results, stage3_result
            )

            # Send completion event
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        except Exception as e:
            # Send error event
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
