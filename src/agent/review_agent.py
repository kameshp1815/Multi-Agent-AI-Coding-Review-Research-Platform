from src.models.model import State
from langgraph.graph import  END
from src.models.model import ReviewAgentResponse
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.repository.error_repository import ErrorRepository
from src.utils.constants import REVIEW_AGENT_TOKENS,REVIEW_AGENT_TEMP
from src.agent.prompts import SYSTEM_PROMPT_PEP8
from src.utils.exceptions.custom_app_exception import AppBaseException,AgentInvocationException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from settings import settings
from src.utils.logger import logger
from src.agent.agent import BaseAgent
from langgraph.types import Command
error=ErrorRepository()

async def create_client():
    try:
        mcp_client= MultiServerMCPClient({
                "coder agent":{
                    "url":settings.mcp_server_url,
                    "transport":"streamable-http"
                    }})
        tools= await mcp_client.get_tools()
        allowed_tools=["format_code"]
        load_tools=[]
        for i in tools:
            if i.name in allowed_tools:
                load_tools.append(i)
        logger.info("MCP Tools loaded successfully for Review Agent")
        return load_tools
    except AgentInvocationException:
        raise
    except Exception as e:
        logger.error("Error in creating client for MCP Server")
        error.error(
            file_name="review_agent.py",
            function_name="create_client",
            message=f"MCP client creation error{e}"
        )
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR,"CA_01"),
            message=f"MCP client creation error{e}",
            status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
        )
    
class ReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            max_tokens=REVIEW_AGENT_TOKENS,
            temperature=REVIEW_AGENT_TEMP,
            system_prompt=SYSTEM_PROMPT_PEP8,
            response_format=ReviewAgentResponse     
        )

    async def run(self,state:State)->State:
        try:
            tools=await create_client()
            self.tools =tools
            agent= await self.get_agent()
            logger.info("Review Agent Created Successfuly")
            result= await agent.ainvoke({
                "messages":[HumanMessage(content=state["generated_code"])]
            }
            )
            logger.info("Reviewer Agent Reviewed Successfully")
            results=result.get('structured_response').model_dump()
            review_status=results['review_status'].strip().lower()
            logger.info(f"Review Status is {review_status}")
            print(f"Review Feedback obtained is: \n {results['review_feedback']}")
            if review_status=="pass":   
                return Command(update={
                "review_status": "PASS",
                "review_feedback":results['review_feedback']
                },goto=END)
            elif review_status=="fail": 
                return Command(update={
                "review_status": "FAIL",
                "review_feedback":results['review_feedback']
                },goto="research_agent")
            
        except AgentInvocationException:
            raise
        except Exception as e:
            self.handle_exception(e)    

