from llama_index.llms.groq import Groq#هاد للوصل مع ال llm 
from dotenv import load_dotenv #لتحميل المتغيرات الموجودة في .env.
import os
from src.retrieval.retrieve import retriever#حتى نجيب الملف اللي عملناه دغري
from llama_index.core import PromptTemplate #حتى نكتب تعليمات للنموذج.
from llama_index.core.query_engine import RetrieverQueryEngine #لربط الاسترجاع مع توليد الإجابات.



# read api key 
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
#connect llm 
llm = Groq(model="openai/gpt-oss-20b",api_key=groq_api_key)




#انشاء ال System Prompt

qa_prompt = PromptTemplate(
    """
    You are a helpful assistant for a training center.
    Answer the user's question using ONLY the provided context.
    If the context does not contain enough information,
    say: "I don't have enough information to answer this question."
    Do not use outside knowledge or invent information.
    Use all relevant information from the context.
    Answer the exact question asked by the user.
    Do not focus on only one retrieved document if others contain relevant information.

    Context:
    {context_str}

    Question:
    {query_str}

    Answer:
    """
)

#انشاء ال query_engine
#
query_engine = RetrieverQueryEngine.from_args(  #فكرته الاساسيه انه LlamaIndex بجهّز مكونات النظام ويربطها مع بعضها.
    retriever=retriever,#هو المتغيراللي احنا عملناه ورحعنا استدعيناه 
    llm=llm,#الموديل المستخدم 
    text_qa_template=qa_prompt
)
# انشاء فنكشن ياخد سؤال ويرجع اجابه 
def ask_question(question):
    greetings = ["hello", "hi", "hey", "good morning", "good evening"]

    if question.strip().lower().rstrip("!.,?") in greetings:
        return {"answer": "Hello! Welcome to our training center. How can I help you today?", "sources": [], "supported": True}

    response = query_engine.query(question)

    if not response.source_nodes or max(node.score or 0 for node in response.source_nodes) < 0.6:  # هاد ليمنع ظهور الاجابه المش مدعومه
        return {"answer": "I don't have enough information to answer this question.", "sources": [], "supported": False}

    answer = response.response
    sources = []

    for i in response.source_nodes:
        sources.append({"file_name": i.node.metadata["file_name"], "similarity_score": i.score})

    return {"answer": answer, "sources": sources, "supported": True}