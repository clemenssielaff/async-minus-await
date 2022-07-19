# Ergänzendes Material zum Artikel "Async Minus Await".

Sie finden den gesamten Quelltext des Beispiels in der Datei `async.py`.

Jeder tag in diesem Repo ist eine Momentaufnahme zu dem der Code funktionsfähig ist:

* [1.1 - Not Async Yet](https://github.com/clemenssielaff/async-minus-await/commit/008b935d02aab20b6eb47bda861ecd9e879d5494)
* [1.2 - The Scheduler](https://github.com/clemenssielaff/async-minus-await/commit/47bdf3aac5cccbe0105bf6498a4355681cda690e)
* [1.3 - Wait Smarter, Not Harder](https://github.com/clemenssielaff/async-minus-await/commit/3d01023c1b2630800f389d96b0dc0307e965bb0e)
* [2.2 - Generator Handling](https://github.com/clemenssielaff/async-minus-await/commit/da71639c0d600010fc14ae2d23224f6f363ce289)
* [3.5 - Consumer / Producer](https://github.com/clemenssielaff/async-minus-await/commit/b5555390f2e6260a2cfc559192e2edfbecc7571e)
* [4.4 - Wrap Up](https://github.com/clemenssielaff/async-minus-await/commit/a0ca15bc9546b79ec4bacc1331a2b0677ea71204)

[Hier](https://github.com/clemenssielaff/async-minus-await/compare) können Sie beliebige Tags miteinander vergleichen.

## Referenz

Zum Vergleich mit der letzten Version von `async.py`, hier eine alternative Implementierung mit Python's built-in `asyncio` module und den `async` und `await` keywords:

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