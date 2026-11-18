from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding#بسمح إلنا نستخدم موديلات Embedding من Hugging Face محليًا بدل الاعتماد على OpenAI API
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

documents = SimpleDirectoryReader("../../data").load_data()   #t1

splitter=SentenceSplitter(chunk_size=256,chunk_overlap=30)  #t2
doc_as_chunkes=splitter.get_nodes_from_documents(documents)


# build a Vector Index  T3=======================================================================
index=VectorStoreIndex.from_documents(doc_as_chunkes ,embed_model=embed_model)
print("vectore index crated successfuly")
print("Number of indexed chunks:", len(doc_as_chunkes))
index.storage_context.persist(persist_dir="storage")#عشان ما نعيد بناء الـ Index والـ Embeddings كل مرة نشغّل فيها المشروع.
print("Index saved successfully!")














































"""لما أنشأنا الـ VectorStoreIndex، طلع معنا Error بحكي إنه ما في OpenAI API Key، لأنه LlamaIndex بشكل افتراضي بحاول يستخدم موديل Embedding من OpenAI، وإحنا ما عنا API Key.

كيف حلّيناها؟

بدل ما نستخدم OpenAI، قررنا نستخدم موديل مجاني ومحلي من Hugging Face اسمه BAAI/bge-small-en-v1.5.

ثبتنا المكتبة المطلوبة، واستوردنا HuggingFaceEmbedding، وحمّلنا الموديل، وبعدها ربطناه بالـ VectorStoreIndex.

وبهيك قدرنا نعمل الـ Index بنجاح بدون الحاجة لـ OpenAI API Key."""