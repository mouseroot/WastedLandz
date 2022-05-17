from os import system
import sys

MENU_SIZE = 50

class Menu:
  def __init__(self, title, choices=[],exit_text="Exit"):
    self.title = title
    self.choices = choices
    self.selection = 0
    self.quit = False
    self.exit_text = exit_text
    self.last_prompt = None
    self.sub_data = None
    
  def ReShow(self):
    self.Show(self.last_prompt)
    
  def Show(self, prompt="?"):
    """Shows the menu and returns the index and the item selected or -1,None if quit was selected
    """
    system("cls || clear")
    counter = 0
    self.last_prompt = prompt
    print(f'+{"-"*MENU_SIZE}+')
    if self.title != "":
      
      print(f'| {self.title}')
      print(f'+{"-"*MENU_SIZE}+')
    if self.sub_data:
        for d in self.sub_data:
            print(f'| {d}')
    
        print(f'+{"-"*MENU_SIZE}+')
    for index,cho in enumerate(self.choices):
      print(f"| {index}.  {cho}")
      counter=index
    print(f"| {counter+1}.  {self.exit_text}")
    print(f'+{"-"*MENU_SIZE}+')
    try:
        self.selection = int(input(f"| {prompt}"))
        if self.selection == counter+1:
            self.quit = True
            print(f'+{"-"*MENU_SIZE}+')
            return -1,None
        else:
            print(f'+{"-"*MENU_SIZE}+')
            try:
                return self.selection, self.choices[self.selection]
            except IndexError:
                return -1,None
    except ValueError:
        return -1,None
    
    
