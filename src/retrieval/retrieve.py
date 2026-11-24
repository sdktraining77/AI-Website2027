from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")#مراجعه هااد الموديل 
project_root= Path(__file__).resolve().parents[2]#بدنا نرجع لجذر المشروع، وبعدها ندخل على مجلد data
storage_dir = project_root / "src" / "ingestion" / "storage"
if not storage_dir.exists():
    raise FileNotFoundError(
        f"Storage directory not found: {storage_dir}"
    )


#Implement and Test Semantic Document Retrieval     T4 =============================================
storage_context=StorageContext.from_defaults(persist_dir=str(storage_dir))
index=load_index_from_storage(storage_context,embed_model=embed_model)#بدنا نرجع ال index الي حفظناه من قبل 


retriever = index.as_retriever(similarity_top_k=3)

def retrieve_documents(question):
    results = retriever.retrieve(question)
    for result in results:
        print("result source=",result.metadata.get("file_name", "Unknown source"))
        print("result content=",result.text)
        print("similarity score=",result.score)
        print("===================================================")
    return results

if __name__ == "__main__":
    results = retrieve_documents(
        "What courses does the training center offer and how long does each course take?"
    )

































































"""StorageContext: بيساعدنا نوصل لبيانات الـ Index المحفوظة.



load_index_from_storage: بتحميل الـ Index من مجلد storage.



HuggingFaceEmbedding: عشان نستخدم نفس موديل الـ Embedding اللي استخدمناه وقت بناء الفهرس."""