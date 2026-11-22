from llama_index.core.node_parser import SentenceSplitter 
from load_doc import documents
#spliting documnet  T2 -------------------------------------------------------------------------------------------
#256 chunk size
splitter_256=SentenceSplitter(chunk_size=256,chunk_overlap=30)
doc_as_chunkes_256=splitter_256.get_nodes_from_documents(documents)
print("number of chunkes_256=",len(doc_as_chunkes_256))

for chunk in doc_as_chunkes_256[:3]:
    print("chunk sourse=",chunk.metadata["file_name"])
    print("chunk content=",chunk.text)
    print("===================================================")
#512 chunk size 
splitter_512=SentenceSplitter(chunk_size=512,chunk_overlap=30)
doc_as_chunkes_512=splitter_512.get_nodes_from_documents(documents)
print("number of chunkes_512=",len(doc_as_chunkes_512))

for chunk in doc_as_chunkes_512[:3]:
    print("chunk sourse=",chunk.metadata["file_name"])
    print("chunk content=",chunk.text)
    print("===================================================")

#The number of chunks increases when the chunk size decreases
#Smaller chunks produce more chunks and provide more focused information
#Larger chunks produce fewer chunks and preserve more context
#number of chunkes_256= 10
#number of chunkes_512= 6