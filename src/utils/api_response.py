from uuid import uuid4
from datetime import datetime
class APIResponse:
    def __init__(self,thread_id:str,message:dict,status_code:int):
        self.message="Response has been generated Successfully"
        self.status_code=status_code
        self.request_id=uuid4()
        self.timestamp=datetime.now().timetz()
        self.response=message
        self.thread_id=thread_id
        self.to_dict()
    def to_dict(self):
        return{
            "message":self.message,
            "status_code":self.status_code,
            "response":self.response,
            "request_id":self.request_id,
            "thread_id":self.thread_id,
            "timestamp":self.timestamp
        }
