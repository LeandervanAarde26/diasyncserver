from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

def create_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1400,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        memory=memory,
        llm=llm,
        retriever=vectorstore.as_retriever()
        )
    return chain

def user_input(user_question, chain):
    try:
        response = chain(
            {'question': user_question}
        )
        return response['chat_history']
    
    except Exception as e:
        print("Err:", e)

def main(query, data):
    load_dotenv()
    try:
        print("getting text chunks")
        chunks = create_chunks(data)
        if(chunks is not None):
            print("handling vectorstore")
            vectorstore = vector_store(chunks)
            print(vectorstore)
            if vectorstore:
                print("creating chain")
                chain = get_conversation_chain(vectorstore)
                if chain:
                    print("handling query")
                    return user_input(query, chain)
                
                
    except Exception as e:
        print(str(e))