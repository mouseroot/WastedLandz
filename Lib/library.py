#from Lib.enemy import Enemy

class Item:
    def __init__(self, name):
        self.name = name
        self.value = 1
        self.description = ""
        self.can_use = False
        self.uses = -1
        self.use_count = 0
        self.use_argument = 0

    def Use(self, target, arg):
        print(f"{target.name} uses {self.name} with arg: {arg}")

class Weapon(Item):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 1

class Armor(Item):
    def __init__(self, name):
        super().__init__(name)
        self.defense = 1
