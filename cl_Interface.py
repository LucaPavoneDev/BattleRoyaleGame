import tkinter as tk

# Put root window down.
root = tk.Tk()

# Add top menu
menuBar  = tk.Menu(root)
fileMenu = tk.Menu(menuBar,tearoff=0)
fileMenu.add_command(label="Exit", command=root.quit)

menuBar.add_cascade(label="File", menu=fileMenu)

# Map List Scrollbar
mapScroll = tk.Scrollbar(root,jump=1)
mapScroll.pack(side="right", fill="y")

# Map Listing
mapList = tk.Listbox(root,height=5,width=40,selectmode="SINGLE",
                     yscrollcommand=mapScroll.set)
mapList.insert(1,"Banana!")
mapList.insert(2,"Apple!")
mapList.insert(3,"Mango!")
mapList.insert(4,"Tomato!")
mapList.insert(5,"Potato!")
mapList.insert(6,"Pepper!")
mapList.insert(7,"Horseradish!")
mapList.insert(8,"Berries!")
mapList.pack(side="left",fill="both")

# Configs before go time
mapScroll.config(command=mapList.yview)
root.config(menu=menuBar)

# do the thing.
root.mainloop()
