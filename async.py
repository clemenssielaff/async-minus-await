"""
Listing 13: Asynchrone Queues
Listing 14: Einfügen eines Items in eine asynchrone Queue
Listing 15: Auslesen eines Items aus einer asynchronen Queue

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


class AsyncQueue:
    def __init__(self):
        self.items: List[Any] = list()
        self.waiting: List[Task] = list()

    def put(self, item: Any):
        self.items.append(item)
        if self.waiting:
            Scheduler.call_soon(self.waiting.pop(0))

    def get(self) -> Task:
        def receive():
            while not self.items:
                self.waiting.append(task)
                yield
            yield Result(self.items.pop(0))

        task = Task(receive())
        return task


def producer(n: int, queue: AsyncQueue):
    while n >= 0:
        queue.put(n)
        yield Sleep(1)
        n -= 1


def consumer(name: str, queue: AsyncQueue):
    while True:
        task = queue.get()
        yield Await(task)
        print(name, task.result)
        if task.result == 0:
            return


bobs_queue = AsyncQueue()
alices_queue = AsyncQueue()

Scheduler.call_soon(Task(producer(3, bobs_queue)))
Scheduler.call_soon(Task(consumer("Alice", alices_queue)))
Scheduler.call_soon(Task(producer(3, alices_queue)))
Scheduler.call_soon(Task(consumer("Bob  ", bobs_queue)))
Scheduler.run()

"""
Output von Listing 15:

Alice 3
Bob   3
Alice 2
Bob   2
Alice 1
Bob   1
Alice 0
Bob   0
"""
