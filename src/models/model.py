from pydantic import BaseModel,Field
from typing import TypedDict,Optional
class ChatRequest(BaseModel):
    message:str
    thread_id:Optional[str]=None

class ChatResponse(BaseModel):
    reply:str

class State(TypedDict):
    message:str
    thread_id:str
    intent:str
    generated_code:str
    review_status:str
    review_feedback:str
    research_status:str
    research_feedback:str  
    response:str

class Intent(BaseModel):
    intent:str
    message:str=Field(description="Enter your own response here.Don't enter user request here")

class ReviewAgentResponse(BaseModel):
    review_status:str=Field(description="Enter thr status as either pass or fail")
    review_feedback:list[str]=Field(description="Enter the feedback of the review obtained here.Just provide the list of improvements in the code")

class ResearchAgentResponse(BaseModel):
    research_status:str=Field(description="Enter the status as either pass or fail")
    research_feedback:list[str]=Field(description="Enter the feedback of the research obtained with the help of tools." "Never call tools more than 5 times"\
    "Just provide the list of improvements in the code")
