import random

class Enemy:
    def __init__(self, name):
        self.name = name
        self.hp = 1
        self.items = []
        self.base_attack = 1
        self.attacks = {}

    def Attack(self):
        return self.attack + random.randint(1,5)