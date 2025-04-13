import os
import asyncio
from time import time, sleep
from datetime import datetime
from typing import Literal
from dotenv import load_dotenv
from mem0 import Memory
from mem0_settings import config as mem0_config
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from async_mem0 import AsyncMemory

load_dotenv(override=True)

openai_model = OpenAIModel('gpt-4o-mini', provider=OpenAIProvider(api_key=os.environ["OPENAI_API_KEY"])) # provider could be omitted tho

class Mem0Deps(BaseModel):
    user_id: str
    memory: Memory

    model_config = { "arbitrary_types_allowed": True }

agent = Agent(  
    model=openai_model,
    deps_type=Memory,
    # result_type=Response,
    system_prompt=(
        """
        ~~RULES~~
        - Interact in pt-BR
        - Be kind but brief using less tokens as possible
        - Whenever needed, use the tool to get user relevant memories, specially when context of what's asked involves user's personal info
        ~~PROMPT~~
        You are a nice assistant
        """        
    ),
)

@agent.tool_plain # this would work as prompt? A: yes, but the prompt is only processed when the app starts, so it would always tell the same datetime over and over again. As with tool, it process things on the run
def get_current_date() -> str:  
    """Get the current date"""
    return f'The date is {datetime.now()}.'

@agent.tool
def get_user_relevant_memories(ctx: RunContext[Mem0Deps], messages_query: str):
    """Retrieves user info from memories"""
    print(f"\n** using tool to get memories. user_id={ctx.deps.user_id} | messages_query={messages_query} **\n")
    
    relevant_memories = ctx.deps.memory.search(user_id=ctx.deps.user_id, query=messages_query, limit=3)

    # print(f"Relevant memories: \n{relevant_memories}\n")

    return relevant_memories['results']


async def main():
    memory = AsyncMemory.from_config(mem0_config)

    start_time = time()

    user_id = "some@email.com"
    user_message = "Hi"

    result = await agent.run(user_message)

    updated_time = time()

    print("--- Took %s seconds for AI to compute first hello ---" % (updated_time - start_time))

    while user_message != "quit":
        asyncio.create_task(memory.add(user_id=user_id, messages=user_message, metadata={ "context": "pydantic ai test" }))
        asyncio.create_task(memory.add(user_id=user_id, messages=result.data, metadata={ "context": "pydantic ai test" }))

        await asyncio.sleep(0) # for a tick it yields the thread control to event loop so memory.add tasks are executed. This is required because the while loop blocks the event loop and the tasks get stuck

        # updated_time = time()

        # print("--- Took %s seconds to add messages to memory ---" % (updated_time - start_time))

        print(result.data)

        user_message = input("> ")

        start_time = time()

        result = await agent.run(user_message, message_history=result.all_messages(), deps=Mem0Deps(memory=memory, user_id=user_id))

        updated_time = time()

        print("--- Took %s seconds for agent to run ---" % (updated_time - start_time))

if __name__ == "__main__":
    asyncio.run(main())