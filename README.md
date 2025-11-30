# LLM Council

![llmcouncil](header.jpg)

**A deliberative democracy for AI models** - Get better answers by letting multiple LLMs debate, vote, and synthesize their collective wisdom.

---

## 🍴 About This Fork

**This is a fork of [@karpathy's LLM Council](https://github.com/karpathy/llm-council)** with one key modification: it uses **GitHub Copilot's free-tier models** instead of OpenRouter.

**Why this fork exists:**
As a student with GitHub Copilot access, I wanted to use LLM Council without paying for additional API credits. GitHub Copilot provides free access to GPT-5, Claude Sonnet 4.5, Gemini 2.5 Pro, and xAI Grok - perfect for students and developers who already have Copilot!

**Key differences from the original:**
- ✅ **GitHub Copilot integration** - Use your existing Copilot subscription (free for students!)
- ✅ **OAuth device flow** - Simple authentication, token saved locally
- ✅ **Enhanced UI** - Beautiful voting matrix, response key, podium rankings
- ✅ **Multi-provider support** - Still supports OpenRouter if you want to mix providers
- ✅ **No credit card needed** - If you have GitHub Copilot, you're ready to go!

**Original concept:** [@karpathy](https://x.com/karpathy) - [Original repo](https://github.com/karpathy/llm-council)

---

## 🎓 Perfect for Students!

If you're a student with **GitHub Student Developer Pack**, you already have Copilot for free! This means you can:
- Access GPT-5, Claude 4.5, Gemini 2.5 Pro, and Grok **at no cost**
- Run unlimited queries without worrying about API bills
- Experiment with cutting-edge AI models for learning and projects
- No credit card required!

**Get GitHub Student Pack:** [education.github.com/pack](https://education.github.com/pack)

---

## 🎯 What is LLM Council?

Instead of asking a single LLM for an answer, LLM Council orchestrates a 3-stage deliberation process where multiple AI models collaborate to produce superior responses:

### The 3-Stage Process

**Stage 1: Independent Responses** 💭
- Your question is sent to all council members simultaneously
- Each model provides their answer independently
- No model sees what others are saying yet

**Stage 2: Anonymous Peer Review** 🗳️
- Each model evaluates **all** responses (including their own!)
- Responses are anonymized as "Response A, B, C, D..." to prevent bias
- Models rank responses by quality without knowing who wrote what
- This prevents brand loyalty and ensures objective evaluation

**Stage 3: Chairman Synthesis** ⚖️
- A designated chairman model reviews all responses and rankings
- Synthesizes the best insights from the council's collective wisdom
- Produces a comprehensive final answer with reasoning

## 🌟 Why Anonymous Peer Review Works

Just like academic paper reviews, **blind evaluation prevents bias**:
- Models can't favor their own company's products
- GPT-5 doesn't know which response came from OpenAI
- Claude doesn't know which came from Anthropic
- Gemini doesn't know which came from Google
- Quality wins, not brand names!

**Note:** This anonymous peer review system is the core innovation from [@karpathy's original LLM Council](https://github.com/karpathy/llm-council). This fork simply makes it accessible using free GitHub Copilot models instead of paid OpenRouter credits.

## ✨ Key Features

- **🎨 Beautiful, Modern UI** - Color-coded models, voting matrix, podium rankings
- **🔒 GitHub Copilot Integration** - Free access to GPT-5, Claude 4.5, Gemini 2.5 Pro, Grok!
- **📊 Full Transparency** - See exactly how each model voted and why
- **🎯 Response Key** - Clear mapping showing which letter corresponds to which model
- **💾 Conversation History** - All deliberations saved locally
- **⚡ Fast & Async** - Parallel queries for maximum speed

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with npm
- A GitHub account (for Copilot access)

### 1. Install Dependencies

```bash
# Backend (Python)
uv sync

# Frontend (JavaScript)
cd frontend
npm install
cd ..
```

### 2. Setup GitHub Copilot Authentication

The app uses GitHub Copilot's free-tier models. No credit card required!

**First run:**
```bash
./start.sh
```

**Then:**
1. Open http://localhost:5173 in your browser
2. Click **"Login with GitHub"**
3. You'll see a device code (e.g., `ABCD-1234`)
4. Click the link or visit https://github.com/login/device
5. Enter the code and authorize
6. Token is saved automatically to `~/.llm-council-github-token.json`

**Subsequent runs:**
- Just run `./start.sh` - authentication is automatic!

### 3. Configure Models (Optional)

Edit `backend/config.py` to customize your council:

```python
COUNCIL_MODELS = [
    {"provider": "github", "model": "claude-sonnet-4.5"},     # Anthropic Claude
    {"provider": "github", "model": "gemini-2.5-pro"},        # Google Gemini
    {"provider": "github", "model": "gpt-5"},                 # OpenAI GPT-5
    {"provider": "github", "model": "grok-code-fast-1"},      # xAI Grok
]

CHAIRMAN_MODEL = {"provider": "github", "model": "claude-sonnet-4.5"}
```

**Available GitHub Copilot Models:**

| Model | Provider | Best For |
|-------|----------|----------|
| `gpt-5` | OpenAI | Latest GPT capabilities |
| `gpt-4.1` | OpenAI | Reliable, accurate |
| `claude-sonnet-4.5` | Anthropic | Reasoning, writing |
| `claude-haiku-4.5` | Anthropic | Fast responses |
| `gemini-2.5-pro` | Google | Multimodal, factual |
| `grok-code-fast-1` | xAI | Code generation |

### 🔍 How to Check All Available Models

**Method 1: Python Script (Recommended)**
```bash
python list_models.py
```

This will show a categorized list of all 23+ models with examples of how to configure them.

**Method 2: API Endpoint**
```bash
# Start the backend first
./start.sh

# Then in another terminal:
curl http://localhost:8001/api/github/models
```

**Method 3: Browser**

Visit http://localhost:8001/api/github/models after starting the backend.

The models list updates as GitHub adds new models, so check regularly for new options!

## 🎮 Usage

### Start the Application

**Easiest way:**
```bash
./start.sh
```

**Manual start (two terminals):**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open **http://localhost:5173** in your browser.

### Stop the Application

Press `Ctrl+C` in the terminal running `start.sh`, or stop both terminal processes.

## 🎨 UI Features

### Stage 1: Individual Responses
- **Color-coded model badges** - Each AI has a unique color
- **Tab-based navigation** - Easily compare responses
- **Professional cards** - Clean, modern design

### Stage 2: Peer Review & Voting
- **🏆 Podium Rankings** - See winners with gold/silver/bronze medals
- **📋 Voting Matrix** - Visual table showing exactly how each model ranked others
- **🔤 Response Key** - Clear legend mapping "Response A/B/C" to actual models
- **✅ Top Choice Highlighting** - #1 votes shown in green
- **📊 Individual Evaluations** - Click any model to read their full analysis

### Stage 3: Chairman's Decision
- **👔 Chairman Badge** - Clear indication of the synthesizing model
- **💡 Final Answer** - Highlighted in green for easy identification
- **📝 Reasoning** - Explanation of why this answer was chosen
- **ℹ️ Context Info** - Shows how the synthesis considered all inputs

## 🏗️ Architecture

### Backend (FastAPI)

```
backend/
├── main.py           # FastAPI server, API endpoints
├── config.py         # Model configuration
├── council.py        # 3-stage orchestration logic
├── github_auth.py    # OAuth device flow
├── github_models.py  # GitHub Copilot API client
├── provider.py       # Multi-provider abstraction
├── storage.py        # JSON-based conversation storage
└── openrouter.py     # OpenRouter API (optional)
```

**Key Features:**
- Async/await for parallel model queries
- Graceful degradation (continues if some models fail)
- Anonymous response labeling to prevent bias
- Persistent storage in `data/conversations/`

### Frontend (React + Vite)

```
frontend/src/
├── App.jsx                      # Main app orchestration
├── api.js                       # Backend API client
├── components/
│   ├── ChatInterface.jsx        # Main chat UI
│   ├── GitHubAuth.jsx          # OAuth login flow
│   ├── Sidebar.jsx             # Conversation list
│   ├── StageProgress.jsx       # Visual progress indicator
│   ├── Stage1.jsx              # Individual responses view
│   ├── Stage2.jsx              # Voting matrix & rankings
│   └── Stage3.jsx              # Chairman's final answer
└── index.css                    # Global styles
```

## 🔧 Advanced Configuration

### Using OpenRouter (Alternative)

If you prefer OpenRouter over GitHub Copilot:

1. Get an API key at [openrouter.ai](https://openrouter.ai/)
2. Create `.env` file:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-...
   ```
3. Update `backend/config.py`:
   ```python
   COUNCIL_MODELS = [
       {"provider": "openrouter", "model": "anthropic/claude-sonnet-4.5"},
       {"provider": "openrouter", "model": "google/gemini-2.5-pro"},
       {"provider": "openrouter", "model": "openai/gpt-5"},
       {"provider": "openrouter", "model": "x-ai/grok-4"},
   ]
   ```

### Mixing Providers

You can use both GitHub Copilot and OpenRouter models together:

```python
COUNCIL_MODELS = [
    {"provider": "github", "model": "claude-sonnet-4.5"},      # Free via Copilot
    {"provider": "github", "model": "gpt-5"},                  # Free via Copilot
    {"provider": "openrouter", "model": "meta-llama/llama-4"}, # Paid via OpenRouter
]
```

## 📊 How It Works: The Anonymous Voting System

### Stage 2 in Detail

When models vote, they receive prompts like this:

```
Question: What are the benefits of exercise?

Response A:
[Claude's answer - but models don't know it's Claude!]

Response B:
[Gemini's answer - but models don't know it's Gemini!]

Response C:
[GPT's answer - but models don't know it's GPT!]

Rank these responses from best to worst...
```

**The Magic:**
- Backend creates mapping: `{"Response A": "claude-sonnet-4.5", "Response B": "gemini-2.5-pro", ...}`
- This mapping is **hidden** from the voting models
- Only the UI (after voting) and Chairman (for synthesis) see the true identities
- Each model votes on "Response A/B/C/D" without knowing who wrote what

**Result:** Pure, unbiased quality assessment! 🎯

## 🤝 Contributing

This is a "vibe code" project - feel free to fork and modify as you like! Some ideas:
- Add more providers (Anthropic API, OpenAI API direct)
- Implement streaming responses
- Add cost tracking
- Export deliberations to PDF/markdown
- Custom ranking criteria beyond "accuracy and insight"

## 📜 License

MIT License - Use freely, modify as you wish!

## 🙏 Credits

**Original Project:** [LLM Council](https://github.com/karpathy/llm-council) by [@karpathy](https://x.com/karpathy)

Created as a fun Saturday hack for [reading books with LLMs](https://x.com/karpathy/status/1990577951671509438). The original used OpenRouter for API access.

**This Fork's Additions:**
- GitHub Copilot integration for free model access
- OAuth device flow authentication
- Enhanced UI with voting matrix and response key visualization
- Multi-provider architecture supporting both GitHub Copilot and OpenRouter
- Student-friendly: no additional API costs if you already have Copilot!

**Why I forked it:** As a student with GitHub Copilot access, I wanted to explore multiple LLMs without paying for OpenRouter credits. This fork lets students and developers with Copilot use the same powerful deliberation system for free! 🎓

---

**Built with:** FastAPI, React, Vite, GitHub Copilot API, and a healthy dose of AI democracy! 🗳️✨
