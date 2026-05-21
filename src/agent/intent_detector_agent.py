from src.models.model import State,Intent
from src.utils.exceptions.custom_app_exception import AgentInvocationException
from langgraph.types import Command
from src.utils.logger import logger
from src.agent.prompts import SYSTEM_PROMPT_LLM
from langchain_core.messages import HumanMessage
from langgraph.graph import  END
from src.agent.agent import BaseAgent
from src.utils.constants import INTENT_DETECTOR_TEMP,INTENT_DETECTOR_TOKENS
class IntentDetector(BaseAgent):
    def __init__(self):
        super().__init__(
            max_tokens=INTENT_DETECTOR_TOKENS,
            temperature=INTENT_DETECTOR_TEMP,
            system_prompt=SYSTEM_PROMPT_LLM,
            response_format=Intent
        )
    async def run(self,state:State)->State:
        try:
            agent=await self.get_agent()
            result=await agent.ainvoke({
                "messages":[HumanMessage(content=state["message"])]
            }
            )
            intents=result.get('structured_response').model_dump()
            intent=intents['intent'].lower()
            logger.info(f"User intent is {intent}")
            if intent == "review":
                return Command(update={"generated_code":state["message"],"intent":intent},goto="reviewer_agent")
            elif intent == "code":
                return Command(update={"intent":intent},goto="coder_agent")
            elif intent == "research":
                return Command(update={"intent":intent},goto="research_agent")
            elif intent == "research and code":
                return Command(update={"intent":intent},goto="research_agent")
            else:
                return Command(update={"intent":intent,"response":intents['message']},goto=END)
                
        except AgentInvocationException:
            raise
        except Exception as e:
            self.handle_exception(e)    
