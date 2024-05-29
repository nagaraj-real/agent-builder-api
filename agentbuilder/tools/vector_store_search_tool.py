# You can easily equip your agent with a vector store!

from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.faiss import FAISS
from agentbuilder.llm import get_embed_llm


# Set embeddings
embd = get_embed_llm()

# Docs to index
urls = [
   "https://paulgraham.com/best.html",
]

# Load
docs = [WebBaseLoader(url).load() for url in urls]
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

vectorstore_search = create_retriever_tool(
   retriever=vectorstore_retriever,
   name="vectorstore_search",
   description="Retrieve relevant info from a vectorstore that contains information from Paul Graham about how to write good essays."
)

vectorstore_search.metadata= {"file_path": str(Path(__file__).absolute())}