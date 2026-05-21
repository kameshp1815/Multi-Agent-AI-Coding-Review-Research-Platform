from fastapi import FastAPI,Request
import uvicorn
from src.router.router import router
from fastapi.responses import JSONResponse
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import StatusCode
app=FastAPI(title="Coder Agent",version="1.0.0")
@app.exception_handler(AppBaseException)
async def app_exception_handler(request:Request,exc:AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request:Request,exc:Exception):
    return JSONResponse(
        status_code=StatusCode().INTERNAL_SERVER_ERROR_STATUS_CODE,
        content={"message":"An unexpected error occured"}
    )

app.include_router(router)
if __name__== "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )
