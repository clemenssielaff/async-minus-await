"""
Listing 1: Ein einfacher, synchroner Countdown

Um sich alle Code-Beispiele in diesem Artikel ansehen und vergleichen zu können,
besuchen Sie bitte:
    https://github.com/clemenssielaff/async-minus-await/compare
"""
from time import sleep


def countdown(name: str, n: int):
    while n >= 0:
        print(name, n)
        sleep(1)
        n -= 1


countdown("Alice", 3)
countdown("Bob  ", 3)

"""
Listing 2: Output von Listing 1, zwei Countdowns nacheinander

Alice 3
Alice 2
Alice 1
Alice 0
Bob   3
Bob   2
Bob   1
Bob   0
"""
