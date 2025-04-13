import asyncio
from mem0 import Memory
from functools import wraps, partial

def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run 

class AsyncMemory(Memory):
    def add(self, user_id: str, agent_id:str = None, run_id:str = None, messages: any = None, metadata: dict = None, *args, **kwargs):
        kwargs.update({
            'user_id': user_id,
            'agent_id': agent_id,
            'run_id': run_id,
            'messages': messages,
            'metadata': metadata
        })

        async_add = async_wrap(super().add)

        return async_add(*args, **kwargs)


    def add_via_thread(self, user_id: str, agent_id:str = None, run_id:str = None, messages: any = None, metadata: dict = None, *args, **kwargs):
        kwargs.update({
            'user_id': user_id,
            'agent_id': agent_id,
            'run_id': run_id,
            'messages': messages,
            'metadata': metadata
        })

        asyncio.to_thread(super().add, *args, **kwargs)