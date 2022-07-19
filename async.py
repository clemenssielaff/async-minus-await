from time import sleep, time as now
from typing import *


class Scheduler:
    ready: List[Callable] = list()
    sleeping: List[Tuple[float, Callable]] = list()  # sleeping functions

    @classmethod
    def call_soon(cls, func: Callable):
        cls.ready.append(func)

    @classmethod
    def call_later(cls, delay: float, func: Callable):
        deadline = now() + delay
        cls.sleeping.append((deadline, func))
        cls.sleeping.sort()  # sort by expiration

    @classmethod
    def run(cls):
        while cls.ready or cls.sleeping:
            if not cls.ready:
                deadline, func = cls.sleeping.pop(0)  # get next
                delta = deadline - now()
                if delta > 0:
                    sleep(delta)  # sleep until next wakes up
                cls.call_soon(func)
            while cls.ready:
                current = cls.ready.pop(0)
                current()


def countdown(name: str, n: int):
    if n >= 0:
        print(name, n)
        # no sleep
        Scheduler.call_later(1, lambda: countdown(name, n - 1))


Scheduler.call_soon(lambda: countdown("Alice ", 3))
Scheduler.call_soon(lambda: countdown("Bob ", 3))
Scheduler.run()
