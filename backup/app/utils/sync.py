import asyncio

from functools import partial
from typing import Callable

async def run_in_thread(sync_funtion, *args, **kwargs) -> Callable: # type: ignore
    loop = asyncio.get_running_loop()
    sync_fn = partial(sync_funtion, *args, **kwargs)
    return await loop.run_in_executor(None, sync_fn)
    