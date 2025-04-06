# You can easily equip your agent with a vector store!

from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from agentbuilder.llm import get_embed_llm
from agentbuilder.data import data_path

# Set embeddings
embd = get_embed_llm()
job_retriever=None

def load_job_retriever():
   global job_retriever
   # Docs to index
   urls = [
      f"{data_path}/job_description.txt",
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
   job_retriever = vectorstore.as_retriever()
   return job_retriever


load_job_retriever()

from langchain.tools.retriever import create_retriever_tool

job_description_tool = create_retriever_tool(
   retriever=job_retriever,
   name="job_description_tool",
   description="Retrieve relevant info from a vectorstore that contains description about a job",
)

job_description_tool.metadata= {"file_path": str(Path(__file__).absolute())}