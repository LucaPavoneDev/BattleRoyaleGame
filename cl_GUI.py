# Import important GUI modules.
import tkinter as tk
from tkinter import ttk

CONF_innerPad = 2
CONF_outerPad = 4

# Define basic window class.
############################
class Window(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.master = master

class MainScreen(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.master = master
        self.master.title("Battle Royale Game")
        self.currentScreen = tk.Toplevel(self.master)
        
        
        TitleScreen(self.master)

class TitleScreen(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.master = master
        self.window()
    
    def window(self):
        self.pack(fill="both",expand=1,padx=CONF_outerPad,pady=CONF_outerPad)
        
        # String Vars
        #############
        GUI_TestLabel = tk.StringVar()
        GUI_TestLabel.set = "I'm a banana!"
        
        
        # 
        ###########
        
        testLabel = tk.Label(self,textvariable=GUI_TestLabel)
        testLabel.grid(row=0,column=0)
        

def MapSelect():
    pass

def FighterSelect():
    pass

def TeamSelect():
    pass

def GameWindow():
    pass

root = tk.Tk()
app = MainScreen(root)
root.resizable(width=False, height=False)
root.geometry("800x600")
root.mainloop()