from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter

# loading data  T1  ------------------------------------------------------------------------------------------
documents= SimpleDirectoryReader("../../data").load_data()
print("number of document loaded=",len(documents))

for document in documents:
    print(document.metadata["file_name"])# بقدر برضو اجيب ال file_path ,file_type,file_size 
    print(document.text[0:200])

#spliting documnet  T2 -------------------------------------------------------------------------------------------
#256 chunk size
splitter=SentenceSplitter(chunk_size=256,chunk_overlap=30)
doc_as_chunkes_256=splitter.get_nodes_from_documents(documents)
print("number of chunkes_256=",len(doc_as_chunkes_256))

for chunk in doc_as_chunkes_256[:3]:
    print("chunk sourse=",chunk.metadata["file_name"])
    print("chunk content=",chunk.text)
    print("===================================================")
#512 chunk size 
splitter=SentenceSplitter(chunk_size=512,chunk_overlap=30)
doc_as_chunkes_512=splitter.get_nodes_from_documents(documents)
print("number of chunkes_512=",len(doc_as_chunkes_256))

for chunk in doc_as_chunkes_256[:3]:
    print("chunk sourse=",chunk.metadata["file_name"])
    print("chunk content=",chunk.text)
    print("===================================================")