"""
Listing 5: Wait Smarter, Not Harder

Um sich alle Code-Beispiele in diesem Artikel ansehen und vergleichen zu können,
besuchen Sie bitte:
    https://github.com/clemenssielaff/async-minus-await/compare
"""
from time import sleep, time as now
from typing import *


class Scheduler:
    ready: List[Callable] = list()
    sleeping: List[Tuple[float, Callable]] = list()

    @classmethod
    def call_soon(cls, func: Callable):
        cls.ready.append(func)

    @classmethod
    def call_later(cls, delay: float, func: Callable):
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
                current()


def countdown(name: str, n: int):
    if n >= 0:
        print(name, n)
        # no sleep
        Scheduler.call_later(1, lambda: countdown(name, n - 1))


Scheduler.call_soon(lambda: countdown("Alice", 3))
Scheduler.call_soon(lambda: countdown("Bob  ", 3))
Scheduler.run()

"""
Die Ausführung dieses Programms dauert 4 Sekunden (3 Sekunden bis zum Ende des
Countdowns, eine weitere Sekunde bis der Scheduler beendet ist).
Dies ist das erwartete Verhalten.


Output von Listing 5:

Alice 3
Bob   3
Alice 2
Bob   2
Alice 1
Bob   1
Alice 0
Bob   0
"""
