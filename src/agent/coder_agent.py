from src.models.model import State
from langgraph.types import Command
from src.agent.agent import BaseAgent
from langchain_core.messages import HumanMessage,SystemMessage
from src.agent.prompts import SYSTEM_PROMPT
from src.utils.exceptions.custom_app_exception import AgentInvocationException
from src.utils.logger import logger
from src.utils.constants import CODER_AGENT_TOKENS,CODER_AGENT_TEMP
class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            max_tokens=CODER_AGENT_TOKENS,
            temperature=CODER_AGENT_TEMP,
            system_prompt=SYSTEM_PROMPT
        )
    async def run(self,state:State)->State:
        try:
            agent= await self.get_agent()
            logger.info("Coder Agent created successfully")
            contents=f"User query is {state['message']} and The generated code is {state['generated_code']}  and The review feedback that need to be corrected in the code is {state['review_feedback']}"
            result= await agent.ainvoke({
                "messages":[HumanMessage(content=contents)]
            }
            )
            logger.info("Coder Agent Response Generated Successfully")
            generated_code=result["messages"][-1].content
            print(f"The generated code is : \n {generated_code}")
            return Command(update={
                "generated_code":generated_code
            },goto="reviewer_agent")
        except AgentInvocationException:
            raise
        except Exception as e:
            self.handle_exception(e)      


