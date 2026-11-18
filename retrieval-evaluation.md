
# Retrieval Evaluation

## 1. Overview
This evaluation tests the retrieval performance of the Training Center RAG system using 10 questions.

The retriever uses:
- Embedding Model: BAAI/bge-small-en-v1.5
- Similarity Top K: 3
- Search Method: Semantic Search

## 2. Test Results

| # | Question | Expected Source | Result |
|---|---|---|---|
| 1 | How long does the AI course take? | ai-course.md | Correct |
| 2 | What are the prerequisites for the AI course? | ai-course.md | Correct |
| 3 | What courses does the training center offer? | faq.md | Correct |
| 4 | How can I register for a course? | registration.md | Correct |
| 5 | Does the Web Development course require programming experience? | faq.md | Correct |
| 6 | How long does the Data Analysis course take? | faq.md | Correct |
| 7 | What is the fee for the AI course? | ai-course.md | Correct |
| 8 | What will students learn in the AI course? | ai-course.md | Correct |
| 9 | What is the schedule for the AI course? | ai-course.md | Correct |
| 10 | Where is the training center located? | faq.md | Correct |

## 3. Evaluation Results

- Total Questions: 10
- Correct Retrievals: 10
- Incorrect Retrievals: 0
- Retrieval Success Rate: 100%

Success Rate = (Correct Retrievals / Total Questions) × 100

## 4. Conclusion

The retrieval system successfully retrieved relevant information for all 10 test questions.

The results show that the system can find relevant document chunks using semantic search.
