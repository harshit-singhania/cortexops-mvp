from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.core.cache import cache_service

class LogDebuggerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="openai/gpt-3.5-turbo",
            temperature=0,
            openai_api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        
        self.prompt_template = """You are an expert DevOps engineer and backend debugger.
        Analyze the following log entry and provide a root cause analysis.
        
        Log Entry:
        {log_data}
        
        Context (surrounding logs or metadata):
        {context}
        
        Please provide:
        1. Summary of the error.
        2. Potential Root Cause.
        3. Recommended Fix.
        """
        
        self.PROMPT = PromptTemplate(
            template=self.prompt_template, input_variables=["log_data", "context"]
        )

    async def analyze(self, log_data: str, context: str = "") -> str:
        # Cache key based on log data
        cache_key = f"{log_data[:100]}-{context[:50]}"
        cached_response = cache_service.get("debugger_agent", cache_key)
        if cached_response:
            return cached_response

        chain = self.PROMPT | self.llm
        response = await chain.ainvoke({"log_data": log_data, "context": context})
        result = response.content
        
        cache_service.set("debugger_agent", cache_key, result)
        return result

debugger_agent = LogDebuggerAgent()
