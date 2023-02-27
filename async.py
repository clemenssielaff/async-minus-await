"""
Listing 9: Ein Task besteht aus einem Generator und einem Resultat
Listing 10: Der Scheduler kann schlafen, einen Wert erwarten oder einen produzieren
Listing 11: Künstlich erschwerter Countdown mit einem asynchronen Produzenten
Listing 12: Ausführung von Befehlen im Scheduler

Um sich alle Code-Beispiele in diesem Artikel ansehen und vergleichen zu können,
besuchen Sie bitte:
    https://github.com/clemenssielaff/async-minus-await/compare
"""
from time import sleep, time as now
from typing import *


class Task:
    def __init__(self, generator: Generator):
        self.generator: Generator = generator
        self.result: Optional[Any] = None


class Sleep:
    def __init__(self, duration: float):
        self.duration: float = duration


class Result:
    def __init__(self, result: Any):
        self.result: Any = result


class Await:
    def __init__(self, task: Task):
        self.task: Task = task


class Scheduler:
    ready: List[Task] = list()
    sleeping: List[Tuple[float, Task]] = list()
    blocked: Dict[Task, Set[Task]] = dict()

    @classmethod
    def call_soon(cls, func: Task):
        cls.ready.append(func)

    @classmethod
    def call_later(cls, delay: float, func: Task):
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
                    instruction = next(current.generator)
                except StopIteration:
                    continue

                if isinstance(instruction, Sleep):
                    cls.call_later(instruction.duration, current)

                elif isinstance(instruction, Result):
                    current.result = instruction.result
                    if current in cls.blocked:
                        for blocked in cls.blocked[current]:
                            cls.call_soon(blocked)
                        del cls.blocked[current]

                elif isinstance(instruction, Await):
                    if instruction.task in cls.blocked:
                        cls.blocked[instruction.task].add(current)
                    else:
                        cls.blocked[instruction.task] = {current}
                    cls.call_soon(instruction.task)


def producer(n: int):
    yield Sleep(1)
    yield Result(n - 1)


def countdown(name: str, n: int):
    while n >= 0:
        print(name, n)
        task = Task(producer(n))
        yield Await(task)
        n = task.result


Scheduler.call_soon(Task(countdown("Alice", 3)))
Scheduler.call_soon(Task(countdown("Bob  ", 3)))
Scheduler.run()

"""
Output von Listing 12:

Alice 3
Bob   3
Alice 2
Bob   2
Alice 1
Bob   1
Alice 0
Bob   0
"""
