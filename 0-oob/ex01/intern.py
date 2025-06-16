

class Intern:

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def __init__(self, name: str | None = None):
        self.builder(name)

    def builder(self, name: str | None):
        if name is None:
            self.Name = "My name? I'm nobody, an intern, I have no name."
        else:
            self.Name = name

    def __str__(self) -> str:
        return self.Name

    def work(self):
        raise Exception("I'm just an intern, I can't do that...")

    def make_coffee(self):
        return self.Coffee()


def run_tests():
    mark = Intern("Mark")
    print(mark)
    print(mark.make_coffee())

    someone = Intern()
    print(someone)
    try:
        someone.work()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    run_tests()
