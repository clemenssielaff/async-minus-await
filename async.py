from time import sleep
from typing import *  # Python type hints - not necessary but informative


class Scheduler:
    ready: List[Callable] = list()  # functions ready to execute

    @classmethod
    def call_soon(cls, func: Callable):
        cls.ready.append(func)

    @classmethod
    def run(cls):
        while cls.ready:
            current = cls.ready.pop(0)
            current()


def countdown(name: str, n: int):
    if n >= 0:  # no longer a loop
        print(name, n)
        sleep(1)  # [1]
        Scheduler.call_soon(lambda: countdown(name, n - 1))


Scheduler.call_soon(lambda: countdown("Alice ", 3))  # [2]
Scheduler.call_soon(lambda: countdown("Bob ", 3))
Scheduler.run()
