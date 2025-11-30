#!/bin/bash

# LLM Council - Start script

echo "═══════════════════════════════════════════════════════════"
echo "  LLM Council - Multi-Model Deliberation System"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Starting services..."
echo ""

# Start backend
echo "→ Starting backend on http://localhost:8001..."
uv run python -m backend.main &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend
echo "→ Starting frontend on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✓ LLM Council is running!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Backend:  http://localhost:8001"
echo "  Frontend: http://localhost:5173"
echo ""
echo "───────────────────────────────────────────────────────────"
echo "  Next Steps:"
echo "  1. Open http://localhost:5173 in your browser"
echo "  2. Authenticate with GitHub Copilot"
echo "  3. Start a new conversation"
echo "───────────────────────────────────────────────────────────"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped.'; exit" SIGINT SIGTERM
wait
