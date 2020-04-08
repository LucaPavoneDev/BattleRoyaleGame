# Import important GUI modules.
import tkinter as tk
from tkinter import ttk

from cl_Room import mapList
from cl_Game import GameSystem
from cl_Mob import mobList, teamList

# Configuration for inner/outer padding of items.
CONF_innerPad = 2
CONF_outerPad = 4

# Image Dictionary
# For static images like UI elements and HUD elements.
DICT_imgs = {"title":"./img/title.png",
             "map_placeholder":"./img/_nomap.png",
             "fighter_placeholder":"/img/_nofighter.png",
             }

# Text Dictionary
# For easier translation into different languages later.
DICT_txts = {"Title_newGame":"New Battle",
             "Title_gameGuide":"Game Guide",
             "Title_gameStats":"Game Statistics",
             "Title_quitGame":"Quit Game",
             "Title_language":"Change Language",
             "Title_copyright":"2019-2020, Luca Pavone",
             "MapSel_name":"Name:",
             "MapSel_sname":"Short Name:",
             "MapSel_desc":"Description:",
             "mapSel_rooms":"Room Count:",
             "mapSel_minMax":"Min./Max. Fighters:",
             "mapSel_back":"Back to Title",
             "mapSel_next":"Next",
             "mobSel_fighterList":"Fighters",
             "mobSel_fighterPics":"Fighter's Portraits",
             "mobSel_teamArrangement":"Team Setup",
             "mobSel_curMap":"Selected Map",
             "mobSel_":"",
             "mobSel_back":"Back to Map Selection",
             "mobSel_next":"Next",
             "teamSel_":"",
             "teamSel_":"",
             "teamSel_":"",
             "teamSel_":"",
             "teamSel_back":"Back to Fighter Selection",
             "teamSel_next":"Start the Fight!",
             "gameGuide_intro":"",
             "gameGuide_maps":"",
             "gameGuide_mobs":"",
             "gameGuide_modes":"",
             "gameGuide_rooms":"",
             "gameGuide_movement":"",
             "gameGuide_combat":"",
             "gameGuide_buffs":"",
             "gameGuide_hazards":"",
             "gameGuide_victory":"",
             "gameGuide_postgame":"",
             "gameGuide_":"",
             "gameGuide_":"",
             "gameGuide_":"",}

# Define basic window class and App
###################################
class Window(tk.Frame):
    def __init__(self,master=None):
        # Basically this to ensure the window always has a consistent title.
        # I could throw other 'global' things in here too.
        tk.Frame.__init__(self,master)
        self.master.title("Battle Royale Game")

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Current Frame
        self._screenFrame = None
        # Current Map
        self._gameSystem = GameSystem()
        
        # Initialise Frame
        self.switchFrames(TitleWin)
    
    def switchFrames(self,newClass):
        #print("Switching Frames...")
        #print(self.winfo_children())
        
        newFrame = newClass(self)
        if self._screenFrame is not None:
            #print("Destroying current Frame...")
            self._screenFrame.destroy()
        self._screenFrame = newFrame
        self._screenFrame.pack(fill="both",expand=1)
        
        #print(self.winfo_children())
        #print("Frames Switched.")

class TitleWin(Window):
    # Title Screen
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.pack(fill="both",expand=1,padx=CONF_outerPad,pady=CONF_outerPad)
        
        # Title Image
        #############
        titleImg = tk.PhotoImage(file=DICT_imgs["title"])
        titleLab = tk.Label(self,image=titleImg)
        titleLab.titleImg = titleImg
        
        titleLab.grid(row=0,column=0,columnspan=3,sticky="ew")
        
        # Labels and Buttons
        ####################
        newGame     = tk.Button(self,text=DICT_txts["Title_newGame"],
                                command=lambda: master.switchFrames(MapSelect))
        gameGuide   = tk.Button(self,text=DICT_txts["Title_gameGuide"],
                                command=lambda: master.switchFrames())
        gameStats   = tk.Button(self,text=DICT_txts["Title_gameStats"],
                                command=lambda: master.switchFrames())
        language    = tk.Button(self,text=DICT_txts["Title_language"],
                                command=lambda: master.switchFrames())
        quitGame    = tk.Button(self,text=DICT_txts["Title_quitGame"],
                                command=lambda: master.destroy())
        
        newGame.grid(row=1,column=1,sticky="ew")
        gameGuide.grid(row=2,column=1,sticky="ew")
        gameStats.grid(row=3,column=1,sticky="ew")
        language.grid(row=4,column=1,sticky="ew")
        quitGame.grid(row=5,column=1,sticky="ew")
        
        copyNote = tk.Label(self,text=DICT_txts["Title_copyright"])
        copyNote.grid(row=6,column=1)
        
        # Grid Padding Configuration
        ############################
        for c in self.winfo_children():
            c.grid_configure(padx=CONF_innerPad,pady=CONF_innerPad)

class MapSelect(Window):
    # Map Info Selection Screen
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.pack(fill="both",expand=1,padx=CONF_outerPad,pady=CONF_outerPad)
        self.mapIndex = 0
        
        ## GUI Variables ##
        ###################
        GUI_mList = tk.StringVar()
        GUI_mList.set(mapList)
        
        GUI_mapName  = tk.StringVar()
        GUI_mapShort = tk.StringVar()
        GUI_mapDesc  = tk.StringVar()
        GUI_mapRooms = tk.IntVar()
        GUI_maxMin   = tk.IntVar()
        GUI_mapImg   = tk.IntVar()
        
        ## Functions ##
        ###############
        
        def callback(event=None):
            # Super simple callback function for whatever.
            print(event)
            return event
        
        def setMapIndex():
            # Changes the Map Index variable.
            # Use curselection to get index
            if(len(mapselList.curselection()) > 0):
                self.mapIndex = mapselList.curselection()[0]
            else:
                self.mapIndex = 0
        
        def openMap(event=None):
            # Gets a maps variables and puts them in the GUI variables.
            # Uses the current mapIndex.
            setMapIndex()
            m = mapList[self.mapIndex]
            
            # Assign to GUI vars
            GUI_mapName.set(m.name)
            GUI_mapShort.set(m.sname)
            GUI_mapDesc.set(m.desc)
            GUI_mapRooms.set(m.rCount)
            GUI_maxMin.set(str(m.minFig)+" / "+str(m.maxFig))
            GUI_mapImg.set(m.image)
            
            try:
                mapImg.config(file=mapList[self.mapIndex].image)
            except:
                # Image not present. Change image to placeholder.
                mapImg.config(file=DICT_imgs["map_placeholder"])
            
        ## Widgets ##
        #############
        # Frame Setup
        #############
        mapFrame = tk.LabelFrame(self,text="Map Display",width=60)
        mapFrame.grid(row=0,column=0,columnspan=2,sticky="ns")
        
        optFrame = tk.LabelFrame(self,text="Map Selection")
        optFrame.grid(row=0,column=2,sticky="ns")
        
        actFrame = tk.LabelFrame(self,text="Actions")
        actFrame.grid(row=1,column=0,columnspan=3,sticky="ew")
        
        # Map Display Frame
        ###################
        #mapImg = tk.PhotoImage(file=)
        #mapImg = tk.Label(mapFrame,image=titleImg)
        #titleLab.titleImg = titleImg
        
        mapNameLab = tk.Label(mapFrame,text=DICT_txts["MapSel_name"])
        mapNameDis = tk.Label(mapFrame,textvariable=GUI_mapName)
        mapNameLab.grid(row=0,column=0)
        mapNameDis.grid(row=0,column=1)
        
        mapShortLab = tk.Label(mapFrame,text=DICT_txts["MapSel_sname"])
        mapShortDis = tk.Label(mapFrame,textvariable=GUI_mapShort)
        mapShortLab.grid(row=1,column=0)
        mapShortDis.grid(row=1,column=1)
        
        mapDescLab  = tk.Label(mapFrame,text=DICT_txts["MapSel_desc"])
        mapDescDis  = tk.Label(mapFrame,textvariable=GUI_mapDesc)
        mapDescDis.config(wraplength=240,justify=tk.LEFT)
        mapDescLab.grid(row=2,column=0)
        mapDescDis.grid(row=2,column=1)
        
        mapRoomsLab = tk.Label(mapFrame,text=DICT_txts["mapSel_rooms"])
        mapRoomsDis = tk.Label(mapFrame,textvariable=GUI_mapRooms)
        mapRoomsLab.grid(row=3,column=0,sticky="w")
        mapRoomsDis.grid(row=3,column=1)
        
        mapMobLab   = tk.Label(mapFrame,text=DICT_txts["mapSel_minMax"])
        mapMobDis   = tk.Label(mapFrame,textvariable=GUI_maxMin)
        mapMobLab.grid(row=4,column=0)
        mapMobDis.grid(row=4,column=1)
        
        # Load first map's image in immediately to prevent
        # the program from falling over itself.
        mapImg      = tk.PhotoImage(file=mapList[self.mapIndex].image)
        mapImgLab   = tk.Label(mapFrame,image=mapImg)
        mapImgLab.mapImg = mapImg
        mapImgLab.grid(row=5,column=0,columnspan=2)
        
        for c in mapFrame.winfo_children():
            c.grid_configure(sticky="wn")
        # Exceptions for the min/max mob count and map image
        mapImgLab.grid_configure(sticky="wens")
        
        # Option Display Frame
        ######################
        mapselLabel = tk.Label(optFrame,text="Your Maps")
        mapselLabel.grid(row=0,column=0,columnspan=2,sticky="ew")
        
        mapselScroll    = tk.Scrollbar(optFrame)
        mapselList      = tk.Listbox(optFrame,
                                     width=32,height=24,
                                     listvariable=GUI_mList,
                                     selectmode="SINGLE",
                                     activestyle="dotbox",
                                     yscrollcommand=mapselScroll.set)
        mapselScroll.config(command=mapselList.yview)
        mapselList.grid(row=1,column=0)
        mapselScroll.grid(row=1,column=1,sticky="ns")
        mapselList.bind("<<ListboxSelect>>",openMap)
        
        # Action Display Frame
        backButton = tk.Button(actFrame,text=DICT_txts["mapSel_back"],
                               command=lambda: master.switchFrames(TitleWin))
        nextButton = tk.Button(actFrame,text=DICT_txts["mapSel_next"],
                               command=lambda: master.switchFrames(FighterSelect))
        
        backButton.grid(row=0,column=0,sticky="we")
        nextButton.grid(row=0,column=2,sticky="we")

        # Grid Padding Configuration
        ############################
        # First, the three main frames of the window.
        for c in self.winfo_children():
            c.grid_configure(padx=CONF_innerPad,pady=CONF_innerPad)
        # Then the children of those three frames.
        for c in mapFrame.winfo_children():
            c.grid_configure(padx=CONF_innerPad,pady=CONF_innerPad)
        for c in optFrame.winfo_children():
            c.grid_configure(padx=CONF_innerPad,pady=CONF_innerPad)
        for c in actFrame.winfo_children():
            c.grid_configure(padx=CONF_innerPad,pady=CONF_innerPad)
        openMap()

class FighterSelect(Window):
    # Fighter Inspection Screen and Team Building
    def __init__(self,master=None):
        Window.__init__(self,master)
        self.pack(fill="both",expand=1,padx=CONF_outerPad,pady=CONF_outerPad)
        self.fighterIndex = 0
        
        ## GUI Variables ##
        ###################
        # Fighter List
        GUI_fList   = tk.StringVar()
        GUI_fList.set(mobList)
        
        # Fighter Details
        GUI_fName   = tk.StringVar()
        GUI_fSname  = tk.StringVar()
        GUI_fDesc   = tk.StringVar()
        GUI_attacks = tk.StringVar()
        
        # Fighter Statistics
        GUI_statATK = tk.IntVar()
        GUI_statDEF = tk.IntVar()
        GUI_statAGI = tk.IntVar()
        GUI_statSPD = tk.IntVar()
        GUI_statMAG = tk.IntVar()
        GUI_statMDF = tk.IntVar()
        
        ## Functions ##
        ###############
        def callback(event=None):
            # Super simple callback function for whatever.
            print(event)
            return event
        
        def updateFighterIndex(event=None):
            # Update fighter index based on position of a listbox later.
            self.fighterIndex = 0
        
        def updateFighter(event=None):
            fi = self.fighterIndex
            
            GUI_fName.set(mobList[fi].name)
            GUI_fSname.set(mobList[fi].sname)
            GUI_fDesc.set(mobList[fi].desc)
            GUI_attacks.set(mobList[fi].attacks)
            
            stats = mobList[fi].stats
            
            GUI_statATK.set(stats["ATK"])
            GUI_statDEF.set(stats["DEF"])
            GUI_statAGI.set(stats["AGI"])
            GUI_statSPD.set(stats["SPD"])
            GUI_statMAG.set(stats["MAG"])
            GUI_statMDF.set(stats["MDF"])
        
        ## Widgets ##
        #############
        # Frame Setup
        fighterFrame = tk.LabelFrame(self,text="Fighter Display")
        fighterFrame.grid(row=0,column=0)
        
        teamFrame = tk.Frame(self)
        teamFrame.grid(row=1,column=0)
        
        listFrame = tk.Frame(self)
        listFrame.grid(row=0,column=1,rowspan=2)
        
        actionFrame = tk.Frame(self)
        actionFrame.grid(row=2,column=0,columnspan=2)
        
        # Figher Display Frame
        ######################
        fighterImg  = tk.PhotoImage(file=mapList[self.fighterIndex].image)
        
        # Team Setup/Game Mode Frame
        ############################
        
        # Fighter List Frame
        ####################
        
        # Action Button Frame
        #####################
        

class GameGuide(Window):
    # Game Information/Rundown/Help Area
    def __init__(self,master=None):
        Window.__init__(self,master)
        pass

class GameWindow(Window):
    def __init__(self,master=None):
        Window.__init__(self,master)
        pass










# Create Sub-Windows to Move THrough
#################

def startGUI():
    app = MainApp()
    app.resizable(width=False, height=False)
    #app.geometry("800x600")
    app.mainloop()
    return app

'''
app = MainApp()
app.resizable(width=False, height=False)
#app.geometry("800x600")
app.mainloop()
'''
