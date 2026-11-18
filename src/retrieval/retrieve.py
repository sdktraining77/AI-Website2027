from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")



#Implement and Test Semantic Document Retrieval     T4 =============================================
storage_context=StorageContext.from_defaults(persist_dir="../ingestion/storage")
index=load_index_from_storage(storage_context,embed_model=embed_model)#بدنا نرجع ال index الي حفظناه من قبل 
print("Index loaded successfully!")

retriever = index.as_retriever(similarity_top_k=3)

def retrieve_documents(question):
    results = retriever.retrieve(question)
    for result in results:
        print("result sourse=",result.metadata["file_name"])
        print("result content=",result.text)
        print("===================================================")
    return results
question = input("Enter your question: ")
results = retrieve_documents(question)







































































"""StorageContext: بيساعدنا نوصل لبيانات الـ Index المحفوظة.



load_index_from_storage: بتحميل الـ Index من مجلد storage.



HuggingFaceEmbedding: عشان نستخدم نفس موديل الـ Embedding اللي استخدمناه وقت بناء الفهرس."""