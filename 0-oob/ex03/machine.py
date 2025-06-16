import random
import beverages

class CoffeeMachine:
    _MAX_RESOURCE = 10
    def __init__(self):
        self.resource = self._MAX_RESOURCE

    def repair(self):
        self.resource = self._MAX_RESOURCE

    def serve(self, beverage_class: type[beverages.HotBeverage]):
        if self.resource <= 0:
            raise self.BrokenMachineException()
        self.resource -= 1
        return random.choice([beverage_class(), self.EmptyCup()])
    
    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    class EmptyCup(beverages.HotBeverage):
        def __init__(self):
            super().__init__()
            self.name = "empty cup"
            self.price = 0.90

        def description(self) -> str:
            return "An empty cup?! Gimme my money back!"


if __name__ == "__main__":
    machine_one = CoffeeMachine()
    beverages_list: list[type[beverages.HotBeverage]] = [
        beverages.HotBeverage,
        beverages.Coffee,
        beverages.Tea,
        beverages.Chocolate,
        beverages.Cappuccino
        ]
    for i in range(23):
        try:
            print(machine_one.serve(random.choice(beverages_list)))
        except CoffeeMachine.BrokenMachineException as e:
            print(f"\033[0;31m{e}\033[0m")
            if i < 20:
                machine_one.repair()
                print("\033[0;32m[REPAIRED]\033[0m")
