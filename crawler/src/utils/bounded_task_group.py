import asyncio


class BoundedTaskGroup(asyncio.TaskGroup):
    def __init__(self, max_tasks=0):
        super().__init__()
        if max_tasks:
            self._sem = asyncio.Semaphore(max_tasks)
        else:
            self._sem = None

    def create_task(self, coro, *args, **kwargs):
        if self._sem:
            async def _wrapped_coro(sem, coro):
                async with sem:
                    return await coro

            coro = _wrapped_coro(self._sem, coro)

        return super().create_task(coro, *args, **kwargs)
