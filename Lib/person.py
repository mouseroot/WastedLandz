from os import system
from Lib.menu import Menu
from Lib.library import Item

class Person:
    def __init__(self, name) -> None:
        self.name = name
        self.dialog = {}

    def addDialog(self, prompt, response):
        self.dialog[prompt] = response


    def Dialog(self, player):
        while 1:
            speak_menu = Menu(f"Talking with {self.name}",choices=[x for x in self.dialog])
            index, item = speak_menu.Show("? ")
            if speak_menu.quit:
                break
            else:
                current_line = list(self.dialog.keys())[index]
                print(f"{player.name}: {current_line}")
                for i,text in enumerate(self.dialog[current_line]):
                    if type(text) == Item:
                        player.addItem(text)
                        self.dialog[current_line][i] = "*You already obtained this item*"
                    else:
                        print(f"{self.name}: {text}")
                    input("...")
                input("End of Dialog...")
"""
    def Dialog(self, player):
        speaking = True
        quit_index = len(self.dialog)
        while speaking:
            system("cls")
            print(f"Talking with {self.name}")
            print()
            for i,dialog in enumerate(self.dialog):
                print(f"{i}.\t{dialog}")
            print(f"{i+1}.\tLeave")
            sel = int(input("?"))
            if sel == quit_index:
                speaking = False
                break
            else:
                current_line = list(self.dialog.keys())[sel]
                print(f"{player.name}: {current_line}")
                for i,text in enumerate(self.dialog[current_line]):
                    if type(text) == Item:
                        player.addItem(text)
                        self.dialog[current_line][i] = "*You already obtained this item*"
                    else:
                        print(f"{self.name}: {text}")
                    input("...")
                input("*End of Dialog*")
"""  

class Shop(Person):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.inventory = []
    
    def Dialog(self, player):
        while 1:
            shop_menu = Menu(f"{self.name} Shop",choices=["Buy","Sell","Talk"])
            index,item = shop_menu.Show(f"{self.name}: How can I help you? ")
            if shop_menu.quit:
                break
            else:
                if item == "Buy":
                    buy_menu = Menu(f"Purchase Good ({self.name})",choices=[f"(${x.value}){x.name}" for x in self.inventory])
                    buy_index, buy_item = buy_menu.Show(f"What would you like to buy? ")
                    if buy_menu.quit:
                        return
                    else:
                        sel_item = self.inventory[buy_index]
                        if sel_item.value > player.money:
                            print(f"{self.name}: Sorry you dont have enough for that...")
                            input("...")
                            pass
                        else:
                            print(f"So you want to purchase {sel_item.name} for {sel_item.value} Gold?")
                            yes_no = Menu(f"Really purchase {sel_item.name} for {sel_item.value} Gold?",choices=["Yes","No"])
                            cho_index,_ = yes_no.Show("Confirm? ")
                            if yes_no.quit or cho_index == 1:
                                return
                            else:
                                input(f"...Confirmation Complete, Performing purchase of {sel_item.name}")
                                player.money -= sel_item.value
                                player.items.append(sel_item)
                                self.inventory.remove(sel_item)

                elif item == "Sell":
                    sell_menu = Menu(f"Sell Goods ({self.name})",choices=[f"(${x.value}){x.name}" for x in player.items])
                    sell_index, sell_item = sell_menu.Show(f"What are you looking to get rid of? ")
                    if sell_menu.quit:
                        return
                    else:
                        sel_item = player.items[sell_index]
                        print(f"So your looking to get rid of {sel_item.name}, ill give you {sel_item.value}")
                        yes_no = Menu(f"Really Sell {sel_item.name} for {sel_item.value}?",choices=["Yes","No"])
                        cho_index,_ = yes_no.Show("Confirm? ")
                        if yes_no.quit or cho_index == 1:
                            return
                        else:
                            input(f"Okay your hocking the {sel_item.name}")
                            player.money += sel_item.value
                            player.items.remove(sel_item)
                elif item == "Talk":
                    super().Dialog(player)