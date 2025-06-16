
class HotBeverage:
    def __init__(self):
        self.name = "hot beverage"
        self.price = 0.30

    def description(self) -> str:
        return "Just some hot water in a cup."

    def __str__(self):
        return "\n".join([
            f"name : {self.name}",
            f"price : {self.price:.2f}",
            f"description : {self.description()}"
            ])

class Coffee(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "coffee"
        self.price = 0.40

    def description(self) -> str:
        return "A coffee, to stay awake."

class Tea(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "tea"

class Chocolate(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "chocolate"
        self.price = 0.50

    def description(self) -> str:
        return "Chocolate, sweet chocolate..."

class Cappuccino(HotBeverage):
    def __init__(self):
        super().__init__()
        self.name = "cappuccino"
        self.price = 0.45

    def description(self) -> str:
        return "Un po' di Italia nella sua tazza!"

def test_single_drink(drink):
    instance = drink()
    print(instance, end="\n\n")

def process():
    test_single_drink(HotBeverage)
    test_single_drink(Coffee)
    test_single_drink(Tea)
    test_single_drink(Chocolate)
    test_single_drink(Cappuccino)

if __name__ == "__main__":
    process()
