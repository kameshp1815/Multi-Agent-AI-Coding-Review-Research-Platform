from src.models.model import State
from langgraph.graph import  END
from src.models.model import ResearchAgentResponse
from src.agent.agent import BaseAgent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.utils.helpers import LLM
from langgraph.types import Command
from src.agent.prompts import RESEARCH_AGENT_SYSTEM_PROMPT
from src.utils.exceptions.custom_app_exception import AppBaseException,AgentInvocationException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from settings import settings
from src.utils.constants import RESEARCH_AGENT_TOKENS,RESEARCH_AGENT_TEMP
from src.utils.logger import logger
from src.repository.error_repository import ErrorRepository

error=ErrorRepository()
async def create_client():
        try:
            mcp_client= MultiServerMCPClient({
                    "research agent":{
                        "url":settings.mcp_server_url_ddg,
                        "transport":"streamable-http",
                        }})
            tools=await mcp_client.get_tools()
            logger.info("MCP Tools loaded successfully for Research Agent")
            return tools
        except AgentInvocationException:
            raise
        except Exception as e:
            logger.error("Error in creating client for MCP Server")
            error.error(
                file_name="research_agent.py",
                function_name="create_client",
                message=f"MCP client creation error{e}"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR,"CA_01"),
                message=f"MCP client creation error{e}",
                status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
            )
    
class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            max_tokens=RESEARCH_AGENT_TOKENS,
            temperature=RESEARCH_AGENT_TEMP,
            system_prompt=RESEARCH_AGENT_SYSTEM_PROMPT,
            response_format=ResearchAgentResponse
            
        )

    async def run(self,state:State)->State:
        try:
            tools=await create_client()
            self.tools=tools
            agent=await self.get_agent()
            logger.info("Research Agent Created Successfuly")
            result= await agent.ainvoke({
                "messages":[HumanMessage(content=f"User message is {state['message'] }and review feedback obtained is {state['review_feedback']}")]
            }
            )
            logger.info("Researcher Agent Researched Successfully")
            results=result.get('structured_response').model_dump()
            research_status=results['research_status'].strip().lower()
            logger.info(f"Research status obtained is {research_status}")
            print(f"Research Feedback obtained is: \n {results['research_feedback']}")
            if state['intent'] == "research ":
                route=END
            else:
                route="coder_agent"
            if research_status=="pass":   
                return Command(update={
                "research_status": "PASS",
                "research_feedback":results['research_feedback']
                },goto=route)
            elif research_status == "fail":
                return Command(update={
                "research_status": "FAIL",
                "research_feedback":results['research_feedback']
                },goto=route)
        except AgentInvocationException:
            raise
        except Exception as e:
            self.handle_exception(e)    
        
