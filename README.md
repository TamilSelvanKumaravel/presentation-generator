# AI Presentation Generator

A professional Python-based application that generates PowerPoint presentations using Large Language Models (LLMs).

## Features

- 🤖 Support for multiple LLM providers (OpenAI, Ollama)
- 📊 Generate professional PPTX presentations
- 🎨 Multiple presentation styles (Professional, Casual, Academic)
- 🌍 Multi-language support
- 🚀 FastAPI REST API
- 📝 Comprehensive logging
- ✅ Type-safe with Pydantic

## Prerequisites

- Python 3.10 or higher
- pip
- (Optional) Ollama for local LLM support

## Installation

### 1. Clone and Setup

```bash
# Navigate to project directory
cd D:\presentation-generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
copy env.example .env

# Edit .env with your settings
# For OpenAI:
OPENAI_API_KEY=your_key_here
LLM_PROVIDER=openai

# For Ollama (local):
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

### 3. Setup Ollama (Optional - for local LLMs)

```bash
# Install Ollama from https://ollama.ai
# Pull a model
ollama pull llama2
# or
ollama pull mistral
```

## Usage

### Start the Server

```bash
python -m src.main
```

Or using uvicorn directly:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Generate Presentation

```bash
curl -X POST "http://localhost:8000/api/v1/presentation/generate" ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\": \"Introduction to Machine Learning\", \"number_of_slides\": 5, \"format\": \"pptx\", \"style\": \"professional\"}"
```

### Python Example

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/v1/presentation/generate",
    json={
        "topic": "Climate Change Solutions",
        "number_of_slides": 7,
        "format": "pptx",
        "style": "professional"
    }
)

result = response.json()
print(result)
```

## Project Structure

```
presentation-generator/
├── src/
│   ├── api/          # API routes
│   ├── config/       # Configuration
│   ├── models/       # Pydantic models
│   ├── services/     # Business logic
│   └── utils/        # Utilities
├── tests/            # Tests
└── presentations/    # Generated files
```

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## License

MIT

