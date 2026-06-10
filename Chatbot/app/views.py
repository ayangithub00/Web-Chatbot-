from django.shortcuts import render
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import (
    HuggingFaceEmbeddings,
    HuggingFaceEndpoint,
    ChatHuggingFace
)
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
# from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from rest_framework.views import APIView
from rest_framework.response import Response

from dotenv import load_dotenv
load_dotenv()

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

class ChatView(APIView):
    def post(self,request):
        page_text = request.data.get("page_text")
        question  = request.data.get("question")
        session_id = request.data.get("session_id")
        
        # Text Splitter 
        splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
        chunks   = splitter.create_documents([page_text])
        
        # Emobedding Generation
        from langchain_huggingface import HuggingFaceEmbeddings

        Embedding = HuggingFaceEndpointEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        )
        
        # Storing In Vector 
        Vector_store = FAISS.from_documents(chunks,Embedding)
        
        # Retreive 
        retreiver = Vector_store.as_retriever(search_type="similarity" , search_kwargs={"k":10})
        
        llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.5,
        )


        model = ChatHuggingFace(llm=llm)
        
        prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Answer ONLY from the provided context. If context is insufficient, say you don't know."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "Context: {context}\nQuestion: {question}")
        ])
        

        def format_docs(retrieved_docs):
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            return context_text

        parallel_chain = RunnableParallel(
        {
        'context': RunnableLambda(lambda x: x["question"]) | retreiver | RunnableLambda(format_docs),
        'question': RunnableLambda(lambda x: x["question"]),
        'chat_history': RunnableLambda(lambda x: x.get("chat_history", []))
        }
    )

        parser = StrOutputParser()

        main_chain = parallel_chain | prompt | model | parser
        
        chain_with_history = RunnableWithMessageHistory(
            main_chain,
            get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history"
        )
        
        answer = chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
        )
        return Response({"answer": answer})