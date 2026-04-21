# AI Search Assistant

A fullstack AI-powered search assistant that allows users to query documents/data and receive intelligent, context-aware results using embeddings and vector search.

Live Demo: https://ai-search-assistant-gamma.vercel.app/

---

This project is still under active development and has some limitations:

- The assistant only answers based on a fixed set of indexed documents
- It does not yet perform general web search or real-time information retrieval
- Responses are limited to the content available in the current dataset
- No long-term memory or conversation history is implemented yet
- Ranking and retrieval quality can still be improved

## Overview

This project is a fullstack AI search application that combines:

-  FastAPI backend (Python)
-  React frontend
-  Vector-based search (FAISS)
-  Cloud deployment (Render + Vercel)

The system allows users to enter a query and receive relevant results from indexed data using semantic search.

---

## Architecture

Frontend (React)
↓
REST API (FastAPI)
↓
Embedding / Search Layer
↓
Vector Database (FAISS)

---

## Features

-  Semantic search using embeddings
-  Fast API response backend
-  Clean React UI for query input and results
-  Document/data ingestion pipeline
-  Fully deployed cloud architecture
-  Frontend–backend integration via REST API
-  Production deployment

---

##  Tech Stack

### Backend
- Python
- FastAPI
- FAISS (vector search)
- OpenAI embeddings (or similar)
- Uvicorn

### Frontend
- React (Create React App)
- JavaScript
- Fetch API

### Deployment
- Vercel (frontend)
- Render (backend)

---

## Project Structure

ai_search_assistant/
│
├── backend/
│ ├── api/
│ │ └── main.py
│ ├── core/
│ ├── services/
│ ├── data/
│ └── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── App.js
│ │ └── components/
│ ├── public/
│ └── .env
│
└── README.md


---

## How it works

1. User enters a query in the frontend
2. Frontend sends request to FastAPI backend
3. Backend converts query into embeddings
4. FAISS searches for similar vectors
5. Relevant results are returned to frontend
6. UI displays results to user

---

## API Endpoint

### POST `/search`

**Request:**
```json
{
  "query": "your search text"
}
```

**Response:**
```
{
  "results": [
    {
      "text": "...",
      "score": 0.89
    }
  ]
}
```

## Deployment
-  Backend (Render)
-  Hosted on Render cloud platform
-  Runs with: uvicorn api.main:app
-  Frontend (Vercel)
-  Hosted on Vercel
-  Connected to backend via environment variables

## Key Learnings
-  Building a fullstack AI system from scratch
-  Working with embeddings and vector search
-  Connecting frontend and backend in production
-  Deploying cloud applications (Vercel + Render)
-  Handling CORS and environment variables
-  Debugging fullstack issues in production

## relevant questions
The system performs best when users ask questions directly related to the indexed documents.
You can ask questions like:

-Explanations
“What is artificial intelligence?”
“How does machine learning work?”

-Healthcare & technology
“How is AI used in healthcare?”
“What are the benefits of digital health services?”

-Education & innovation
“How does education support innovation?”
“What fields are important for the future workforce?”

-Cybersecurity & digitalization
“Why is cybersecurity important?”

-General conceptual topics
“How is cooking both an art and a science?”
“What techniques are used in cooking?”

## author
Built by Marziyeh Khaleghi
Fullstack AI & Software Engineering Project
