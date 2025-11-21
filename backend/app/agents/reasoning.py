from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.services.embeddings import embedding_service
from app.core.config import settings
from app.core.cache import cache_service

class SystemReasoningAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="openai/gpt-3.5-turbo",
            temperature=0,
            openai_api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        self.vector_store = embedding_service.get_vector_store()
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        self.prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        Answer:"""
        
        self.PROMPT = PromptTemplate(
            template=self.prompt_template, input_variables=["context", "question"]
        )

    async def run(self, query: str) -> str:
        # Check cache
        cached_response = cache_service.get("reasoning_agent", query)
        if cached_response:
            return cached_response

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": self.PROMPT}
        )
        
        try:
            response = await qa_chain.ainvoke({"query": query})
            result = response['result']
            
            # Cache result
            cache_service.set("reasoning_agent", query, result)
            return result
        except Exception as e:
            return f"Error processing query: {str(e)}"

reasoning_agent = SystemReasoningAgent()
