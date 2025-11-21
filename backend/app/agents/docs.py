from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.core.cache import cache_service

class DocsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="openai/gpt-3.5-turbo", # Cheaper model for summarization
            temperature=0.3,
            openai_api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        
        self.prompt_template = """You are a Technical Writer.
        Generate a concise architectural summary for the following service based on its manifest and metadata.
        
        Service Name: {service_name}
        Description: {description}
        Metadata: {metadata}
        
        Output Format:
        ## Service Overview
        [Summary]
        
        ## Key Features
        - [Feature 1]
        - [Feature 2]
        
        ## Tech Stack
        [Inferred from metadata]
        """
        
        self.PROMPT = PromptTemplate(
            template=self.prompt_template, input_variables=["service_name", "description", "metadata"]
        )

    async def generate_docs(self, service_name: str, description: str, metadata: dict) -> str:
        cache_key = f"{service_name}-{description[:50]}"
        cached_response = cache_service.get("docs_agent", cache_key)
        if cached_response:
            return cached_response

        chain = self.PROMPT | self.llm
        response = await chain.ainvoke({
            "service_name": service_name,
            "description": description,
            "metadata": str(metadata)
        })
        result = response.content
        
        cache_service.set("docs_agent", cache_key, result)
        return result

docs_agent = DocsAgent()
