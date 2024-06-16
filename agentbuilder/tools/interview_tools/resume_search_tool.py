# You can easily equip your agent with a vector store!

from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from agentbuilder.llm import get_embed_llm


# Set embeddings
embd = get_embed_llm()
current_path = str(Path(__file__).parent)

# Docs to index
urls = [
   current_path+"./../../data/resume.txt",
]

# Load
docs = [TextLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

# Split
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
   chunk_size=512, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

# Add to vectorstore
vectorstore = FAISS.from_documents(
   documents=doc_splits,
   embedding=embd,
)

vectorstore_retriever = vectorstore.as_retriever()


from langchain.tools.retriever import create_retriever_tool

resume_search = create_retriever_tool(
   retriever=vectorstore_retriever,
   name="resume_search_tool",
   description="Retrieve relevant info from a vectorstore that contains information on a candidate resume."
)

resume_search.metadata= {"file_path": str(Path(__file__).absolute())}