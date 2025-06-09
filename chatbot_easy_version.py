import openai
import os
import sys
from dotenv import load_dotenv
load_dotenv()

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

# openai_key = os.environ.get['OPENAI_API_KEY']
os.environ["OPENAI_API_KEY"] = ""


# This is used to pass the argument with query
query = None
if len(sys.argv) > 1:
	query = sys.argv[1]


# Load custom data and split it into chunks
loader = DirectoryLoader("mydata/")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# This part is used for embedding the docs and store it into a Vector DB and initialize the retriever
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

# Create the RetrieveQA object
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

# This part is used to build a chat or Q@A application having the capability of both conversational capabilities and document retreival
chain = ConversationalRetrievalChain.from_llm(
	llm=ChatOpenAI(model="gpt-3.5-turbo"),
	retriever=docsearch.as_retriever(search_kwargs={'k':1})
	)

chat_history = []
while True:
	if not query:
		query = input('Prompt: ')
	if query in ['quit','q','exit']:
		sys.exit()

	result = chain({'question': query, "chat_history": chat_history})
	print(result['answer'])

	chat_history.append((query, result['answer']))
	query = None