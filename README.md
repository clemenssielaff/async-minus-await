# Ergänzendes Material zum Artikel "Asynchrones Programmieren: async minus await".

Sie finden den gesamten Quelltext des [Artikels](https://www.heise.de/hintergrund/Asynchrones-Programmieren-async-minus-await-7527129.html) in der Datei `async.py`.

Jeder tag in diesem Repo ist eine Momentaufnahme zu dem der Code funktionsfähig ist:

* [Listing 1-2: Ein einfacher, synchroner Countdown](https://github.com/clemenssielaff/async-minus-await/commit/06a908253df6a0ed4b73dcdf923586c27429e08e)
* [Listing 3-4: Countdown mit einem einfachen Scheduler](https://github.com/clemenssielaff/async-minus-await/commit/c126efe659988c83e0e5e000dfa75e82cc6da27e)
* [Listing 5: Wait Smarter, Not Harder](https://github.com/clemenssielaff/async-minus-await/commit/b25ddb18774838c6aed7b4fd34eb4a063145dc07)
* [Listing 6-8: Scheduler mit Generatoren](https://github.com/clemenssielaff/async-minus-await/commit/ba064b81e0a16a9fdf71f70a7392f44bb7d32c52)
* [Listing 9-12: Ausführung von Befehlen im Scheduler](https://github.com/clemenssielaff/async-minus-await/commit/dc8358e7ad0f1c6dbedacc2fd528a588e88642a5)
* [Listing 13-15: Asynchrone Queues](https://github.com/clemenssielaff/async-minus-await/commit/a1616c788840558755cd2fb75394a34a39deb642)

[Hier](https://github.com/clemenssielaff/async-minus-await/compare/Listing-1...Listing-15) können Sie beliebige Tags miteinander vergleichen.

## asyncio Referenz

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
