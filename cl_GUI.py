# Import important GUI modules.
import tkinter as tk
from tkinter import ttk

from cl_Room import mapList, buildMap, clearRooms
from cl_Game import GameSystem
from cl_Mob import mobList, teamList

# Configuration for inner/outer padding of items.
CONF_innerPad = 2
CONF_outerPad = 4

# Image Dictionary
# For static images like UI elements and HUD elements.
DICT_imgs = {"title":"./img/title.png",
             "map_placeholder":"./img/_nomap.png",
             "fighter_placeholder":"./img/_nofighter.png",
             
             # Icons
             "heart":"./img/stat_health.png",
             "skull":"./img/stat_",
             "atk":  "./img/stat_atk.png",
             "def":  "./img/stat_def.png",
             "agi":  "./img/stat_agi.png",
             "spd":  "./img/stat_spd.png",
             "mag":  "./img/stat_mag.png",
             "mdf":  "./img/stat_mdf.png",
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
             "mobSel_fighterList":"Fighter List",
             "mobSel_fighterBio":"Fighter Information",
             "mobSel_fighterAttacks":"Attacks",
             "mobSel_teamArrangement":"Team Setup",
             "mobSel_curMap":"Selected Map:",
             "mobSel_back":"Back to Map Selection",
             "mobSel_next":"Next",
             "teamSel_":"",
             "teamSel_":"",
             "teamSel_":"",
             "teamSel_":"",
             "teamSel_back":"Back to Fighter Selection",
             "teamSel_next":"Start the Fight!",
             "gameGuide_intro":"Welcome to the Battle Royale Game. This is a zero-player game that plays out automatically as computerised characters fight it out for your amusement.",
             "gameGuide_maps":"Maps are stored in the \'./maps\' directory. Maps have a list of rooms, their exits, and some metadata about the whole of the map.",
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
    
    def getCurrentMap(self):
        return self._gameSystem.currentMap

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
            
            master._gameSystem.updateCurrentMap(m)
            
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
        
        actFrame = tk.Frame(self)
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
        
        # Team Setup
        GUI_teamType = tk.StringVar()
        GUI_teamType.set("LMS")
        GUI_fCount = tk.IntVar()
        GUI_fCount.set(len(mobList))
        
        # Current Map
        GUI_curMap  = tk.StringVar()
        GUI_curMap.set(master.getCurrentMap())
        
        ## Functions ##
        ###############
        def callback(event=None):
            # Super simple callback function for whatever.
            print(event)
            return event        
        
        def updateFighter(event=None):
            if(len(fighterList.curselection()) > 0):
                self.fighterIndex = fighterList.curselection()[0]
            else:
                self.fighterIndex = 0
            
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
            
            try:
                fighterImg.config(file=mobList[self.fighterIndex].image)
            except:
                # Image not present. Change image to placeholder.
                fighterImg.config(file=DICT_imgs["fighter_placeholder"])
        
        def updateTeams(event=None):
            print(GUI_teamType.get())
        
        ## Widgets ##
        #############
        # Frame Setup
        fighterFrame = tk.LabelFrame(self,text=DICT_txts["mobSel_fighterBio"])
        teamFrame = tk.LabelFrame(self,text=DICT_txts["mobSel_teamArrangement"])
        listFrame = tk.LabelFrame(self,text=DICT_txts["mobSel_fighterList"])
        actionFrame = tk.Frame(self)
        
        fighterFrame.grid(row=0,column=0,sticky="nsew")
        teamFrame.grid(row=1,column=0,sticky="nsew")
        listFrame.grid(row=0,column=1,rowspan=2,sticky="nsew")
        actionFrame.grid(row=2,column=0,columnspan=2,sticky="nsew")
        
        # Sizing/Spacing for main widgets.
        self.grid_rowconfigure(0,minsize=120)
        self.grid_columnconfigure(0,minsize=480)
        
        # Figher Display Frame
        ######################
        try:
            fighterImg  = tk.PhotoImage(file=mobList[self.fighterIndex].image)
        except tk.TclError:
            # Image not present. Change image to placeholder.
            fighterImg  = tk.PhotoImage(file=DICT_imgs["fighter_placeholder"])
        fighterFace = tk.Label(fighterFrame,image=fighterImg)
        fighterFace.fighterImg = fighterImg
        
        # Fighter Details
        fighterName = tk.Label(fighterFrame,textvariable=GUI_fName)
        fighterShort= tk.Label(fighterFrame,textvariable=GUI_fSname)
        fighterDesc = tk.Label(fighterFrame,textvariable=GUI_fDesc,width=35)
        fighterDesc.config(wraplength=240,justify=tk.LEFT)
        
        # Labels + Stat Images
        icoATK      = tk.PhotoImage(file=DICT_imgs["atk"])
        icoDEF      = tk.PhotoImage(file=DICT_imgs["def"])
        icoAGI      = tk.PhotoImage(file=DICT_imgs["agi"])
        icoSPD      = tk.PhotoImage(file=DICT_imgs["spd"])
        icoMAG      = tk.PhotoImage(file=DICT_imgs["mag"])
        icoMDF      = tk.PhotoImage(file=DICT_imgs["mdf"])
        
        labATK      = tk.Label(fighterFrame,image=icoATK)
        labDEF      = tk.Label(fighterFrame,image=icoDEF)
        labAGI      = tk.Label(fighterFrame,image=icoAGI)
        labSPD      = tk.Label(fighterFrame,image=icoSPD)
        labMAG      = tk.Label(fighterFrame,image=icoMAG)
        labMDF      = tk.Label(fighterFrame,image=icoMDF)
        
        labATK.icoATK = icoATK
        labDEF.icoDEF = icoDEF
        labAGI.icoAGI = icoAGI
        labSPD.icoSPD = icoSPD
        labMAG.icoMAG = icoMAG
        labMDF.icoMDF = icoMDF
        
        # Stats
        fighterATK  = tk.Label(fighterFrame,textvariable=GUI_statATK)
        fighterDEF  = tk.Label(fighterFrame,textvariable=GUI_statDEF)
        fighterAGI  = tk.Label(fighterFrame,textvariable=GUI_statAGI)
        fighterSPD  = tk.Label(fighterFrame,textvariable=GUI_statSPD)
        fighterMAG  = tk.Label(fighterFrame,textvariable=GUI_statMAG)
        fighterMDF  = tk.Label(fighterFrame,textvariable=GUI_statMDF)
        
        atksLabel   = tk.Label(fighterFrame,text=DICT_txts["mobSel_fighterAttacks"])
        fighterAtks = tk.Listbox(fighterFrame,
                                 width=24,height=4,
                                 listvariable=GUI_attacks,
                                 selectmode="SINGLE",
                                 activestyle="dotbox")
        atkInfo     = tk.Label(fighterFrame)
        
        # Gridding Image
        fighterFace.grid(row=0,column=0,rowspan=5)
        
        # Gridding Main Details
        fighterName.grid(row=0,column=1,columnspan=2)
        fighterShort.grid(row=0,column=3,columnspan=2)
        fighterDesc.grid(row=1,column=1,columnspan=4)
        fighterDesc.grid_columnconfigure(1,minsize=480)
        
        # Gridding Statistics and Attacks
        labATK.grid(row=2,column=1)
        labDEF.grid(row=2,column=3)
        labAGI.grid(row=3,column=1)
        labSPD.grid(row=3,column=3)
        labMAG.grid(row=4,column=1)
        labMDF.grid(row=4,column=3)
        
        fighterATK.grid(row=2,column=2)
        fighterDEF.grid(row=2,column=4)
        fighterAGI.grid(row=3,column=2)
        fighterSPD.grid(row=3,column=4)
        fighterMAG.grid(row=4,column=2)
        fighterMDF.grid(row=4,column=4)
        
        atksLabel.grid(row=0,column=5)
        fighterAtks.grid(row=1,column=5,rowspan=3)
        atkInfo.grid(row=4,column=5)
        
        for c in [labATK,labDEF,labAGI,labSPD,labMAG,labMDF]:
            c.grid_configure(sticky="e")
        
        for c in [fighterATK,fighterDEF,fighterAGI,
                  fighterSPD,fighterMAG,fighterMDF]:
            c.grid_configure(sticky="w")
        
        # Team Setup/Game Mode Frame
        ############################
        # Radio Buttons
        it = 0
        for txt,var in [("Last Man Standing","LMS"),
                        ("Last Team Standing","LTS"),
                        ("Doubles/Duos","DUOS"),
                        ("Triples/Tris","TRIS"),
                        ("Quartets/Quads","QUADS")]:
            # Create buttons and grid them dynamically.
            b = tk.Radiobutton(teamFrame,text=txt,
                               variable=GUI_teamType,value=var,
                               command=updateTeams)
            b.grid(row=it,column=0, sticky="w")
            it += 1
        
        
        # Fighter List Frame
        ####################
        fighterScroll = tk.Scrollbar(listFrame)
        fighterList = tk.Listbox(listFrame,
                                 width=24,
                                 height=16,
                                 listvariable=GUI_fList,
                                 selectmode="SINGLE",
                                 activestyle="dotbox",
                                 yscrollcommand=fighterScroll.set)
        fighterScroll.config(command=fighterList.yview)
        fighterList.bind("<<ListboxSelect>>",updateFighter)

        fighterList.grid(row=0,column=0)
        fighterScroll.grid(row=0,column=1,sticky="wns")
        
        
        # Action Button Frame
        #####################
        backButton  = tk.Button(actionFrame,text=DICT_txts["mobSel_back"],
                                command=lambda: master.switchFrames(MapSelect))
        mapLabel    = tk.Label(actionFrame,text=DICT_txts["mobSel_curMap"])
        mapGUI      = tk.Label(actionFrame,textvariable=GUI_curMap)
        playButton  = tk.Button(actionFrame,text=DICT_txts["mobSel_next"],
                                command=lambda: master.switchFrames(TitleWin))
        
        backButton.grid(row=0,column=0)
        mapLabel.grid(row=0,column=1)
        mapGUI.grid(row=0,column=2)
        playButton.grid(row=0,column=3)
        
        ## Padding Gridding
        ###################
        for c in self.winfo_children():
            c.grid_configure(padx=CONF_innerPad,pady=CONF_innerPad)
        
        ## Last Functions
        #################
        updateFighter()
        updateTeams()
        

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
