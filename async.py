from time import sleep, time as now
from typing import *


class Scheduler:
    ready: List[Generator] = list()
    sleeping: List[Tuple[float, Generator]] = list()

    @classmethod
    def call_soon(cls, func: Generator):
        cls.ready.append(func)

    @classmethod
    def call_later(cls, delay: float, func: Generator):
        deadline = now() + delay
        cls.sleeping.append((deadline, func))
        cls.sleeping.sort()

    @classmethod
    def run(cls):
        while cls.ready or cls.sleeping:
            if not cls.ready:
                deadline, func = cls.sleeping.pop(0)
                delta = deadline - now()
                if delta > 0:
                    sleep(delta)
                cls.call_soon(func)
            while cls.ready:
                current = cls.ready.pop(0)
                try:
                    delay = next(current)
                except StopIteration:
                    continue  # discard finished generators
                if delay is not None:
                    cls.call_later(delay, current)


def countdown(name: str, n: int):
    while n >= 0:
        print(name, n)
        yield 1  # sleep for 1 second
        n -= 1


Scheduler.call_soon(countdown("Alice ", 3))
Scheduler.call_soon(countdown("Bob ", 3))
Scheduler.run()
