
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

## 5. RAG Chatbot Evaluation

This section evaluates the chatbot's answer generation using the retrieved context.

| Test | Expected Behavior | Result |
|---|---|---|
| Relevant question | Generate an answer based on the documents | Passed |
| Question about course information | Provide accurate course details | Passed |
| Question about registration | Explain registration steps | Passed |
| Question about course fees | Return the correct fee | Passed |
| External question | Return an insufficient information message | Passed |

**Additional Observation:**

A final regression test showed that the chatbot could not answer a question requiring information about both the training center's courses and its main mission. This remains a known limitation for future improvement.

### Conclusion

The RAG chatbot successfully generates natural-language answers using the retrieved documents.

It also provides supporting source filenames and handles questions that cannot be answered using the available information.

**Note:** The 100% retrieval success rate applies only to the 10 questions included in this evaluation. Complex multi-document questions may still require further improvement.