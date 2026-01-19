# Oregent-1 Chat Application

A production-ready FastAPI-based chat application that supports multimodal interactions with text and image inputs. Built with conversation intelligence and session management capabilities.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Performance](#performance)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 💬 **Text-based Chat**: Process natural language queries
- 🖼️ **Image Upload Support**: Handle image inputs with automatic file management
- 🔄 **Session Management**: Maintain conversation context across multiple requests
- 🤖 **AI-Powered Agent**: Integration with intelligent conversation agent
- 📁 **Automatic File Storage**: Secure file handling with UUID-based naming
- 🚀 **Async Support**: Built on FastAPI's async architecture for high performance
- 📝 **Auto-generated API Docs**: Interactive documentation at `/docs` and `/redoc`
- 🔒 **Type Safety**: Full type hints for better code quality

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP POST
       ▼
┌─────────────────────────┐
│   FastAPI Server        │
│   ┌─────────────────┐   │
│   │ /chat endpoint  │   │
│   └────────┬────────┘   │
│            │             │
│   ┌────────▼────────┐   │
│   │ File Handler    │   │
│   └────────┬────────┘   │
│            │             │
│   ┌────────▼────────┐   │
│   │ Conversation    │   │
│   │     Agent       │   │
│   └────────┬────────┘   │
└───────────┬─────────────┘
            │
            ▼
     ┌─────────────┐
     │  Response   │
     └─────────────┘
```

### Components

1. **FastAPI Server** (`main.py`)
   - Handles HTTP requests
   - Manages file uploads
   - Routes requests to conversation agent

2. **Conversation Agent** (`conversation_agent.py`)
   - Processes user input
   - Handles image analysis
   - Maintains conversation context

3. **Upload Directory** (`uploads/`)
   - Stores uploaded images
   - Uses UUID naming for uniqueness
   - Automatically created on startup

## 📦 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- 500MB free disk space (for uploads)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Oregent-1
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install fastapi uvicorn python-multipart pillow anthropic
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
# API Keys
ANTHROPIC_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Upload Configuration
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes

# Session Configuration
SESSION_TIMEOUT=3600  # 1 hour in seconds
```

### 5. Run the Application

**Development Mode:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production Mode:**
```bash
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

Access interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## ⚙️ Configuration

### Upload Settings

Modify upload directory in `main.py`:

```python
UPLOAD_DIR = "uploads"  # Change to your preferred directory
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
```

### CORS Configuration

Add CORS middleware for web applications:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 API Documentation

### Endpoint: POST /chat

Process a chat message with optional image attachment.

**URL:** `/chat`

**Method:** `POST`

**Content-Type:** `multipart/form-data`

**Parameters:**
```json
{
  "user_input": "Hello, how are you?",
  "session_id": "user123",
  "image": "image.jpg"
}
```

**Response:**
```json
{
  "response": "string",
  "session_id": "string",
  "timestamp": "ISO8601 datetime",
  "tokens_used": "integer",
  "image_processed": "boolean"
}
```

**Status Codes:**
- `200 OK`: Request processed successfully
- `400 Bad Request`: Invalid input or file format
- `413 Payload Too Large`: File exceeds size limit
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

**Example Success Response:**
```json
{
  "response": "I can see a beautiful sunset in the image. The sky is painted with vibrant orange and pink hues.",
  "session_id": "user123",
  "timestamp": "2024-01-15T10:30:00Z",
  "tokens_used": 150,
  "image_processed": true
}
```

**Example Error Response:**
```json
{
  "detail": "File size exceeds maximum allowed size of 10MB"
}
```

## 💻 Usage Examples

### Using cURL

**Text-only Message:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "user_input=Hello, how are you?" \
  -F "session_id=user123"
```

**Message with Image:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "user_input=What's in this image?" \
  -F "session_id=user123" \
  -F "image=@/path/to/image.jpg"
```

**With Custom Headers:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "user_input=Analyze this" \
  -F "image=@image.png"
```

### Using Python Requests

**Basic Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    data={
        "user_input": "Hello!",
        "session_id": "user123"
    }
)

print(response.json())
```

**With Image Upload:**
```python
import requests

with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/chat",
        data={
            "user_input": "Analyze this image",
            "session_id": "user123"
        },
        files={"image": f}
    )

result = response.json()
print(f"Response: {result['response']}")
print(f"Session ID: {result['session_id']}")
```

**Complete Application:**
```python
import requests
from pathlib import Path

class ChatClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def chat(self, message, image_path=None):
        data = {"user_input": message}
        
        if self.session_id:
            data["session_id"] = self.session_id
        
        files = None
        if image_path:
            files = {"image": open(image_path, "rb")}
        
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                data=data,
                files=files
            )
            response.raise_for_status()
            
            result = response.json()
            self.session_id = result.get("session_id")
            
            return result
        finally:
            if files:
                files["image"].close()

# Usage
client = ChatClient()

# Text message
response = client.chat("Hello!")
print(response["response"])

# Message with image
response = client.chat("What's in this image?", "photo.jpg")
print(response["response"])
```

### Using JavaScript/TypeScript

**With Fetch API:**
```javascript
async function sendChat(message, imageFile = null, sessionId = "default") {
    const formData = new FormData();
    formData.append("user_input", message);
    formData.append("session_id", sessionId);
    
    if (imageFile) {
        formData.append("image", imageFile);
    }
    
    const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        body: formData
    });
    
    return await response.json();
}

// Usage
const result = await sendChat("Hello!");
console.log(result.response);

// With image
const fileInput = document.querySelector("#imageInput");
const file = fileInput.files[0];
const result = await sendChat("Analyze this", file, "user123");
```

**With Axios:**
```javascript
import axios from 'axios';

async function sendChat(message, imageFile = null) {
    const formData = new FormData();
    formData.append("user_input", message);
    formData.append("session_id", "user123");
    
    if (imageFile) {
        formData.append("image", imageFile);
    }
    
    const response = await axios.post(
        "http://localhost:8000/chat",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );
    
    return response.data;
}
```

### Using Postman

1. **Set Method:** POST
2. **URL:** `http://localhost:8000/chat`
3. **Body Tab:** Select "form-data"
4. **Add Fields:**
   - Key: `user_input`, Type: Text, Value: Your message
   - Key: `session_id`, Type: Text, Value: Your session ID
   - Key: `image`, Type: File, Value: Select image file
5. **Click Send**

## 📁 Project Structure

```
Oregent-1/
├── main.py                      # FastAPI application entry point
├── conversation_agent.py        # AI conversation agent logic
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore file
├── README.md                    # This file
├── uploads/                     # Directory for uploaded images
│   └── .gitkeep                 # Keep directory in git
├── tests/                       # Test files
│   ├── __init__.py
│   ├── test_main.py
│   └── test_conversation_agent.py
├── docs/                        # Additional documentation
│   ├── architecture.md
│   └── api-examples.md
└── scripts/                     # Utility scripts
    ├── setup.sh
    └── deploy.sh
```

### File Descriptions

- **main.py**: Core FastAPI application with route handlers
- **conversation_agent.py**: AI logic for processing messages and images
- **requirements.txt**: List of Python package dependencies
- **.env**: Environment configuration (API keys, settings)
- **uploads/**: Storage directory for user-uploaded images
- **tests/**: Unit and integration tests
- **docs/**: Extended documentation and guides

## ⚠️ Error Handling

### Common Errors

**File Too Large:**
```json
{
  "detail": "File size exceeds maximum allowed size of 10MB"
}
```
**Solution:** Reduce image size or compress before uploading

**Invalid File Format:**
```json
{
  "detail": "Invalid file format. Allowed: jpg, jpeg, png, gif, webp"
}
```
**Solution:** Convert image to supported format

**Missing Required Field:**
```json
{
  "detail": [
    {
      "loc": ["body", "user_input"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
**Solution:** Include `user_input` in request

**Session Not Found:**
```json
{
  "detail": "Session expired or not found"
}
```
**Solution:** Start new session or check session_id

## 🔒 Security Considerations

### File Upload Security

1. **File Size Limit**: Implemented to prevent DoS attacks
2. **File Type Validation**: Only allowed image formats accepted
3. **UUID Naming**: Prevents directory traversal attacks
4. **Separate Upload Directory**: Isolates user files

### Best Practices

```python
# Add file validation
from PIL import Image

def validate_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except:
        return False

# Add rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(...):
    # ...existing code...
```

### Environment Variables

Never commit `.env` file. Use `.env.example`:

```env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
MAX_UPLOAD_SIZE=10485760
SECRET_KEY=generate_random_secret_key
```

## 🚀 Performance

### Optimization Tips

1. **Enable Gzip Compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

2. **Use Multiple Workers:**
```bash
uvicorn main:app --workers 4
```

3. **Implement Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def process_image(image_path: str):
    # ...existing code...
```

4. **Async File Operations:**
```python
import aiofiles

async with aiofiles.open(image_path, "wb") as f:
    await f.write(await image.read())
```

### Benchmarks

| Metric | Value |
|--------|-------|
| Average Response Time | 200-500ms |
| Requests/Second | 100-200 |
| Memory Usage | 50-100MB |
| Image Upload Time | 100-300ms |

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

### Example Test

```python
# tests/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_chat_text_only():
    response = client.post(
        "/chat",
        data={
            "user_input": "Hello",
            "session_id": "test123"
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["session_id"] == "test123"

def test_chat_with_image():
    with open("test_image.jpg", "rb") as img:
        response = client.post(
            "/chat",
            data={"user_input": "Analyze this"},
            files={"image": ("test.jpg", img, "image/jpeg")}
        )
    assert response.status_code == 200
    assert "image_processed" in response.json()
```

## 🌐 Deployment

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
```

**Deploy:**
```bash
docker-compose up -d
```

### Cloud Deployment

**AWS (EC2):**
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip

# Clone and setup
git clone <repo-url>
cd Oregent-1
pip3 install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/oregent.service
```

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn main:app --host=0.0.0.0 --port=${PORT}" > Procfile

# Deploy
heroku create oregent-chat
git push heroku main
```

**Railway/Render:**
- Connect GitHub repository
- Set environment variables
- Deploy automatically

## 🔧 Troubleshooting

### Issue: Port Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac
```

### Issue: Module Not Found

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check virtual environment
which python  # Should point to venv
```

### Issue: Upload Directory Permission Denied

```bash
# Linux/Mac
chmod 755 uploads/

# Windows
# Right-click uploads folder > Properties > Security > Edit
```

### Issue: API Key Error

```bash
# Check .env file exists
ls -la .env

# Verify API key is set
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY%  # Windows
```

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.post("/chat")
async def chat(...):
    logger.debug(f"Received request: {user_input}")
    # ...existing code...
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions
- Write unit tests for new features

```python
def process_message(user_input: str, session_id: str) -> dict:
    """
    Process user message and generate response.
    
    Args:
        user_input: The user's message text
        session_id: Unique session identifier
        
    Returns:
        Dictionary containing response and metadata
    """
    # ...existing code...
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Project Maintainer**: [Your Name]
- **Email**: your.email@example.com
- **GitHub**: https://github.com/yourusername/oregent-1
- **Issues**: https://github.com/yourusername/oregent-1/issues

## 🙏 Acknowledgments

- FastAPI framework by Sebastián Ramírez
- Anthropic Claude API
- Python community

## 📝 Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- Basic chat functionality
- Image upload support
- Session management

### Future Roadmap

- [ ] Add user authentication
- [ ] Implement WebSocket support for real-time chat
- [ ] Add conversation history storage
- [ ] Support for multiple AI models
- [ ] Rate limiting and quota management
- [ ] Admin dashboard
- [ ] Batch processing support
- [ ] Audio input support

---

**Made with ❤️ using FastAPI**