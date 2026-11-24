# SDK Integration Notes

## 1. Overview

This document describes how the existing Training Center RAG Chatbot can be prepared for integration with an external SDK or application.

The current implementation provides reusable RAG functionality and a FastAPI REST API. The goal of future integration is to reuse the existing components rather than rebuild the chatbot.

**Integration Status:** FastAPI is implemented and tested. No specific external SDK has been selected or integrated yet.

## 2. Reusable Components

The following components are available for reuse:

| Component | File | Responsibility |
|---|---|---|
| Main RAG Function | `src/retrieval/rag_chatbot.py` | Processes user questions and returns answers, sources, and support status. |
| Retriever | `src/retrieval/retrieve.py` | Retrieves relevant document chunks from the persisted index. |
| Reranker | `src/retrieval/reranker.py` | Reorders retrieved results based on relevance. |
| Evidence Validator | `src/retrieval/evidence_validator.py` | Validates whether retrieved evidence supports the question. |
| FastAPI Service | `src/api/main.py` | Exposes the chatbot through REST API endpoints. |

### Main Entry Point

The main reusable function is:

`ask_question(question)`

It accepts a user question and returns a dictionary containing:

- `answer`: The generated answer.
- `sources`: The supporting document sources.
- `supported`: Indicates whether the response is considered supported.

Example response:

```json
{
  "answer": "The training center offers several courses.",
  "sources": ["faq.md"],
  "supported": true
}
```

## 3. Current API Endpoints

The existing FastAPI service provides:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks whether the API is running. |
| POST | `/chat` | Accepts a question and returns the RAG response. |

Example request:

```json
{
  "question": "What courses does the training center offer?"
}
```

The API can be started using:

```bash
python -m uvicorn src.api.main:app --reload
```

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## 4. Required Changes for Future SDK Integration

The following changes may be required depending on the target SDK:

1. **SDK Compatibility:** Identify the target SDK and adapt the existing API or callable function to its expected interface.
2. **Input and Output Mapping:** Map the SDK input format to the `question` parameter and return the answer, sources, and support status in the required format.
3. **Configuration Management:** Ensure API keys, model settings, and environment variables are configured securely.
4. **Dependency Management:** Verify that SDK dependencies are compatible with the existing Python environment.
5. **Model Initialization:** Review model initialization and resource reuse to avoid unnecessary repeated loading.
6. **Error Handling:** Provide appropriate error responses when retrieval, model inference, or external services fail.
7. **Testing:** Test supported, unsupported, greeting, and multi-document questions after integration.

## 5. Current Limitations

- The current embedding model is primarily English-focused, which may affect Arabic-language retrieval.
- Multi-document questions may not always retrieve sufficient evidence.
- Retrieval and validation thresholds are empirically configured.
- The current evaluation dataset has limited coverage.

These limitations should be considered during future integration and improvement.

## 6. Integration Considerations

- Reuse the existing RAG pipeline instead of implementing a new one.
- Keep retrieval and evidence validation separate from the API layer.
- Preserve source information in the SDK response.
- Maintain the `supported` field to distinguish supported answers from unsupported questions.
- Avoid exposing API keys or sensitive configuration values.
- Keep the Streamlit interface and API layer independent while reusing the same RAG logic.

## 7. Conclusion

The project provides a reusable RAG pipeline, a Streamlit interface, and a tested FastAPI interface.

The main integration work will involve adapting the existing interface to the target SDK, configuring dependencies, and validating the chatbot's behavior after integration.

**Note:** No specific external SDK has been selected or integrated yet. The required changes will depend on the SDK chosen.