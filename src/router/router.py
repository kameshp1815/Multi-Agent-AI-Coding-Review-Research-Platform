from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from src.utils.api_response import APIResponse
from src.models.model import ChatRequest,ChatResponse
from src.service.code_service import CodeGenerator
from src.repository.error_repository import ErrorRepository
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode,ErrorCodeStatus,StatusCode
from src.utils.logger import logger
from src.utils.helpers import thread_check

def depends(error:ErrorRepository = Depends(ErrorRepository)):
    return CodeGenerator(error=error)

router=APIRouter(prefix="/api/v1",tags=["Coder Agent"])
@router.post("/chat")
async def code_generator(request:ChatRequest,service:CodeGenerator=Depends(depends),error:ErrorRepository=Depends(ErrorRepository)):
    try:
        logger.info("In Code Generator Router File")
        thread_id=await thread_check(request)
        message=request.message.strip()
        if message and thread_id:
            logger.info("In Code Generator Router:Request has been validated ")
            result= await service.code_generator(message,thread_id)
            return APIResponse(
                thread_id=str(thread_id),
                message=result,
                status_code=StatusCode().RESPONSE_GENERATED_STATUS_CODE
            )
        else:
            logger.error("User sent an empty values either for message or for thread_id")
            error.error(
                function_name="code_generator",
                file_name="router.py",
                message="User query or thread_id can't be empty"
            )
            raise AppBaseException(
                error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED,"CA_AGENT_01"),
                status_code= StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE,
                message= f"User message or thread id can't be empty"
            )

    except AppBaseException:
        raise
    except Exception as e:
        logger.error("Error in router file")
        error.error(
            function_name="code_generator",
            file_name="router.py",
            message=f"Router Error {e}"
        )
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(ErrorCode.CHAT_PROCESSING_FAILED,"CA_AGENT_01"),
            status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE,
            message= f"Router error while generating code{e}"
        )
        