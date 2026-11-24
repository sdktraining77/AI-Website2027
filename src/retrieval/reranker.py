from sentence_transformers import CrossEncoder

model = CrossEncoder("BAAI/bge-reranker-base")#هاد الموديل مخصص لإعادة ترتيب نتائج البحث حسب العلاقة بين السؤال والمقطع
#--------------------------------------------------------------------------------------------
def reranking_result(question, results):
    pairs=[]
    for r in results:
        pairs.append((question,r.node.text))
    scores = model.predict(pairs)#score relevence بجيب 
    ranked_results =sorted(zip(results, scores), key=lambda x: x[1],reverse=True)
    return ranked_results

if __name__ == "__main__":
    from src.retrieval.retrieve import retrieve_documents

    question = "What courses does the training center offer and how long does each course take?"

    results = retrieve_documents(question)

    ranked_results = reranking_result(question, results)

    for result, score in ranked_results:
        print("Source:", result.metadata["file_name"])
        print("Relevance Score:", score)
        print("Content:", result.node.text)
        print("=" * 60)