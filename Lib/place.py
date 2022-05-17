import random
from Lib.library import *

class Place:
    def __init__(self, name, loot_table=[],enemy_table=[]):
        self.doors = []
        self.name = name
        self.intro_text = ""
        self.description_text = ""
        self.direction = ""
        self.loot_table = loot_table
        self.enemy_table = enemy_table
        self.explore_table = []

    def addDoor(self, otherPlace):
        self.doors.append(otherPlace)
        otherPlace.doors.append(self)

    def setIntroText(self, text):
        self.intro_text = text

    def setDescriptionText(self, text):
        self.description_text = text

    def setDirection(self, dir):
        self.direction = dir.upper()

    def addExploreNode(self, type, text):
        self.explore_table.append([type, text])
