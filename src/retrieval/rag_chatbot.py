
from llama_index.llms.groq import Groq
from dotenv import load_dotenv
import os
import json
import re

from src.retrieval.retrieve import retriever
from llama_index.core import PromptTemplate
from src.retrieval.reranker import reranking_result
from src.retrieval.evidence_validator import check_evidence


# --------------------------------------------------
# 1. Load environment variables and initialize LLM
# --------------------------------------------------

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY was not found in the environment variables.")

llm = Groq(
    model="openai/gpt-oss-120b",
    api_key=groq_api_key
)


# --------------------------------------------------
# 2. Decompose question into factual hypotheses
# --------------------------------------------------

def decompose_question(question, ranked_results):

    context = "\n\n".join(
        result.node.text
        for result, score in ranked_results
    )

    prompt = f"""
You are a question analysis component in a Retrieval-Augmented Generation system.

Your task is to break the user's question into independent factual hypotheses.

Question:
{question}

Available context:
{context}

Instructions:

1. Extract only the specific factual information requested by the user.
2. Each hypothesis must represent one independent factual claim.
3. Do not answer the question.
4. Do not add information that the user did not request.
5. Do not invent facts, names, prices, numbers, durations, or other details.
6. Do not assume that information exists just because the question asks about it.
7. Preserve the meaning of the user's question.
8. If the question asks about multiple details, create a separate hypothesis for each detail.
9. Return only a valid JSON array of strings.
10. Do not include Markdown or explanations.

Example output:
[
    "The Practical Artificial Intelligence course lasts 8 weeks.",
    "The Practical Artificial Intelligence course includes 48 training hours."
]

Return the JSON array only.
"""

    response = llm.complete(prompt, max_tokens=2048)

    response_text = response.text.strip()

    if not response_text:
        raise ValueError("The LLM returned an empty response.")

    # Remove Markdown JSON fences if present
    response_text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response_text,
        flags=re.IGNORECASE
    ).strip()

    hypotheses = json.loads(response_text)

    if not isinstance(hypotheses, list):
        raise ValueError("The generated hypotheses must be a JSON list.")

    if not all(isinstance(item, str) for item in hypotheses):
        raise ValueError("Every hypothesis must be a string.")

    return hypotheses


# --------------------------------------------------
# 3. Check whether numerical claims exist in evidence
# --------------------------------------------------

def numeric_claim_is_grounded(premise, hypothesis):

    number_pattern = r"\b\d+(?:,\d{3})*(?:\.\d+)?\b"

    premise_numbers = set(
        re.findall(number_pattern, premise)
    )

    hypothesis_numbers = set(
        re.findall(number_pattern, hypothesis)
    )

    return hypothesis_numbers.issubset(premise_numbers)


# --------------------------------------------------
# 4. Validate hypotheses using NLI
# --------------------------------------------------

def validate_hypotheses(hypotheses, ranked_results):

    validation_results = []

    for hypothesis in hypotheses:

        evidence = []

        for result, relevance_score in ranked_results:

            source = result.metadata.get("file_name", "Unknown source")

            chunk_text = result.node.text

            sentences = re.split(r"(?<=[.!?])\s+", chunk_text)

            for sentence in sentences:

                sentence = sentence.strip()

                if not sentence:
                    continue

                # Reject numerical claims not grounded in this sentence
                if not numeric_claim_is_grounded(sentence, hypothesis):
                    continue

                nli_result = check_evidence(
                    premise=sentence,
                    hypothesis=hypothesis
                )

                evidence.append({
                    "source": source,
                    "premise": sentence,
                    "label": nli_result["label"],
                    "score": nli_result["score"]
                })

        # A hypothesis is supported only if at least one
        # evidence sentence entails it with sufficient confidence.

        supported = any(
            item["label"] == "entailment"
            and item["score"] >= 0.8
            for item in evidence
        )

        validation_results.append({
            "hypothesis": hypothesis,
            "supported": supported,
            "evidence": evidence
        })

    return validation_results


# --------------------------------------------------
# 5. Check whether at least one hypothesis is supported
# --------------------------------------------------

def is_answer_supported(validation_results):

    if not validation_results:
        return False

    return any(
        item["supported"]
        for item in validation_results
    )


# --------------------------------------------------
# 6. Generate the final answer
# --------------------------------------------------

qa_prompt = PromptTemplate(
    """
You are a helpful assistant for a training center.

Answer the user's question using ONLY the information in the
provided evidence.

Question:
{question}

Supported evidence:
{context}

Instructions:

1. Use only facts explicitly supported by the evidence.
2. Do not invent or assume any information.
3. Answer all parts of the question that can be answered using the evidence.
4. If a requested detail is not available in the evidence,
   clearly say that the provided information does not contain the answer.
5. Do not infer a course price from a general statement about paying course fees.
6. Do not add unsupported numbers, dates, names, or details.
7. If the question has both supported and unsupported parts,
   provide the supported information and clearly mention what is unavailable.
8. Keep the answer clear and concise.
9. Treat source labels as references, not as additional facts.

Answer:
"""
)


# --------------------------------------------------
# 7. Main RAG pipeline
# --------------------------------------------------

def ask_question(question):

    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
            "supported": False
        }

    # Greeting shortcut
    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if question.lower().strip("!?., ") in greetings:
        return {
            "answer": "Hello! How can I help you with the training center?",
            "sources": [],
            "supported": True
        }

    # Step 1: Retrieve relevant chunks
    retrieved_results = retriever.retrieve(question)

    if not retrieved_results:
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Step 2: Similarity filtering
    similarity_threshold = 0.6

    filtered_results = [
        result
        for result in retrieved_results
        if result.score is not None
        and result.score >= similarity_threshold
    ]

    if not filtered_results:
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Step 3: Reranking
    ranked_results = reranking_result(
        question,
        filtered_results
    )

    if not ranked_results:
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Step 3.1: Relevance Gate
    # Reranker scores are raw relevance scores, not probabilities.
    reranker_threshold = 0.1

    top_relevance_score = max(
        score for result, score in ranked_results
    )

    if top_relevance_score < reranker_threshold:
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Step 4: Generate hypotheses
    hypotheses = decompose_question(
        question,
        ranked_results
    )

    if not hypotheses:
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Step 5: Validate hypotheses
    validation_results = validate_hypotheses(
        hypotheses,
        ranked_results
    )

    # Step 6: Check whether any part is supported
    if not is_answer_supported(validation_results):
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Step 7: Collect only evidence supporting hypotheses
    supported_evidence = []

    for item in validation_results:

        if not item["supported"]:
            continue

        for evidence in item["evidence"]:

            if (
                evidence["label"] == "entailment"
                and evidence["score"] >= 0.8
            ):
                supported_evidence.append(evidence)

    if not supported_evidence:
        return {
            "answer": "I don't have enough information to answer this question.",
            "sources": [],
            "supported": False
        }

    # Remove duplicate evidence sentences
    unique_evidence = []
    seen_evidence = set()

    for item in supported_evidence:

        evidence_key = (
            item["source"],
            item["premise"]
        )

        if evidence_key not in seen_evidence:
            seen_evidence.add(evidence_key)
            unique_evidence.append(item)

    # Include source names alongside the evidence
    context = "\n".join(
        f"[Source: {item['source']}] {item['premise']}"
        for item in unique_evidence
    )

    # Step 8: Generate final answer from supported evidence
    final_prompt = qa_prompt.format(
        question=question,
        context=context
    )

    response = llm.complete(
        final_prompt,
        max_tokens=2048
    )

    answer = response.text.strip()

    if not answer:
        answer = "I don't have enough information to answer this question."

    # Step 9: Collect unique sources
    sources = list(dict.fromkeys(
        item["source"]
        for item in unique_evidence
    ))

    return {
        "answer": answer,
        "sources": sources,
        "supported": True
    }


# --------------------------------------------------
# 8. Local testing
# --------------------------------------------------

if __name__ == "__main__":

    question = "What is the main mission of the training center?"

    result = ask_question(question)

    print("\n" + "-" * 60)
    print(result)
