from abc import ABC, abstractmethod
from src.repository.error_repository import ErrorRepository
from src.utils.helpers import LLM, logger
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus, StatusCode
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

class BaseAgent(ABC):
    def __init__(self, max_tokens: int, temperature: float, system_prompt: str, response_format=None, tools=None, **kwargs):
        self.error = ErrorRepository()            
        self.max_tokens = max_tokens              
        self.temperature = temperature            
        self.system_prompt = system_prompt        
        self.response_format = response_format     
        self.tools = tools                         
        self.kwargs = kwargs

    async def get_agent(self):
        llm = await LLM(self.error).get_llm(      
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return  create_agent(                       
            model=llm,
            system_prompt=SystemMessage(content=self.system_prompt),
            **({"response_format": self.response_format} if self.response_format else {}),
            **({"tools": self.tools} if self.tools else {}),
            **self.kwargs
        )

    def handle_exception(self, e: Exception):     
        logger.info("Error in Agent")
        self.error.error(
            file_name="agent.py",
            function_name="agent",
            message=f"Agent running error: {e}"
        )
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR, "CA_01"),
            message=f"Agent error: {e}",
            status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
        )

    @abstractmethod
    async def run(self, *args, **kwargs):           
        pass