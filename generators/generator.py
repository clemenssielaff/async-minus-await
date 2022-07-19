def foo():
    """
    A simple generator with yields and one piece of internal state (i).
    """
    i = 1
    yield f"one: {i}"
    i += 1
    yield f"two: {i}"


class Foo:
    """
    Manual implementation of the Foo generator.
    """

    def __init__(self):
        """
        Initializes the state of the generator before starting.
        """
        self.cursor = 0
        self.i = None

    def __next__(self):
        """
        Sequence generator.
        """
        self.cursor += 1
        if self.cursor == 1:
            self.i = 1
            return f"one: {self.i}"
        elif self.cursor == 2:
            self.i += 1
            return f"two: {self.i}"
        raise StopIteration()

    def __iter__(self):
        """
        Allow iteration using a for-in loop.
        """
        try:
            while True:
                yield next(self)
        except StopIteration:
            return


def main():
    """
    Main function.
    """
    print("Python generator:")
    for i in foo():
        print(i)
    print("---")
    print("Manual generator:")
    for i in Foo():
        print(i)


if __name__ == "__main__":
    main()
