from time import sleep


def countdown(name: str, n: int):
    while n >= 0:
        print(name, n)
        sleep(1)
        n -= 1


countdown("Alice", 3)
countdown("Bob", 3)
