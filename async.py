"""
Listing 3: Countdown mit einem einfachen Scheduler

Um sich alle Code-Beispiele in diesem Artikel ansehen und vergleichen zu können,
besuchen Sie bitte:
    https://github.com/clemenssielaff/async-minus-await/compare
"""
from time import sleep
from typing import *


class Scheduler:
    ready: List[Callable] = list()

    @classmethod
    def call_soon(cls, func: Callable):
        cls.ready.append(func)

    @classmethod
    def run(cls):
        while cls.ready:
            current = cls.ready.pop(0)
            current()


def countdown(name: str, n: int):
    if n >= 0:
        print(name, n)
        sleep(1)
        Scheduler.call_soon(lambda: countdown(name, n - 1))


Scheduler.call_soon(lambda: countdown("Alice", 3))
Scheduler.call_soon(lambda: countdown("Bob  ", 3))
Scheduler.run()

"""
Anmerkungen zu Listing 3:
Zeile 12 [1]: Um den Kontrollfluss zuverlässig zu steuern, darf es nur einen
    Scheduler geben. Er ist deshalb als Singleton geschrieben.
Zeile 30 [2]: Die Schleife wird von countdown in den Scheduler verlagert.
    Dieser kann  somit mehrere gleichzeitige Schleifen verzahnen.
Zeile 33 [3]: Der Scheduler kann nur Funktionen ohne Parameter ausführen,
    countdown benötigt allerdings einen Namen und die derzeitige Zahl. Deshalb
    wird der eigentliche Aufruf in eine parameterlose Lambda-Funktion verpackt.

Die Ausführung dieses Programms dauert 8 Sekunden (6 Sekunden bis zum Ende des
Countdowns, weitere 2 Sekunden bis der Scheduler beendet ist).
Dies ist doppelt so lange wie erwartet.


Listing 4: Output von Listing 3: zwei Countdowns zur selben Zeit

Alice 3
Bob   3
Alice 2
Bob   2
Alice 1
Bob   1
Alice 0
Bob   0
"""
