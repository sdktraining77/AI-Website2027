
# RAG Answer Evaluation

## 1. Evaluation Overview

The purpose of this evaluation is to test the RAG chatbot's ability to:

- Answer questions using the training center documents.
- Understand paraphrased questions.
- Retrieve relevant information from multiple documents.
- Handle unsupported questions without generating fabricated answers.
- Respond appropriately to greetings.

### System Configuration

- **Embedding Model:** BAAI/bge-small-en-v1.5
- **LLM:** openai/gpt-oss-20b (via Groq)
- **Retrieval Top K:** 3
- **Similarity Threshold:** 0.6

## 2. Test Cases

### Test 1: Greeting

- **Question:** `Hello`
- **Expected Answer:** A friendly greeting.
- **Actual Answer:** Hello! Welcome to our training center. How can I help you today?
- **Sources:** No supporting sources required.
- **Result:** Pass

**Additional Test:**
- **Question:** `Hello!`
- **Actual Answer:** Hello! Welcome to our training center. How can I help you today?
- **Sources:** No supporting sources required.
- **Result:** Pass

**Notes:** The chatbot now handles greetings directly without calling the RAG query engine. It also handles punctuation marks at the end of greetings.

### Test 2: Paraphrased AI Course Duration

- **Question:** Can you tell me the duration of the AI course?
- **Expected Answer:** 8 weeks (48 training hours).
- **Actual Answer:** The Practical Artificial Intelligence course lasts 8 weeks and includes 48 training hours.
- **Sources:**
  - ai-course.md (0.833)
  - faq.md (0.826)
  - faq.md (0.775)
- **Result:** Pass

### Test 3: Web Development Course Duration

- **Question:** What is the duration of the Web Development course?
- **Expected Answer:** 10 weeks (60 training hours).
- **Actual Answer:** 10 weeks (60 training hours).
- **Sources:**
  - web-development.md (0.816)
  - faq.md (0.786)
- **Result:** Pass

### Test 4: Unsupported Medical Degree

- **Question:** Does the training center offer a medical degree?
- **Expected Answer:** The chatbot should not invent information.
- **Actual Answer:** I don't have enough information to answer this question.
- **Sources:**
  - faq.md (0.642)
  - about.md (0.640)
- **Result:** Pass

### Test 5: Paraphrased Data Analysis Course Question

- **Question:** I'm interested in learning data analysis. What training does the center provide?
- **Expected Answer:** Information about the Data Analysis with Python and Power BI course.
- **Actual Answer:** The chatbot provided the course name, description, duration, schedule, prerequisites, target audience, learning outcomes, and fee.
- **Sources:**
  - data-analysis.md (0.700)
  - about.md (0.678)
  - faq.md (0.670)
- **Result:** Pass

### Test 6: Data Analysis Schedule

- **Question:** What days and times are Data Analysis classes held?
- **Expected Answer:** Monday, Wednesday, and Thursday, from 4:00 PM to 6:00 PM.
- **Actual Answer:** Monday, Wednesday, and Thursday, from 4:00 PM to 6:00 PM.
- **Sources:**
  - data-analysis.md (0.740)
  - faq.md (0.684)
  - ai-course.md (0.651)
- **Result:** Pass

### Test 7: Prerequisites and Target Audience

- **Question:** What are the prerequisites and target audience for the Data Analysis course?
- **Expected Answer:** Basic computer skills, recommended spreadsheet knowledge, no previous Python experience required, and the relevant target audience.
- **Actual Answer:** The chatbot correctly listed the prerequisites and target audience.
- **Sources:**
  - data-analysis.md (0.746)
  - ai-course.md (0.674)
  - web-development.md (0.632)
- **Result:** Pass

### Test 8: Unsupported Scholarship Question

- **Question:** Does the training center provide scholarships or financial aid?
- **Expected Answer:** The chatbot should not invent scholarship information.
- **Actual Answer:** I don't have enough information to answer this question.
- **Sources:**
  - faq.md (0.655)
  - about.md (0.637)
- **Result:** Pass

### Test 9: Comparing Course Durations

- **Question:** Compare the duration of the AI, Web Development, and Data Analysis courses.
- **Expected Answer:**
  - AI: 8 weeks (48 hours).
  - Web Development: 10 weeks (60 hours).
  - Data Analysis: 6 weeks (36 hours).
- **Actual Answer:** The chatbot correctly compared all three courses and identified Web Development as the longest and Data Analysis as the shortest.
- **Sources:**
  - faq.md (0.740)
  - ai-course.md (0.716)
- **Result:** Partial Pass
- **Notes:** The answer was correct, but the displayed sources did not clearly include all three course documents. Source coverage needs further investigation.

### Test 10: Data Analysis Course Fee

- **Question:** How much does the Data Analysis course cost?
- **Expected Answer:** 160 JOD.
- **Actual Answer:** The Data Analysis course costs 160 JOD.
- **Sources:**
  - data-analysis.md (0.766)
  - faq.md (0.664)
  - ai-course.md (0.662)
- **Result:** Pass

## 3. Evaluation Summary

| Metric | Result |
|---|---:|
| Total Tests | 10 |
| Pass | 8 |
| Partial Pass | 1 |
| Needs Improvement | 1 |

The chatbot successfully answered most supported questions and rejected unsupported questions without inventing answers.

## 4. Limitations

- Greetings are not handled separately from knowledge-base questions.
- Retrieved sources may include documents that are not directly relevant to the question.
- Similarity scores alone do not guarantee that retrieved context contains enough information.
- Multi-document answers may not always display all relevant source documents.
- The evaluation uses a limited set of manually written test questions.

## 5. Future Improvements

- Add greeting detection and friendly responses.
- Improve retrieval relevance and source filtering.
- Improve multi-document retrieval and answer grounding.
- Expand the evaluation dataset with more questions and paraphrases.
- Tune the similarity threshold using a larger evaluation dataset.
