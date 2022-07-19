# Ergänzendes Material zum Artikel "Async Minus Await".

Sie finden den gesamten Quelltext des Beispiels in der Datei `async.py`.
Jeder commit in diesem Repo ist eine Momentaufnahme zu dem der Code funktionsfähig ist.
Das heißt, es gibt zum Beispiel den Commit "2.2", aber da die Zwischenschritte kein lauffähiges Programm darstellen, ist der nächste Commit erst wieder "3.5".

## Referenz

Die letzte Version des `async.py` snippets steht im Vergleich zur Referenzimplentierung mit Python's built-in `asyncio` module und den `async` und `await` keywords:

```python
import asyncio


async def producer(n: int, queue: asyncio.Queue):
    while n >= 0:
        queue.put_nowait(n)
        await asyncio.sleep(1)
        n -= 1


async def consumer(name: str, queue: asyncio.Queue):
    while True:
        result = await queue.get()
        print(name, result)
        if result == 0:
            return


async def main():
    bobs_queue = asyncio.Queue()
    alices_queue = asyncio.Queue()
    await asyncio.gather(
        asyncio.create_task(producer(3, bobs_queue)),
        asyncio.create_task(consumer("Alice", alices_queue)),
        asyncio.create_task(consumer("Bob", bobs_queue)),
        asyncio.create_task(producer(3, alices_queue)),
    )


asyncio.run(main())
```