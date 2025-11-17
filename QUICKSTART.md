# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Configure Environment

Edit the `.env` file and add your API key:

**For OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

**For Ollama (Local LLM):**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

> **Note:** If using Ollama, make sure Ollama is installed and running. Download from https://ollama.ai

### Step 2: Start the Server

```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate

# Start the server
python -m src.main
```

The server will start at: **http://localhost:8000**

### Step 3: Test the API

**Option A: Using Swagger UI (Recommended)**
- Open browser: http://localhost:8000/docs
- Click on `/api/v1/presentation/generate`
- Click "Try it out"
- Enter your request:
```json
{
  "topic": "Introduction to Machine Learning",
  "number_of_slides": 5,
  "format": "pptx",
  "style": "professional"
}
```
- Click "Execute"
- Download the generated PPTX file

**Option B: Using cURL**
```bash
curl -X POST "http://localhost:8000/api/v1/presentation/generate" ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\": \"AI in Healthcare\", \"number_of_slides\": 5, \"format\": \"pptx\"}"
```

**Option C: Using Python**
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
# Download URL will be in result["download_url"]
```

## 📁 Generated Files

All generated presentations are saved in the `presentations/` folder.

## 🔧 Troubleshooting

### Issue: "OpenAI API key not configured"
**Solution:** Make sure you've set `OPENAI_API_KEY` in your `.env` file.

### Issue: "Failed to connect to Ollama"
**Solution:** 
1. Make sure Ollama is installed and running
2. Test with: `ollama list`
3. Pull a model: `ollama pull llama2`

### Issue: Import errors
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 API Endpoints

- `GET /` - Root endpoint
- `GET /docs` - Swagger UI documentation
- `GET /api/v1/presentation/health` - Health check
- `POST /api/v1/presentation/generate` - Generate presentation
- `GET /api/v1/presentation/download/{filename}` - Download presentation

## 🎨 Presentation Styles

- `professional` - Formal, business-oriented
- `casual` - Conversational, friendly
- `academic` - Scholarly, research-based

## 📝 Example Request

```json
{
  "topic": "The Future of Artificial Intelligence",
  "number_of_slides": 10,
  "format": "pptx",
  "style": "professional",
  "language": "English",
  "include_images": false
}
```

Happy presenting! 🎉

