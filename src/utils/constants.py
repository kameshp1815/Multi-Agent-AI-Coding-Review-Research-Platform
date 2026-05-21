INTENT_DETECTOR_TOKENS=3000
INTENT_DETECTOR_TEMP=0.3
CODER_AGENT_TOKENS=5000
CODER_AGENT_TEMP=0.7
REVIEW_AGENT_TOKENS=3000
REVIEW_AGENT_TEMP=0.3
RESEARCH_AGENT_TOKENS=3000
RESEARCH_AGENT_TEMP=0.3
from src.models.model import State

async def state_builder(message,thread_id):
    initial_state = State(
                        message=message,
                        thread_id=thread_id,
                        intent="",
                        generated_code="",
                        review_status="",
                        review_feedback="",
                        research_feedback="",
                        research_status="",
                        messages=""
                    )
    return initial_state