import random

class Player:
    def __init__(self, name, start_location=None):
        self.name = name
        self.hp = 100
        self.exp = 1
        self.level = 1
        self.wins = 0
        self.losses = 0
        self.fights = 0
        self.rest_cooldown = 0
        self.money = 0

        self.items = []
        self.skills = {
            "Scavange": [1,0],
            "Offense": [1,0],
            "Defense": [1,0],
            "Technique": [1,0],
            "Mind/Sanity": [10,0],
            "Lockpick": [1,0]
        }
        self.blueprints = {
            "Ammo": False,
            "Raygun": False,
            "Motherboard Plate": False
        }
        self.location = start_location

        self.gear = {
            "Weapon": None,
            "Armor": None
        }

    def Attack(self):
        base_attack = self.skills["Offense"][0]
        base_weapon = self.gear["Weapon"].damage 
        r_attack = random.randint(1, 5+base_weapon)
        return base_attack + r_attack

    def setLocation(self, loc):
        self.location = loc

    def addBlueprint(self, blueprint):
        if blueprint in self.blueprints:
            self.blueprints[blueprint] = True

    def addItem(self, item):
        print(f"{self.name} Obtained a {item.name}!")
        self.items.append(item)

    def addSkill(self, name, value):
        print(f"{name} increased by {value}")
        self.skills[name][1] += value
        if self.skills[name][1] >= 5:
            self.skills[name][0] += 1
            print(f"{name} Increased in level (Now level {self.skills[name][0]}!)")

    def removeItem(self, name, count):
        self.items[name] -= count

    def listBluePrints(self):
        print("[Blueprints]")
        for i,blueprint in enumerate(self.blueprints):
            if self.blueprints[blueprint]:
                print(f"{i}.\t{blueprint.name}")
        

    def listSkills(self):
        print("[Skills]")
        for skill in self.skills:
            print(f"{skill}:\t{self.skills[skill][0]} [{self.skills[skill][1]} / 5]")

    def listItems(self):
        print("[Inventory]")
        for i,item in enumerate(self.items):
            print(f"{i}.:\t{item.name}")
        return len(self.items)
