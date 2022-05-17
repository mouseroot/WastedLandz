from Lib.menu import Menu
from Lib.person import Person,Shop
from Lib.player import Player
from Lib.library import Item
import json
import copy
from os.path import exists
from main import Game

g = Game()
g.initgame()

p_object = {
    "Person": {
        "name": "",
        "dialog": {},
        "parents": ["crashed_plane"]
    }
}

i_object = {
    "Item": {
        "name": "",
        "value": 0
    }
}

s_object = {
    "Shop": {
        "name": ""
    }
}

banner = f"""
| _ _ _ ____ ____ ___ ____ ___     ____ ___  _  _ 
| | | | |__| [__   |  |___ |  \    [__  |  \ |_/  
| |_|_| |  | ___]  |  |___ |__/    ___] |__/ | \_ 
| 
{'+'+'-'*50+'+'}"""

while 1:
    m = Menu("",choices=["Create Person","Create Item","Create Shop","Edit Person","Edit Item","Edit Shop"])
    m.sub_data = [banner] + [
        f"{len(g.places_table)} Places",
        f"{len(g.item_table)} Items",
        f"{len(g.person_table)} Persons"
    ]
    index, item = m.Show()
    if m.quit:
        print("Thanks for using the Wasted SDK")
        break
    else:
        if item == "Create Person":
            p_object = copy.copy(p_object)
            while 1:
                person_menu = Menu("Creating a new Person",choices=["Set Name","Add Dialog Node","Add Dialog Response","Test Person","Save Person"])
                person_menu.sub_data = [
                    "Current Person Data",
                    f"Name: {p_object['Person']['name']}",
                    f"Location: {p_object['Person']['parents']}"
                    ]
                index, selection = person_menu.Show("?")
                if person_menu.quit:
                    break
                else:
                    if selection == "Set Name":
                        name = input("Persons name: ")
                        p_object["Person"]["name"] = name

                    elif selection == "Add Dialog Node":
                        print("Enter a dialog prompt or .quit to exit")
                        node = input("Dialog Prompt: ")
                        if node == ".quit":
                            pass
                        else:
                            p_object["Person"]["dialog"][node] = []
                    elif selection == "Add Dialog Response":
                        while 1:
                            node_menu = Menu("Add To Which Dialog node",choices=list(p_object["Person"]["dialog"].keys()))
                            index,name = node_menu.Show("? ")
                            if node_menu.quit:
                                break
                            else:
                                node = p_object["Person"]["dialog"][name]
                                while 1:
                                    print("Enter response .quit to exit")
                                    print(f"Prompt: {name}")
                                    response = input("Response: ")
                                    if response == ".quit":
                                        break
                                    else:
                                        p_object["Person"]["dialog"][name].append(response)
                    elif selection == "Test Person":
                        print(f"Setting up Person data {p_object['Person']['name']}")
                        p = Person(p_object["Person"]["name"])
                        for dialog in p_object["Person"]["dialog"]:
                            p.addDialog(dialog,p_object["Person"]["dialog"][dialog])
                        p.Dialog(Player("Wasted SDK Developer"))

                    elif selection == "Save Person":
                        save_menu = Menu(f"Really save {p_object['Person']['name']}?",choices=["Yes","No"])
                        index, item = save_menu.Show("?")
                        if save_menu.quit or index == 1:
                            pass
                        else:
                            filename = input("Save to which file? ")
                            with open(f"Persons//{filename}","w") as newPerson:
                                newPerson.write(json.dumps(p_object))
                            if exists(f"Persons//{filename}"):
                                print("Saved")
                            else:
                                print("Error: file not found!!!")

