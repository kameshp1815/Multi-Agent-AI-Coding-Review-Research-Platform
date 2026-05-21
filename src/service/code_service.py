from src.models.model import State
from src.utils.exceptions.custom_app_exception import AppBaseException,BuildGraphException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus,StatusCode
from src.utils.constants import state_builder
from urllib.parse import quote_plus
from settings import settings
from src.utils.logger import logger
from langgraph.graph import StateGraph, END
from src.agent.coder_agent import CoderAgent
from src.agent.review_agent import ReviewAgent
from src.agent.research_agent import ResearchAgent
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from src.agent.intent_detector_agent import IntentDetector
class BuildGraph:
    def __init__(self,error):
        self.error = error
        self.intent_detector=IntentDetector()
        self.coder_agent=CoderAgent()
        self.reviewer_agent=ReviewAgent()
        self.research_agent=ResearchAgent()

    def _get_db_uri(self) -> str:
        encoded_password = quote_plus(settings.db_password)
        return (
            f"postgresql://{settings.db_username}:{encoded_password}"
            f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        )
    async def build_graph(self,checkpointer):
        try:
            graph=StateGraph(State)
            graph.add_node("intent_detectors",self.intent_detector.run)
            graph.add_node("coder_agent",self.coder_agent.run)
            graph.add_node("reviewer_agent",self.reviewer_agent.run)
            graph.add_node("research_agent",self.research_agent.run)
            logger.info("Nodes has been added successfully")
            graph.set_entry_point("intent_detectors")
            return graph.compile(checkpointer=checkpointer)

        except BuildGraphException:
            raise
        except Exception as e:
            logger.error("Error in building graph")
            self.error.error(
                file_name="code_service.py",
                function_name="build_graph",
                message=f"Error in building graph{e}"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED),
                message=f"Service Error while building {e}",
                status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
            )
        
class CodeGenerator:
    def __init__(self,error):
        self.error=error
     
    async def code_generator(self,message:str,thread_id:str)->dict:
        try:
            async with AsyncPostgresSaver.from_conn_string(BuildGraph(self.error)._get_db_uri()) as checkpointer:
                await checkpointer.setup()
                logger.info("In Service file ")
                initial_state=await state_builder(message,thread_id)
                graph =  await BuildGraph(self.error).build_graph(checkpointer)
                logger.info("Graph has been built successfully")
                config = RunnableConfig(configurable={"thread_id": thread_id})
                result= await graph.ainvoke(initial_state,config)
                if result["generated_code"]:
                    return {"updated_code":result["generated_code"]}
                elif result["research_feedback"]:
                    return {"research_content":result["research_feedback"]}
                elif result["review_feedback"]:
                    return {"review_content":result["review_feedback"]}
                else:
                    return {"reply":result["response"]}
        except AppBaseException:
            raise 
        except Exception as e:
            logger.error("Error in Service file code_generator function")
            self.error.error(
                file_name="code_generator.py",
                function_name="code_generator",
                message=f"Error in generating code{e}"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED),
                message=f"Error in generating code{e}",
                status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE
            )


        


