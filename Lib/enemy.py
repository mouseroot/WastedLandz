import random

class Enemy:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.loot = []
        self.attack = 1

    def Attack(self):
        return self.attack + random.randint(1,5)