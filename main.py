from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from ollama import chat
from langchain_core.tools import tool

# -------------------------------------------
# 1. Document Ingestion & Chunking

pdf_docs = PyPDFLoader("./data/Singapore.pdf").load()
html_docs_1 = UnstructuredHTMLLoader("./data/Singapore_Travel_Guide_&_Tips_Travel_Essentials.html").load()
html_docs_2 = UnstructuredHTMLLoader("./data/Singapore_Guided_Tour_Pass_Klook.html").load()
document = pdf_docs + html_docs_1 + html_docs_2
documents = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=100,
).split_documents(document)
print('PDF Successfully chunked==============')

# ----------------------------------------------
# 2. Embedding Creation & Vector Store Indexing

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
print('Embeddings created succsesfully================')


# ----------------------------------------------
# 3. Check stored DB data in vector

collection = vectorstore._collection
raw_data = collection.get(include=["embeddings", "documents", "metadatas"])
first_vector = raw_data["embeddings"][0]
print("Vector Dimensions:", len(first_vector))
print("Raw Vector Data:", first_vector[:5], "... (truncated)")

# ----------------------------------------------
# 4. LLM model 

model = "llama3.2"

# -----------------------------------------------
# 5. Prompt Template

template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three paragraphs maximum and keep the answer concise.
Question: {input}
Context: {context}
Answer:"""

prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    """Flatten retrieved chunks into a single text block for the prompt context."""
    return "\n\n".join(doc.page_content for doc in docs)


# -----------------------------------------------
# 6. RAG Chain Assembly (Retrieval → Augmentation → Generation)
# LangChain LCEL pipeline wiring all stages together:
#   - Retrieval:    retriever fetches top-6 relevant chunks for the question.
#   - Augmentation: format_docs merges them into the prompt's {context} slot.
#   - Generation:   llmama generates the answer


chain = (
    {"context": retriever | format_docs, "input": RunnablePassthrough()}
    | prompt
    | RunnableLambda(lambda p: chat(model=model, messages=[{"role": "user", "content": p.text}], options={"max_tokens": 2000, "temperature": 0.2}))
)

#-----------------------------------------------
# 7. Tool decorator registers the RAG chain as a callable tool for the agent to use.
@tool
def singapore_rag(question: str) -> str:
    """Search the Singapore PDF and HTML knowledge base and answer the question."""
    result = chain.invoke(question)
    if hasattr(result, "message"):
        return result.message.content

    return str(result)