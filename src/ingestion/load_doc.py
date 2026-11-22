from llama_index.core import SimpleDirectoryReader
from pathlib import Path
# loading data  T1  ------------------------------------------------------------------------------------------
project_root= Path(__file__).resolve().parents[2]#بدنا نرجع لجذر المشروع، وبعدها ندخل على مجلد data
data=project_root/ "data"
documents= SimpleDirectoryReader(input_dir=str(data)).load_data()
print("number of document loaded=",len(documents))

for document in documents:
    print(document.metadata["file_name"])# بقدر برضو اجيب ال file_path ,file_type,file_size 
    print(document.text[0:200])
