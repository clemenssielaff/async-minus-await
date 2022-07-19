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
                    # reschedule blocked tasks
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


def countdown(name: str, x: int):
    while x >= 0:
        print(name, x)
        task = Task(producer(x))
        yield Await(task)
        x = task.result


Scheduler.call_soon(Task(countdown("Alice ", 3)))
Scheduler.call_soon(Task(countdown("Bob ", 3)))
Scheduler.run()
