from os import system
from os import listdir
import random
import json
from Lib.player import Player
from Lib.place import Place
from Lib.enemy import Enemy
from Lib.library import Item
from Lib.menu import Menu
from Lib.person import Person,Shop




def HealPlayer(player, val):
    player.hp += int(val)


class Wilderness:
    def __init__(self, name):
        self.name = name
        self.enemies = []


#Normal places , Safe Zones

crashed_plane = Place("Crashed Plane")
underground = Place("The Underground Subway")
lake = Place("Lake")
graveyard = Place("Graveyard")
park = Place("Park")
coast = Place("Coast")
factory = Place("Factory")
city2 = Place("Big City 2")
haven = Place("Haven")
storage = Place("Storage Cellar")
city = Place("Tourine City")

#Wilderness places, fight zones, loot areas (dungeons)

swamp = Wilderness("Swamp")



city.addExploreNode(underground, f"Travel to {underground.name}")
city.addExploreNode(lake,f"Travel to {lake.name}")
city.addExploreNode(factory,f"Travel to {factory.name}")
city.addExploreNode(city2,f"Travel to {city2.name}")
city.addExploreNode(crashed_plane,f"Return to {crashed_plane.name}(Base)")

factory.addExploreNode(city,f"Travel to {city.name}")

crashed_plane.addExploreNode(city,f"Travel to {city.name}")
crashed_plane.addExploreNode(underground, f"Travel to {underground.name}")
crashed_plane.addExploreNode(storage,"Check out the storage")


underground.addExploreNode(city,f"Travel to the {city.name}")
underground.addExploreNode(graveyard,f"Travel to the {graveyard.name}")
underground.addExploreNode(crashed_plane,f"Return to {crashed_plane.name}(Base)")

lake.addExploreNode(city,f"Travel to {city.name}")

city2.addExploreNode(city,f"Travel to {city.name}")
city2.addExploreNode(haven,f"Travel to {haven.name}")


graveyard.addExploreNode(underground,f"Travel to {underground.name}")
graveyard.addExploreNode(coast,f"Travel to {coast.name}")

coast.addExploreNode(graveyard,f"Travel to {graveyard.name}")

banner = f"""_ _ _ ____ ____ ___ ____ ___  _    ____ _  _ ___  ___  
| | | | |__| [__   |  |___ |  \ |    |__| |\ | |  \   /  
| |_|_| |  | ___]  |  |___ |__/ |___ |  | | \| |__/  /__ 
{'+'+'-'*50+'+'}"""

class Game:
    def __init__(self) -> None:
        self.player = Player("Player")
        self.location = None
        self.debug = False

        self.item_table = {}
        self.person_table = {}
        self.enemy_table = {}
        self.places_table = {
            "crashed_plane": crashed_plane,
            "graveyard": graveyard,
            "city2": city2,
            "city": city,
            "lake": lake,
            "underground": underground,
            "park":park,
            "coast": coast,
            "factory": factory
        }

        self.menus = {
            "Main": Menu("",choices=["Explore","Inventory","Status","Rest","File Managment","Help"]),
            "Inventory": Menu("Inventory",exit_text="Back"),
            "Explore": Menu("Explore"),
            "Files": Menu("File Managment",choices=["Save Game","Load Game","Debug Mode"]),
            "Status": Menu(f"{self.player.name} Status"),
            "Status:SubMenu": Menu("Skill Information")
        }

        self.skill_info = {
            "Scavange": "Determines how much loot you get from dead bodies and how much is found when exploring",
            "Offense": "Determines how much base damage you do before the weapon damage is added",
            "Defense": "Your base defense against incoming attacks not including armor bonuses",
            "Technique": "Your ability to craft items from scrap found",
            "Mind/Sanity": "How sane you are your ability to fight and defend",
            "Lockpick": "Your skill with a paperclip used in lockpicking"
        }

    def LoadEnemy(self, data):
        e_data = json.loads(data)["Enemy"]
        enemy_name = e_data["name"]
        enemy_hp = int(e_data["hp"])
        enemy_exp = int(e_data["exp"])
        enemy_attacks = e_data["attacks"]
        
        enemy = Enemy(enemy_name)
        enemy.hp = enemy_hp
        enemy.exp = enemy_exp
        for attack in enemy_attacks:
            enemy.attacks[attack] = enemy_attacks[attack]
        return enemy, None
        
        

    def LoadShop(self, data):
        shop_data = json.loads(data)["Shop"]
        shop_name = shop_data["name"]
        shop_dialog = shop_data["dialog"]
        shop_items = shop_data["items"]
        shop_places = shop_data["parents"]

        shop = Shop(shop_name)
        shop.inventory = [self.item_table[x.replace("<",'').replace(">",'').split(":")[1]] for x in shop_items]
        for dialog in shop_dialog:
            shop.addDialog(dialog, shop_dialog[dialog])
        return shop, shop_places

    def LoadPerson(self, data):
        person_data = json.loads(data)["Person"]
        person_name = person_data["name"]
        person_dialog = person_data["dialog"]
        person_parents = person_data["parents"]

        pson = Person(person_name)
        for block in person_dialog:
            for i,node in enumerate(person_dialog[block]):
                if node.startswith("<"):
                    object_type,item_name = node.replace("<",'').replace(">",'').split(":")
                    try:
                        person_dialog[block][i] = self.item_table[item_name]
                    except KeyError as k:
                        print(f"Error: {person_name}, the item {k} is invalid, check the name and spelling")
                else:
                    pass
            pson.addDialog(block,person_dialog[block])
        return pson, person_parents

    def LoadItem(self, data):
        item_data = json.loads(data)["Item"]
        name = item_data["name"]
        val = int(item_data["value"])
        desc = item_data["description"]
        try:
            can_use = bool(item_data["can_use"])
            uses = int(item_data["uses"])
        except KeyError:
            can_use = False
            uses = 0
        itm = Item(name)
        itm.value = val
        itm.description = desc
        itm.can_use = can_use
        itm.uses = uses
        return itm


    def savegame(self):
        print("Saving the game")

    def loadgame(self):
        print("Loading save file")

    def initgame(self):
        print("Loading Items....")
        for json_i in listdir("Items"):
            print(f"Loading and Parsing ITEM: {json_i}")
            with open(f"Items//{json_i}") as f:
                data = f.read()
                nItem = self.LoadItem(data)
                self.item_table[nItem.name] = nItem

        print("Loading Persons....")
        for json_file in listdir("Persons"):
            print(f"Loading and Parsing PERSON: {json_file}")
            with open(f"Persons//{json_file}") as j_file:
                data = j_file.read()
                nGuy,places = self.LoadPerson(data)
                self.person_table[nGuy.name] = nGuy
                for place in places:
                    self.places_table[place].addExploreNode(nGuy,f"Talk to {nGuy.name}")

        print("Loading Shops...")
        for json_f in listdir("Shops"):
            print(f"Loading and Parsing SHOP: {json_f}")
            with open(f"Shops//{json_f}") as f:
                data = f.read()
                nShop, places = self.LoadShop(data)
                for place in places:
                    self.places_table[place].addExploreNode(nShop,f"Visit {nShop.name}'s Shop")
        print("Loading Enemies...")
        for json_file in listdir("Enemies"):
            print(f"Loading and Parsing ENEMY: {json_file}")
            with open(f"Enemies//{json_file}") as enemy_file:
                data = enemy_file.read()
                nEnemy, places = self.LoadEnemy(data)
                self.enemy_table[nEnemy.name] = nEnemy
        input("Complete, Enter to continue...")

    def gameloop(self):
        while 1:
            self.menus["Main"].sub_data = [banner] + [
                f"Name: {self.player.name}",
                f"Location: {self.location.name}",
                f"Money: ${self.player.money}"
                ]
            index, name = self.menus["Main"].Show("?")
            if self.menus["Main"].quit:
                break
            else:

                #
                #Explore Menu
                if name == "Explore":
                    if len(self.location.explore_table) > 0:
                        self.menus["Explore"].choices = [f"{x[1]}" for i,x in enumerate(self.location.explore_table)]
                        explore_index,_ = self.menus["Explore"].Show("Do what? ")
                        sel_type = self.location.explore_table[explore_index]
                        if self.menus["Explore"].quit == False:
                            #Person
                            if type(sel_type[0]) == Person:
                                sel_type[0].Dialog(self.player)
                                input("...")

                            elif type(sel_type[0]) == Shop:
                                sel_type[0].Dialog(self.player)
                            
                            #Place
                            elif type(sel_type[0]) == Place:
                                print(f"{self.player.name} travels to {sel_type[0].name}")
                                self.location = sel_type[0]
                                input("...")
                            #Item
                            elif type(sel_type[0]) == Item:
                                self.player.addItem(sel_type[0])
                                self.location.explore_table.remove(sel_type)
                                input("...")
                        else:
                            self.menus["Explore"].quit = False
                            pass


                elif name == "Inventory":
                    while 1:
                        self.menus["Inventory"].choices = [x.name for x in self.player.items]
                        item_index, item_name = self.menus["Inventory"].Show("? ")
                        if self.menus["Inventory"].quit:
                            self.menus["Inventory"].quit = False
                            break
                        else:
                            try:
                                selected_item = self.player.items[item_index]
                            except IndexError:
                                return
                            item_menu = Menu(f"{selected_item.name} Information",choices=["Use","Drop"])
                            item_menu.sub_data = [
                                f"Value: {selected_item.value}",
                                f"Description: {selected_item.description}",
                                f"Uses: {selected_item.use_count} / {selected_item.uses}" if selected_item.can_use else "Not Usable"

                            ]
                            index, item = item_menu.Show("? ")
                            if item_menu.quit:
                                break
                            else:
                                if item == "Use":
                                    if selected_item.can_use:
                                        if selected_item.uses == -1:
                                            selected_item.Use(self.player, selected_item.use_argument)
                                        else:
                                            selected_item.use_count += 1
                                            #Increase use counter
                                            if selected_item.use_count >= selected_item.uses:
                                                selected_item.Use(self.player, selected_item.use_argument)
                                                self.player.items.remove(selected_item)
                                            else:
                                                selected_item.Use(self.player, selected_item.use_argument)
                                    else:
                                        print(f"You cannot use this item")
                                elif item == "Drop":
                                    print(f"You Dropped the {selected_item.name}")
                                    self.player.items.remove(selected_item)
                        input("...")

                elif name == "Status":
                    self.menus["Status"].choices = [x for x in self.player.skills]
                    self.menus["Status"].sub_data =  [
                        f"Name: {self.player.name}",
                        f"Money: {self.player.money}",
                        f"Inventory: {len(self.player.items)}",
                        f"Health: {self.player.hp}",
                        f"Expereince: {self.player.exp}",
                        f"Level: {self.player.level}",
                        f"Wins/Losses: {self.player.wins} / {self.player.losses}",
                        f"Weapon: {'Nothing (1)' if self.player.gear['Weapon'] is None else self.player.gear['Weapon']}",
                        f"Armor: {'Nothing (1)' if self.player.gear['Armor'] is None else self.player.gear['Weapon']}"
                    ]
                    status_index, status_name = self.menus["Status"].Show("? ")
                    if self.menus["Status"].quit:
                        pass
                    else:
                        self.menus["Status:SubMenu"].sub_data = [
                            f"Name: {status_name}",
                            f"Info: {self.skill_info[status_name]}",
                            f"Level: {self.player.skills[status_name][0]}",
                            f"Progress: [{self.player.skills[status_name][1]*'#'}]"
                            ]
                        self.menus["Status:SubMenu"].Show("?")
                elif name == "Rest":
                    print("Resting....")
                elif name == "File Managment":
                    index,f_item = self.menus["Files"].Show("Action? ")
                    if f_item == "Debug Mode":
                        self.player.money += 500
                        self.location = crashed_plane
                        print("+ $500\nLocation Set: Crashed Plane")
                    elif f_item == "Save Game":
                        self.savegame()
                    elif f_item == "Load Game":
                        self.loadgame()
                    input("...")
                    

if __name__ == "__main__":
    player_name = input("What is the players name? ")
    player = Player(player_name)
    g = Game()
    g.initgame()
    g.player = player
    g.location = crashed_plane
    g.gameloop()
