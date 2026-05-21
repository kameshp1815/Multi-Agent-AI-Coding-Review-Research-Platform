from src.repository.database import get_db
from src.repository.schema import  ErrorLogSchema
from src.utils.exceptions.custom_app_exception import DatabaseConnectionException

class ErrorRepository:
    def error(self,file_name:str,function_name:str,message:str) ->ErrorLogSchema:
        try:
            with get_db() as session:
                new_err=ErrorLogSchema(
                    file_name=file_name,
                    function_name=function_name,
                    message=message
                )   
                session.add(new_err)
                session.commit() 
                session.refresh(new_err)
        except DatabaseConnectionException:
            raise   
        except Exception as e:
            raise DatabaseConnectionException(detail=f"Failed to store error: {str(e)}")