# Training Center RAG Chatbot

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) chatbot designed to answer questions about a training center using its internal documents.

The chatbot retrieves relevant information from a knowledge base, validates the retrieved evidence, and uses a Large Language Model (LLM) to generate answers grounded in the available context.

When the documents do not contain sufficient information, the chatbot responds:

> I don't have enough information to answer this question.

The project provides two ways to interact with the chatbot:

- A Streamlit-based user interface.
- A FastAPI REST API for external application integration.

Both interfaces use the same underlying RAG pipeline.

## Features

- Answers questions using the training center's internal documents.
- Retrieves relevant information using semantic similarity.
- Filters weak retrieval results using a similarity threshold.
- Re-ranks retrieved documents using a Cross-Encoder.
- Applies a Relevance Gate to filter low-relevance results.
- Validates evidence using Natural Language Inference (NLI).
- Performs numeric claim grounding to reduce unsupported numerical answers.
- Supports partial answers when only some parts of a question are supported.
- Detects greeting messages and responds separately.
- Returns source documents associated with supported evidence.
- Provides a Streamlit-based chat interface.
- Exposes the existing RAG functionality through a FastAPI REST API.

## Technologies Used

- Python
- LlamaIndex
- Streamlit
- FastAPI
- Uvicorn
- Pydantic
- Groq API
- Hugging Face Transformers
- Sentence Transformers
- Cross-Encoder Reranking
- Natural Language Inference (NLI)
- BAAI/bge-small-en-v1.5
- python-dotenv

## Project Structure

```text
training-center-rag/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── retrieval-evaluation.md
├── rag-answer-evaluation.md
│
├── data/
│   ├── about.md
│   ├── ai-course.md
│   ├── data-analysis.md
│   ├── faq.md
│   ├── registration.md
│   └── web-development.md
│
└── src/
    ├── api/
    │   ├── __init__.py
    │   └── main.py
    │
    ├── ingestion/
    │   ├── build_index.py
    │   ├── load_doc.py
    │   ├── text_chunker.py
    │   └── storage/
    │
    └── retrieval/
        ├── retrieve.py
        ├── reranker.py
        ├── evidence_validator.py
        └── rag_chatbot.py
```

**Note:** The `storage/` directory contains the generated vector index. It is created when the index is built.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd training-center-rag
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file from the example file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual API key.

**Important:** Never upload your `.env` file or API key to GitHub. The `.env` file is excluded through `.gitignore`, while `.env.example` provides the required variable name without exposing credentials.

### 5. Build the Vector Index

From the project root directory, run:

```powershell
python src/ingestion/build_index.py
```

This process:

1. Loads the training center documents from the `data/` directory.
2. Splits the documents into smaller text chunks.
3. Generates embeddings using the configured Hugging Face embedding model.
4. Creates the vector index.
5. Saves the index in `src/ingestion/storage/`.

Run this command again whenever the source documents change.

### 6. Run the Streamlit Application

```powershell
python -m streamlit run app.py
```

The application will open in your browser.

## FastAPI Service

The project also provides a FastAPI service that allows external applications to interact with the existing RAG chatbot.

The API reuses the existing `ask_question()` function from the RAG pipeline. It does not implement a separate retrieval or evidence-validation pipeline.

### Run the API

From the project root directory, run:

```powershell
python -m uvicorn src.api.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

### Interactive API Documentation

Open the following URL to access the Swagger UI documentation:

`http://127.0.0.1:8000/docs`

### Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks whether the API is running. |
| POST | `/chat` | Sends a question to the existing RAG chatbot. |

### Health Check Example

**GET `/health`**

Example response:

```json
{
  "status": "healthy"
}
```

### Chat Request Example

**POST `/chat`**

Request body:

```json
{
  "question": "What courses does the training center offer?"
}
```

Example response:

```json
{
  "answer": "The training center offers the following courses...",
  "sources": ["faq.md"],
  "supported": true
}
```

### Response Fields

- `answer`: The chatbot's generated answer.
- `sources`: The source documents associated with the supported evidence.
- `supported`: Indicates whether the response is considered supported. For factual questions, it means at least one factual part was supported by the available evidence. Greeting responses are handled separately.

Invalid requests are handled through Pydantic validation. Unexpected processing errors return an HTTP 500 response.

## RAG Workflow

The chatbot follows a multi-stage retrieval and evidence-validation pipeline:

1. The user submits a question through the Streamlit interface or FastAPI endpoint.
2. Greeting detection identifies simple greeting messages and handles them separately.
3. Complex questions are decomposed into smaller factual hypotheses.
4. The question is converted into an embedding.
5. The retriever searches the persisted vector index and retrieves the top 3 results.
6. Similarity filtering removes results below the configured threshold.
7. A Cross-Encoder re-ranks the retrieved results based on relevance to the question.
8. The Relevance Gate filters results using a reranker score threshold.
9. NLI validates whether the retrieved evidence supports each hypothesis.
10. Numeric grounding checks numerical claims against the available evidence.
11. Supported evidence is collected and duplicate sources are removed.
12. The chatbot generates an answer using the validated context.
13. The response includes the answer, source documents, and support status.

**Note:** The pipeline may process evidence across multiple hypotheses. The steps above describe its logical workflow.

## System Configuration

| Component | Configuration |
|---|---|
| Embedding Model | BAAI/bge-small-en-v1.5 |
| LLM Provider | Groq |
| LLM Model | openai/gpt-oss-120b |
| Retrieval Method | Semantic Similarity |
| Retrieval Top K | 3 |
| Similarity Threshold | 0.6 |
| Reranker | BAAI/bge-reranker-base |
| Relevance Gate Threshold | 0.1 |
| NLI Model | cross-encoder/nli-deberta-v3-base |
| NLI Acceptance Threshold | 0.8 |
| User Interface | Streamlit |
| API Framework | FastAPI |
| API Server | Uvicorn |

**Note:** Similarity and reranker thresholds are empirical values based on the current testing. They may require recalibration when the dataset or models change.

## Evaluation

The chatbot was evaluated using manually prepared test questions covering:

- Normal questions.
- Paraphrased questions.
- Unsupported questions.
- Greeting messages.
- Partially supported questions.
- Questions requiring information from multiple documents.
- Out-of-domain questions.
- Questions containing numerical claims.

The evaluation results are documented in:

- `retrieval-evaluation.md`
- `rag-answer-evaluation.md`

The chatbot was also tested through the FastAPI service. The tests included:

- A supported question.
- An unsupported question.
- A greeting message.
- An empty question to verify request validation.
- A health check using `GET /health`.

The API successfully returned HTTP 200 for the tested health check and greeting request. The greeting response contained the expected `answer`, `sources`, and `supported` fields.

A final regression test identified a limitation in handling questions requiring information from multiple documents. The chatbot could not answer a question combining information about the available courses and the training center's main mission. This behavior is documented for future improvement.

## Limitations

- Retrieval is limited to the top 3 results, which may not capture all relevant information in complex questions.
- Similarity and reranker thresholds are empirical and may not generalize to every query.
- NLI validation does not guarantee complete protection against semantic hallucinations.
- Question decomposition may omit some details in complex questions.
- Numeric grounding currently focuses on numerical values represented as digits.
- The evaluation dataset is still limited.
- The current embedding model is primarily English-focused, which may reduce Arabic-language retrieval reliability.
- Multi-document questions may fail when the required evidence is not retrieved or validated across multiple documents.

## Future Improvements

- Expand the evaluation dataset with more diverse questions.
- Optimize similarity and reranker thresholds using a larger evaluation set.
- Improve retrieval for questions requiring information from multiple documents.
- Improve question decomposition for complex queries.
- Extend numeric grounding to cover written-out numbers and numerical relationships.
- Explore multilingual embedding models to improve Arabic-language retrieval.
- Improve the chatbot interface and user experience.
- Expand API testing and integration with external applications.

## Reliability Improvements

### Retrieval and Relevance

- Semantic retrieval using BAAI/bge-small-en-v1.5.
- Similarity filtering with a threshold of 0.6.
- Cross-Encoder reranking.
- Relevance Gate before evidence validation.

### Evidence Validation

- NLI-based evidence validation.
- Numeric claim grounding.
- Partial answers for partially supported questions.

### Source Management

- Only evidence-supported sources are used in the final response.
- Duplicate evidence and source filenames are removed.

### Testing

- Supported questions.
- Unsupported questions.
- Partially supported questions.
- Multi-document questions.
- Out-of-domain questions.
- Greeting messages.
- Numerical claim validation.
- FastAPI endpoint testing.
- Health check endpoint testing.
- Streamlit startup testing in a clean virtual environment.

## Legacy Files

The repository may contain older TypeScript files and Node.js configuration files from an earlier implementation.

These files are not required to install or run the current Python chatbot.

The current application uses Python, Streamlit, FastAPI, and LlamaIndex. The legacy TypeScript files can be reviewed separately before removal.

## SDK Integration

No specific external SDK has been selected or integrated into the current implementation.

The FastAPI service provides an HTTP interface that can be used as an integration point for future applications.

## Author

Developed as a Retrieval-Augmented Generation (RAG) chatbot project for a training center.