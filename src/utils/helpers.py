from langchain_aws import ChatBedrock
import boto3
from uuid import uuid4
from src.models.model import ChatRequest
from src.utils.logger import logger
from settings import settings
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode,ErrorCodeStatus,StatusCode
class LLM:
    def __init__(self,error):
        self.error=error
    async def get_llm(self,max_tokens,temperature) -> ChatBedrock:
        try:
            client = boto3.client(
                service_name="bedrock-runtime",
                region_name=settings.aws_region,
            )
            return ChatBedrock(
                client=client,
                model_id=settings.model_id,
                provider=settings.provider,
                model_kwargs={
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
            )
        except AppBaseException:
            raise
        except Exception as e:
            logger.error("Error in creating llm client")
            self.error.error(
                file_name="helpers.py",
                function_name="get_llm",
                message="Error while creating client{e}"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.INTERNAL_SERVER_ERROR,"CA_01"),
                message=f"Coder agent error{e}",
                status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE

            )
        
async def thread_check(request:ChatRequest):
    if request.thread_id is None:
        return uuid4()
    thread_id=request.thread_id.strip()
    if not thread_id:
        raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED),
                status_code= StatusCode().BAD_REQUEST,
                message= f"User thread can't be empty"
            ) 
    return thread_id

        

