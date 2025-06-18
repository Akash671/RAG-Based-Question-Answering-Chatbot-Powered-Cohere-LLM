
# RAG-Based Job Matching System (Powered by Cohere LLM)

A scalable Retrieval-Augmented Generation (RAG) system designed for intelligent job-candidate matching. It uses Cohere’s language model and ChromaDB for semantic search over candidate resumes (PDF documents). The system is deployed via a FastAPI endpoint and is Docker-ready for seamless deployment.

## Project Structure

```
RAG-Based-Question-Answering-Chatbot-Powered-Cohere-LLM/
├── app/
│   ├── api.py
│   ├── extract_documents.py
│   ├── preprocess_documents.py
│   ├── create_embeddings.py
│   ├── store_embeddings.py
│   ├── query_engine.py
│   └── requirements.txt
├── Documents/
│   ├── file1.pdf
│   ├── file2.pdf
├── test/
│   └── test_query.py
├── Dockerfile
├── .env
├── README.md
└── .gitignore
```

## Features

- Stores multiple candidate resume/CV files in `.pdf` format
- Text extraction from PDF resumes
- Preprocessing with spaCy and NLTK
- Text chunking and embedding using SentenceTransformers
- Semantic retrieval using ChromaDB
- Question-answering with Cohere's LLM
- REST API built using FastAPI
- Fully containerized using Docker
- Streamlit-based UI for interactive querying

## Setup (Without Docker)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/RAG-Based-Question-Answering-Chatbot-Powered-Cohere-LLM.git
cd RAG-Based-Question-Answering-Chatbot-Powered-Cohere-LLM
```

### Step 2: Install Dependencies

```bash
cd app
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords
python -m spacy download en_core_web_sm
```

### Step 3: Set the Cohere API Key

Update the `.env` file in the root directory:

```
COHERE_API_KEY=your-cohere-api-key
```

(You can obtain your API key from Cohere’s website.)

### Step 4: Start the API Server

```bash
cd app
uvicorn api:app --reload
```

### Step 5: Run the Streamlit UI (Optional)

```bash
streamlit run chat_ui.py
```

Open the displayed local URL (e.g., http://localhost:8501) in your browser.

### Step 6: Test Using the UI

1. Navigate to the Streamlit app.
2. Enter a question in the input box (e.g., copy from `sample_user_input.txt`).
3. Click Submit to receive a response based on relevant information retrieved from the vector database.

## Run with Docker

### Step 1: Build the Docker Image

```bash
cd RAG-Based-Question-Answering-Chatbot-Powered-Cohere-LLM
docker build -t rag-chatbot .
```

### Step 2: Run the Docker Container

```bash
docker run -p 8000:8000 -e COHERE_API_KEY=your-api-key rag-chatbot
```

### Step 3: Test the API

- Visit the API docs at: http://localhost:8000/docs
- Or run the test script:

```bash
python test/test_query.py
```

## API Endpoint

**POST /ask**

Accepts a job description or user query and returns a synthesized answer with context.

### Example Request

```json
{
  "question": "Looking for a backend engineer experienced in AWS and Python."
}
```

### Example Response

```json
{
  "question": "Looking for a backend engineer experienced in AWS and Python.",
  "answer": "Based on retrieved profiles, candidates X and Y match the description...",
  "context_used": ["chunk1", "chunk2", "..."]
}
```

## Technologies Used

- Embedding Model: all-MiniLM-L6-v2 via SentenceTransformers
- Vector Store: ChromaDB (duckdb + parquet)
- LLM: Cohere command-r-plus
- Frameworks: FastAPI, LangChain, spaCy, NLTK
