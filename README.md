# Oregent-1 Chat Application

A simple FastAPI-based chat application that allows users to send text messages and upload images for analysis.

## 📋 Table of Contents

- [What This App Does](#what-this-app-does)
- [Product Search Agentic AI System](#product-search-agentic-ai-system)
  - [System Overview](#system-overview)
  - [Complete Architecture](#complete-architecture)
  - [Agent Components](#agent-components)
  - [How It All Works Together](#how-it-all-works-together)
  - [Data Flow](#data-flow)
  - [File-by-File Breakdown](#file-by-file-breakdown)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [API Endpoint](#api-endpoint)
- [File Structure](#file-structure)
- [Understanding the Code](#understanding-the-code)

## What This App Does

This application is a simple chat server built with FastAPI. It does three main things:

1. **Accepts text messages** - Users can send a message and get a response from an AI agent
2. **Handles image uploads** - Users can optionally attach an image with their message
3. **Manages conversations** - Each conversation can have a unique session ID to keep messages organized

## Product Search Agentic AI System

### System Overview

This application implements an **Agentic AI system** for product search and recommendation. Unlike simple chatbots, this system uses specialized AI agents that can:

- 🔍 **Search products** across e-commerce platforms
- 🤖 **Make decisions** about which tools to use
- 🧠 **Process images** to understand what users are looking for
- 💬 **Have conversations** while maintaining context
- 🎯 **Take actions** like searching APIs, analyzing data, and formatting responses

### Complete Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER LAYER                                     │
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │   Browser    │    │  Mobile App  │    │ API Client   │             │
│  │   (Swagger)  │    │              │    │  (curl/code) │             │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘             │
│         │                   │                    │                      │
│         └───────────────────┴────────────────────┘                      │
│                             │                                           │
│                    HTTP POST /chat                                      │
│              (text + optional image + session_id)                       │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      FASTAPI SERVER (main.py)                           │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │  1. Request Handler                                         │        │
│  │     - Receives: user_input, session_id, image (optional)   │        │
│  │     - Validates input                                       │        │
│  │     - Generates unique session_id if not provided          │        │
│  └────────────────────┬───────────────────────────────────────┘        │
│                       │                                                 │
│                       ▼                                                 │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │  2. Image Handler (if image exists)                        │        │
│  │     - Creates unique filename (UUID + original name)       │        │
│  │     - Saves to uploads/ folder                             │        │
│  │     - Stores file path                                     │        │
│  └────────────────────┬───────────────────────────────────────┘        │
│                       │                                                 │
│                       ▼                                                 │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │  3. Agent Caller                                            │        │
│  │     - Calls conversation_agent()                            │        │
│  │     - Passes: user_input, image_path (or None)             │        │
│  └────────────────────┬───────────────────────────────────────┘        │
└────────────────────────┼───────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              AGENTIC AI LAYER (conversation_agent.py)                   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │           Main Orchestrator Agent                         │          │
│  │  - Receives user input and optional image                │          │
│  │  - Decides which specialized agent to use                │          │
│  │  - Coordinates the workflow                              │          │
│  │  - Maintains conversation context                        │          │
│  └────────┬─────────────────────────────────────────────────┘          │
│           │                                                             │
│           ├─────────────┬─────────────┬─────────────┬─────────────┐   │
│           │             │             │             │             │   │
│           ▼             ▼             ▼             ▼             ▼   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌────────┐│
│  │   Image    │ │  Product   │ │   Search   │ │  Price   │ │ Review ││
│  │  Analysis  │ │ Extraction │ │   Engine   │ │ Compare  │ │ Analyst││
│  │   Agent    │ │   Agent    │ │   Agent    │ │  Agent   │ │ Agent  ││
│  └────────────┘ └────────────┘ └────────────┘ └──────────┘ └────────┘│
│       │              │              │              │            │      │
│       └──────────────┴──────────────┴──────────────┴────────────┘      │
│                                │                                        │
│                                ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │              Response Formatter                           │          │
│  │  - Combines results from all agents                      │          │
│  │  - Formats into user-friendly response                   │          │
│  │  - Returns: {"response": "...", "metadata": {...}}      │          │
│  └────────────────────────────────────────────────────────┬─┘          │
└─────────────────────────────────────────────────────────────┼───────────┘
                                                              │
                         ┌────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES LAYER                              │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Amazon     │  │    eBay      │  │  Google      │  │   Image    │ │
│  │   Product    │  │   Shopping   │  │   Shopping   │  │  Analysis  │ │
│  │   API        │  │     API      │  │     API      │  │    API     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                         │
                         │ Results aggregated
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      RESPONSE FLOW BACK                                 │
│                                                                          │
│  conversation_agent returns to main.py                                  │
│           │                                                             │
│           ▼                                                             │
│  main.py adds session_id to response                                   │
│           │                                                             │
│           ▼                                                             │
│  JSON response sent back to user                                       │
│           │                                                             │
│           ▼                                                             │
│  ┌─────────────────────────────────────┐                               │
│  │  {                                  │                               │
│  │    "response": "Found 5 products...",                               │
│  │    "session_id": "user123",         │                               │
│  │    "products": [...],               │                               │
│  │    "metadata": {...}                │                               │
│  │  }                                  │                               │
│  └─────────────────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Components

#### 1. **Main Orchestrator Agent** (`conversation_agent.py`)

**What it does:**
- Acts as the "brain" of the system
- Decides which specialized agent to activate
- Maintains conversation history
- Coordinates between different agents

**Example Flow:**
```python
User: "Find me a laptop under $1000"
↓
Orchestrator decides: Need Product Search Agent
↓
Product Search Agent activates
↓
Results returned and formatted
```

#### 2. **Image Analysis Agent**

**Purpose:** Understands what's in uploaded images

**Process:**
```
Image uploaded (e.g., photo of a shoe)
        ↓
1. Image saved to uploads/ folder
        ↓
2. Image Analysis Agent receives path
        ↓
3. AI analyzes image:
   - Identifies objects ("Nike running shoe")
   - Extracts colors ("red and white")
   - Detects text/brands
   - Determines style/category
        ↓
4. Returns structured data:
   {
     "detected_object": "athletic shoe",
     "brand": "Nike",
     "colors": ["red", "white"],
     "style": "running shoe"
   }
```

**Use Cases:**
- "Find products similar to this image"
- "What is this item?"
- "Compare prices for this product"

#### 3. **Product Extraction Agent**

**Purpose:** Extracts specific product details from text

**Process:**
```
User input: "I need wireless headphones with noise cancellation"
        ↓
Product Extraction Agent analyzes:
        ↓
Extracted Information:
{
  "product_type": "headphones",
  "features": ["wireless", "noise cancellation"],
  "category": "electronics",
  "subcategory": "audio"
}
```

#### 4. **Search Engine Agent**

**Purpose:** Queries external e-commerce APIs

**Workflow:**
```
                    Search Engine Agent
                            ↓
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   Amazon API          eBay API         Google Shopping
        │                   │                   │
        ↓                   ↓                   ↓
  5 Products          8 Products          3 Products
        │                   │                   │
        └───────────────────┴───────────────────┘
                            ↓
                    Aggregated Results
                      (16 products)
                            ↓
                    Filtered & Sorted
                            ↓
                    Top 10 Returned
```

**Search Parameters:**
- Keywords from user input
- Price range
- Category
- Ratings threshold
- Availability

#### 5. **Price Comparison Agent**

**Purpose:** Analyzes prices across platforms

**Process:**
```
Product: "iPhone 15 Pro"
        ↓
Finds same product on multiple sites
        ↓
┌─────────────┬─────────────┬─────────────┐
│   Amazon    │     eBay    │   Walmart   │
│   $999      │    $1,049   │    $979     │
└─────────────┴─────────────┴─────────────┘
        ↓
Recommends: Walmart ($979) - Best price!
        ↓
Also shows: Price history, deals, shipping costs
```

#### 6. **Review Analysis Agent**

**Purpose:** Summarizes and analyzes product reviews

**Process:**
```
Collects reviews from multiple sources
        ↓
Analyzes sentiment (positive/negative)
        ↓
Extracts common themes:
  ✓ Pros: Battery life, Camera quality
  ✗ Cons: Expensive, Heavy
        ↓
Calculates overall score
        ↓
Returns summary
```

### How It All Works Together

#### **Example 1: Text-Only Search**

```
User → "Find gaming laptops under $1500"
  ↓
main.py receives request
  ↓
conversation_agent.py activated
  ↓
Main Orchestrator analyzes request:
  - Detects: product search query
  - Identifies: price constraint
  - Category: electronics/laptops
  ↓
Activates Product Extraction Agent
  ↓ 
Extracts:
  {
    "product": "gaming laptop",
    "max_price": 1500,
    "category": "computers"
  }
  ↓
Activates Search Engine Agent
  ↓
Searches 3 e-commerce APIs in parallel
  ↓
Returns 25 results
  ↓
Price Comparison Agent filters:
  - Only laptops ≤ $1500
  - Sorts by: rating, reviews, price
  ↓
Review Analysis Agent summarizes top 5
  ↓
Response formatted:
  "Found 5 gaming laptops under $1500:
   1. ASUS ROG - $1,299 ⭐4.5/5
      Pros: Great GPU, Fast refresh rate
   2. Dell G15 - $1,199 ⭐4.3/5
      Pros: Good value, Solid build
   ..."
  ↓
Returned to user via main.py
```

#### **Example 2: Image-Based Search**

```
User uploads image of a watch + "Find similar watches"
  ↓
main.py receives image file
  ↓
Image saved: uploads/abc123_watch.jpg
  ↓
conversation_agent.py activated with image_path
  ↓
Main Orchestrator detects image + text query
  ↓
Activates Image Analysis Agent
  ↓
Image Analysis Agent processes image:
  ↓
Detects:
  {
    "object": "wristwatch",
    "style": "sports/chronograph",
    "brand": "Casio G-Shock",
    "color": "black",
    "features": ["digital display", "rubber strap"]
  }
  ↓
Activates Product Extraction Agent
  ↓
Combines image data + user text:
  Search query: "Casio G-Shock style sports watch black"
  ↓
Activates Search Engine Agent
  ↓
Searches for similar products
  ↓
Returns matching watches
  ↓
Price Comparison sorts by similarity + price
  ↓
Response:
  "Found watches similar to your image:
   1. Casio G-Shock GA2100 - $99
   2. Similar style from Timex - $79
   ..."
  ↓
Returned to user
```

#### **Example 3: Complex Multi-Turn Conversation**

```
Turn 1:
User → "I need running shoes"
  ↓
Agent searches, returns 10 options
  ↓
Response: "Here are 10 running shoes..."

Turn 2: (Same session_id)
User → "Show me only Nike ones under $100"
  ↓
Orchestrator uses conversation history
  ↓
Knows context: already searched running shoes
  ↓
Filters previous results:
  - Brand: Nike
  - Price: < $100
  ↓
Response: "From the previous results, 3 Nike shoes under $100..."

Turn 3:
User uploads image → "Which one looks like this?"
  ↓
Image Analysis Agent + Previous context
  ↓
Compares uploaded image to the 3 Nike shoes
  ↓
Response: "The Nike Air Zoom Pegasus matches your image most closely..."
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DETAILED DATA FLOW                           │
└─────────────────────────────────────────────────────────────────┘

Step 1: User Input Capture
┌──────────────────────────────────────┐
│  User sends:                         │
│  {                                   │
│    "user_input": "Find red shoes",   │
│    "session_id": "user123",          │
│    "image": <file object>            │
│  }                                   │
└────────────────┬─────────────────────┘
                 │
                 ▼
Step 2: FastAPI Processing (main.py)
┌──────────────────────────────────────┐
│  if image exists:                    │
│    filename = uuid4() + image.name   │
│    path = f"uploads/{filename}"      │
│    save_image(path)                  │
│                                      │
│  image_path = path or None           │
└────────────────┬─────────────────────┘
                 │
                 ▼
Step 3: Agent Invocation
┌──────────────────────────────────────┐
│  response = conversation_agent(      │
│    user_input="Find red shoes",      │
│    image_path="uploads/abc.jpg"      │
│  )                                   │
└────────────────┬─────────────────────┘
                 │
                 ▼
Step 4: Agent Processing
┌──────────────────────────────────────────────────────┐
│  Orchestrator receives input                         │
│          ↓                                           │
│  Analyzes: "Find red shoes" + image                 │
│          ↓                                           │
│  Decision Tree:                                      │
│  - Has image? YES → Activate Image Agent            │
│  - Is search query? YES → Activate Search Agent     │
│  - Needs comparison? NO                              │
│          ↓                                           │
│  Parallel Execution:                                 │
│  ┌─────────────────┐  ┌─────────────────┐          │
│  │ Image Analysis  │  │ Text Processing │          │
│  │ "red athletic   │  │ "shoes, red"    │          │
│  │  shoe detected" │  │                 │          │
│  └────────┬────────┘  └────────┬────────┘          │
│           └──────────┬──────────┘                   │
│                      ▼                               │
│           Combined Query Built:                      │
│           "red athletic shoes"                       │
│                      ↓                               │
│           Search Engine Agent                        │
│                      ↓                               │
│           API Calls (Amazon, eBay, etc.)            │
│                      ↓                               │
│           Results Aggregated                         │
│                      ↓                               │
│           Filtered & Ranked                          │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
Step 5: Response Formation
┌──────────────────────────────────────┐
│  response_data = {                   │
│    "response": "Found 8 red shoes:", │
│    "products": [                     │
│      {                               │
│        "name": "Nike Air Max",       │
│        "price": "$120",              │
│        "rating": 4.5,                │
│        "url": "..."                  │
│      },                              │
│      ...                             │
│    ],                                │
│    "metadata": {                     │
│      "search_time": "0.8s",          │
│      "sources": 3                    │
│    }                                 │
│  }                                   │
└────────────────┬─────────────────────┘
                 │
                 ▼
Step 6: Final Response (main.py)
┌──────────────────────────────────────┐
│  response_data["session_id"] =       │
│    "user123"                         │
│                                      │
│  return JSONResponse(response_data)  │
└────────────────┬─────────────────────┘
                 │
                 ▼
Step 7: User Receives
┌──────────────────────────────────────┐
│  {                                   │
│    "response": "Found 8 red shoes:", │
│    "products": [...],                │
│    "metadata": {...},                │
│    "session_id": "user123"           │
│  }                                   │
└──────────────────────────────────────┘
```

### File-by-File Breakdown

#### **main.py** - The Gateway

```
Purpose: HTTP server that handles all incoming requests

Key Functions:
├─ app = FastAPI()
│  └─ Creates the web server
│
├─ @app.post("/chat")
│  └─ The main endpoint
│     │
│     ├─ Receives: user_input, session_id, image
│     │
│     ├─ If image exists:
│     │  ├─ Generate UUID filename
│     │  ├─ Save to uploads/
│     │  └─ Store path
│     │
│     ├─ Call conversation_agent()
│     │  └─ Pass user_input + image_path
│     │
│     ├─ Receive response from agent
│     │
│     ├─ Add session_id to response
│     │
│     └─ Return JSON response
│
└─ File Management:
   └─ Creates "uploads/" folder on startup

Flow:
  Request → Validate → Save Image → Call Agent → Format → Response
```

#### **conversation_agent.py** - The AI Brain

```
Purpose: Contains all AI agent logic and coordination

Structure:
├─ conversation_agent(user_input, image_path=None)
│  │
│  ├─ Main Orchestrator
│  │  ├─ Analyzes user input
│  │  ├─ Determines intent
│  │  ├─ Decides which agents to activate
│  │  └─ Coordinates workflow
│  │
│  ├─ Agent Functions:
│  │  │
│  │  ├─ analyze_image(image_path)
│  │  │  └─ Processes image, returns object details
│  │  │
│  │  ├─ extract_product_info(text)
│  │  │  └─ Parses text for product details
│  │  │
│  │  ├─ search_products(query, filters)
│  │  │  └─ Calls external APIs, aggregates results
│  │  │
│  │  ├─ compare_prices(product_list)
│  │  │  └─ Analyzes prices across platforms
│  │  │
│  │  └─ analyze_reviews(product_id)
│  │     └─ Summarizes customer reviews
│  │
│  └─ Response Builder
│     ├─ Combines results from all agents
│     ├─ Formats user-friendly response
│     └─ Returns dictionary
│
└─ Helper Functions:
   ├─ format_results()
   ├─ rank_products()
   └─ maintain_context()

Agent Decision Logic:
┌─────────────────────────────────────┐
│ IF user_input contains:             │
│   - "find", "search" → Search Agent │
│   - image_path exists → Image Agent │
│   - "compare", "price" → Price Agent│
│   - "reviews" → Review Agent        │
│                                     │
│ Can activate multiple agents        │
│ simultaneously for complex queries  │
└─────────────────────────────────────┘
```

#### **uploads/** - Storage Directory

```
Purpose: Stores all uploaded images

Structure:
uploads/
  ├─ <uuid>_image1.jpg     ← User uploaded "image1.jpg"
  ├─ <uuid>_photo.png      ← User uploaded "photo.png"
  ├─ <uuid>_product.webp   ← User uploaded "product.webp"
  └─ ...

Naming Convention:
  <randomly-generated-uuid>_<original-filename>

Example:
  550e8400-e29b-41d4-a716-446655440000_sneakers.jpg

Why UUIDs?
  ✓ Prevents filename collisions
  ✓ Unique even if same filename uploaded twice
  ✓ Secure - hard to guess other images

Lifecycle:
  1. Image uploaded
  2. UUID generated
  3. File saved with UUID prefix
  4. Path passed to agent
  5. Agent reads and processes
  6. File remains for future reference
```

### Agent Interaction Patterns

#### **Pattern 1: Sequential Processing**

```
User query: "Find laptops"
     ↓
Extract Intent → Search Products → Format Response
     ↓                ↓                  ↓
  (Done)          (Done)             (Return)
```

#### **Pattern 2: Parallel Processing**

```
User query + Image: "Find similar products"
          ↓
    ┌─────┴─────┐
    ↓           ↓
Image Agent   Text Agent
    ↓           ↓
    └─────┬─────┘
          ↓
    Merge Results
          ↓
    Search Agent
          ↓
       Response
```

#### **Pattern 3: Iterative Refinement**

```
User: "Find shoes"
  ↓
Initial Search (100 results)
  ↓
User: "Only running shoes"
  ↓
Filter Previous Results (30 results)
  ↓
User: "Under $100"
  ↓
Further Filtering (8 results)
  ↓
Final Response
```

### Memory and Context Management

```
┌──────────────────────────────────────────────────┐
│         Session-Based Context Storage            │
├──────────────────────────────────────────────────┤
│                                                  │
│  session_id: "user123"                          │
│    ├─ conversation_history: [...]               │
│    ├─ last_search_results: [...]                │
│    ├─ user_preferences: {...}                   │
│    └─ context: {                                │
│         "current_category": "electronics",       │
│         "price_range": [0, 1000],               │
│         "filters_applied": [...]                │
│       }                                         │
│                                                  │
│  session_id: "user456"                          │
│    ├─ conversation_history: [...]               │
│    ├─ ...                                       │
│                                                  │
└──────────────────────────────────────────────────┘

How Context is Used:
  - Remembers previous searches
  - Understands follow-up questions
  - Applies cumulative filters
  - Personalizes recommendations
```

### Real-World Example: Complete Flow

```
🎯 Scenario: User wants to buy a camera

Turn 1: User → "I want to buy a camera for photography"
        ↓
   [Main Orchestrator Analysis]
        ↓
   Intent: product_search
   Category: electronics/cameras
   Purpose: photography
        ↓
   [Product Extraction Agent]
        ↓
   Extracted: {
     "product": "camera",
     "use_case": "photography",
     "category": "electronics"
   }
        ↓
   [Search Engine Agent] → Queries APIs
        ↓
   Found: 45 cameras
        ↓
   [Review Analysis Agent] → Filters by ratings
        ↓
   Top 10 cameras with good photography reviews
        ↓
   Response: "I found 10 great cameras for photography.
             Here are the top-rated ones:
             1. Canon EOS R6 - $2,499 ⭐4.8/5
             2. Sony A7 IV - $2,498 ⭐4.7/5
             ..."

Turn 2: User → "That's too expensive. Show me under $1000"
        ↓
   [Orchestrator + Context]
        ↓
   Remembers: Previous search was for cameras
   New constraint: price < $1000
        ↓
   [Price Comparison Agent]
        ↓
   Filters previous 45 results by price
        ↓
   Found: 12 cameras under $1,000
        ↓
   Response: "Here are 12 cameras under $1,000:
             1. Canon EOS M50 - $699 ⭐4.5/5
             2. Sony A6400 - $898 ⭐4.6/5
             ..."

Turn 3: User uploads image of Canon camera →
        "Is this one good?"
        ↓
   [Image Analysis Agent]
        ↓
   Detects: Canon EOS Rebel T7
        ↓
   [Search in previous results]
        ↓
   Found: Canon EOS Rebel T7 was #5 in list
        ↓
   [Review Analysis Agent]
        ↓
   Analyzes reviews for this specific model
        ↓
   Response: "Yes! The Canon EOS Rebel T7 ($549) is great
             for beginners. Reviews say:
             ✓ Easy to use
             ✓ Good image quality
             ✗ Limited video features
             ⭐ 4.4/5 from 2,341 reviews
             
             It's currently available at:
             - Amazon: $549
             - B&H Photo: $559
             - Best Buy: $579"
```

## System Architecture

Here's how the entire system works together:

```
┌──────────────────┐
│   User/Client    │
│  (Browser, App,  │
│   or Script)     │
└────────┬─────────┘
         │
         │ Sends message + optional image
         │ (HTTP POST request)
         │
         ▼
┌──────────────────────────────┐
│   FastAPI Server (main.py)   │
│                              │
│  1. Receives the request     │
│  2. Checks if image exists   │
│  3. Saves image to disk      │
│  4. Calls AI Agent           │
│  5. Adds session ID          │
│  6. Returns response         │
└──────────────┬───────────────┘
               │
               │ File path (if image)
               │
               ▼
      ┌────────────────┐
      │  uploads/      │
      │  folder        │
      │  (saved images)│
      └────────────────┘
               │
               │ User input + Image path
               │
               ▼
┌──────────────────────────────────┐
│ Conversation Agent               │
│ (conversation_agent.py)          │
│                                  │
│ 1. Receives user message         │
│ 2. Receives image path (if any)  │
│ 3. Analyzes/processes both       │
│ 4. Generates AI response         │
│ 5. Returns response text         │
└──────────────┬───────────────────┘
               │
               │ Response dictionary
               │
               ▼
┌──────────────────────────────┐
│   FastAPI Server (main.py)   │
│   Adds session_id to response│
└──────────────┬───────────────┘
               │
               │ JSON response
               │
               ▼
┌──────────────────┐
│   User/Client    │
│ Receives answer  │
└──────────────────┘
```

## Prerequisites

You need:
- Python 3.7 or higher installed on your computer
- pip (comes with Python)
- A terminal/command prompt to run commands

## Installation

### Step 1: Get the code
Open your terminal and run:
```bash
git clone <repository-url>
cd Oregent-1
```

### Step 2: Create a virtual environment (optional but recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install required packages
```bash
pip install fastapi uvicorn python-multipart
```

These packages do:
- **fastapi** - The web server framework
- **uvicorn** - The server that runs FastAPI
- **python-multipart** - Allows sending files with forms

## How to Run

Start the server with this command:
```bash
uvicorn main:app --reload
```

You should see something like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

The `--reload` flag makes the server restart when you edit the code. Remove it for production.

## How to Use

### Method 1: Using your browser (Swagger UI)

1. Open http://localhost:8000/docs in your browser
2. Click on the "POST /chat" section to expand it
3. Click "Try it out"
4. Fill in:
   - user_input: Your message
   - session_id: A name for this conversation (optional)
   - image: Upload an image (optional)
5. Click "Execute"

### Method 2: Using curl in terminal

**Send just a message:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "user_input=Hello, how are you?" \
  -F "session_id=myconversation"
```

**Send a message with an image:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -F "user_input=What's in this image?" \
  -F "session_id=myconversation" \
  -F "image=@/path/to/your/image.jpg"
```

### Method 3: Using Python

```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/chat",
    data={
        "user_input": "Hello!",
        "session_id": "user123"
    }
)

# Get the answer
result = response.json()
print(result["response"])
print(result["session_id"])
```

**With an image:**
```python
import requests

with open("myimage.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/chat",
        data={
            "user_input": "Analyze this image",
            "session_id": "user123"
        },
        files={"image": f}
    )

result = response.json()
print(result["response"])
```

## API Endpoint

### The `/chat` Endpoint

**What it does:** Accepts a message and optional image, returns an AI response

**How to call it:**
- URL: `http://localhost:8000/chat`
- Method: `POST`
- Type: `form-data` (can include files)

**What you send:**
```json
{
  "user_input": "Hello, who are you?",
  "session_id": "user123",
  "image": "image.jpg"
}
```

**What you get back:**
```json
{
  "response": "The AI's answer to your message",
  "session_id": "user123"
}
```

## File Structure

Here's what each file does:

```
Oregent-1/
├── main.py                      
│   └─ The main server file. This receives requests, saves images,
│      calls the AI agent, and sends back responses.
│
├── conversation_agent.py        
│   └─ The AI logic. This file has a function that processes your
│      message and image, and returns an answer.
│
├── uploads/                     
│   └─ A folder created automatically. All uploaded images are
│      saved here with unique names.
│
└── README.md                    
    └─ This file - instructions for using the app.
```

## Understanding the Code

### What happens step by step

**When you send a request:**

1. **The request arrives** at `main.py` in the `/chat` endpoint
   - Your message (user_input)
   - Your session ID (session_id) - optional
   - Your image (image) - optional

2. **If you uploaded an image:**
   - A unique filename is created using a UUID (a random ID)
   - The file is saved to the `uploads/` folder
   - Example: `uploads/550e8400-e29b-41d4-a716-446655440000_photo.jpg`

3. **The AI agent is called:**
   - Your message is sent to `conversation_agent()` function
   - The image path is also sent (or `None` if no image)
   - The agent processes everything and returns an answer

4. **The response is prepared:**
   - The answer from the agent is put into a dictionary
   - Your session ID is added to it
   - Everything is sent back to you as JSON

### main.py - What it does

```
1. Imports required libraries (FastAPI, uuid, os, conversation_agent)
2. Creates a FastAPI app
3. Creates an "uploads" folder if it doesn't exist
4. Defines a /chat endpoint that:
   a. Takes three parameters: user_input, session_id, and image
   b. If image exists:
      - Generates a unique filename with uuid
      - Saves the image to the uploads folder
      - Stores the file path
   c. Calls conversation_agent with the message and image path
   d. Adds the session_id to the response
   e. Returns the result
```

### conversation_agent.py - What it does

This file contains the logic that actually processes your message. It:

```
1. Receives your user_input (the message)
2. Receives image_path (path to uploaded image, or None)
3. Does some kind of processing:
   - Analyzes the text
   - If there's an image, analyzes that too
   - Uses AI to generate a response
4. Returns a dictionary with:
   - "response": The answer text
   - Any other information you want to include
```

### What happens with images

```
1. You send an image with your message
2. FastAPI saves it with a unique name in the uploads/ folder
3. The file path is passed to the conversation_agent
4. The agent can read and analyze the image
5. The agent uses the image analysis in its response
6. The image file stays saved in the uploads/ folder
```

## Common Questions

**Q: What's a session_id?**
A: It's just a name for your conversation. If you always use the same session_id, the agent can remember context from previous messages in that conversation.

**Q: Where are my images saved?**
A: In the `uploads/` folder in your project directory. Each image gets a unique name so they don't overwrite each other.

**Q: What formats can I upload?**
A: Depends on your conversation_agent.py file, but usually jpg, png, gif, webp work.

**Q: How do I stop the server?**
A: Press Ctrl+C in the terminal where it's running.

**Q: Can multiple people use this at the same time?**
A: Yes! By default it handles one request at a time. To handle more, run it with workers: `uvicorn main:app --workers 4`

---

**Made with ❤️ using FastAPI**