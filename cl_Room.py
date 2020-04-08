#create CSV function to read/write rooms
import csv, os
import cl_Game

CONFIG_print = False

#Create room class
class Room(object):
    def __init__(self,roomID=-1,name="Blank",desc="Blank Description."):
        self.id = roomID #Gets filled in on creation via .csv read. -1 means room has no ID.
        self.name = name
        self.desc = desc
        self.exits = []
        self.mobs = []
        self.items = []
        self.hazards = []
        if(CONFIG_print): print("New room \""+str(self.name)+"\" was created.");

        # Statistics and Logging
        self.travelledTo = dict()
        self.travelledFrom = dict()
        self.attacksBy = dict()
        self.attacksOn = dict()
        self.pickupsDropped = []
        self.allHazards = []

    def __repr__(self):
        return self.name

    # Travel Metrics Adding
    def addToTravelledTo(self,r,c=1):
        if(str(roomList[r].name) in self.travelledTo):
            self.travelledTo[str(roomList[r])] += c
        else:
            self.travelledTo[str(roomList[r])] = c

    def addToTravelledFrom(self,r,c=1):
        if(str(roomList[r].name) in self.travelledFrom):
            self.travelledFrom[str(roomList[r])] += c
        else:
            self.travelledFrom[str(roomList[r])] = c

    # Attack Metrics
    def addToAttacksBy(self,m,c=1):
        if(str(m.name) in self.attacksBy):
            self.attacksBy[str(m.name)] += c
        else:
            self.attacksBy[str(m.name)] = c

    def addToAttacksOn(self,m,c=1):
        if(str(m.name) in self.attacksOn):
            self.attacksOn[str(m.name)] += c
        else:
            self.attacksOn[str(m.name)] = c

    #Rename room
    def rename(self,newName):
        if(isinstance(newName,str)):
            prevName = self.name
            self.name = newName
            if(CONFIG_print): print(prevName+" is now called "+newName)
        else:
            if(CONFIG_print): print("New name for "+self.name+" is not a string.")

    #Update room description
    def updateDescription(self,newDescription = None):
        if(isinstance(newDescription,str)):
            self.desc = newDescription
            if(CONFIG_print): print("Description for "+self.name+" successfully updated.")
        else:
            if(CONFIG_print): print("New description for "+self.name+" is not a string.")

    #Add Exit
    def addExit(self,newRoom,oneWay = True):
        #determine if new location is a location.
        if(isinstance(newRoom,Room)):
            #New exit can be created.
            self.exits.append(newRoom.id)
            if(CONFIG_print): print("New exit toward "+newRoom.name+" was added to "+self.name+".")

            #Add reciprocal exit if second argument is a true bool.
            if(isinstance(oneWay,bool)):
                if(oneWay == True):
                    #Add exit from new location to this one.
                    newRoom.exits.append(self.id)
                    if(CONFIG_print): print("New exit toward "+self.name+" was added to "+newRoom.name+" reciprocally.")
        else:
            #New exit cannot be created.
            if(CONFIG_print): print("Room \""+str(newRoom)+"\"does not exist or is not a location.")

        #Report new number of exits.
        if(CONFIG_print): print(self.name+" has "+str(len(self.exits))+" exit(s) now.")
        if(isinstance(oneWay,bool)):
            if(oneWay == True):
                if(CONFIG_print): print(newRoom.name+" has "+str(len(newRoom.exits))+" exit(s) now.")

    #Remove Exit
    def removeExit(self,removeRoom,oneWay):
        #Determine if location to remove is a location
        if(isinstance(removeRoom,Room)):
            #determine if given location exists in exit list.
            if(removeRoom.id in self.exits):
                #remove all exits to specified location.
                while(removeRoom.id in self.exits):
                    self.exits.remove(removeRoom.id)
                    if(CONFIG_print): print("Exit to "+str(removeRoom.name)+" has been removed.")

                #Reciprocally remove exit there
                if(isinstance(oneWay,bool)):
                    if(oneWay == True):
                        while(self.id in removeRoom.exits):
                            removeRoom.exits.remove(self.id)
                            if(CONFIG_print): print("Exit to "+str(self.name)+" has been removed reciprocally.")
            else:
                #Room does not exist in list.
                if(CONFIG_print): print(str(removeRoom.name)+" does not have an exit associated with "+self.name+".")
        else:
            if(CONFIG_print): print("Room \""+str(removeRoom)+"\" does not exist or is not a location.")

        #Report new number of exits.
        if(CONFIG_print): print(self.name+" has "+str(len(self.exits))+" exit(s) now.")
        if(isinstance(oneWay,bool)):
            if(oneWay == True):
                if(CONFIG_print): print(removeRoom.name+" has "+str(len(removeRoom.exits))+" exit(s) now.")

    # Get Exits
    def getExits(self):
        exitsPrint = ""
        for ex in self.exits:
            exitsPrint += roomList[ex].name+", "
        else:
            exitsPrint = exitsPrint[:-2]
            exitsPrint += "."
        return exitsPrint

class Hazard(object):
    def __init__(self,newName="16 Tonne Weight",tripChance=5,damSides=6,damDice=5,damMod=0):
        # Essentials
        self.trip = tripChance # Chance out of 20 when room entered, with rollDice function
        self.tripAdd = 0
        self.sides = damSides
        self.dice = damDice
        self.mod = damMod
        self.location = None
        self.expiry = 8
        self.killString = "was squished by"
        hazardList.append(self)

        # Stats
        self.createdOn = -1
        self.damageDone = dict()
        self.damageTargets = dict()
        self.kills = []

        # Decoration/etc.
        self.name = newName
        self.atkDesc = "flattens"
        self.desc = "An undescribed room hazard."

    def __repr__(self):
        return self.name

    def countDown(self):
        self.expiry -= 1
        self.tripAdd += 1
        if(self.expiry <= 0):
            print(self.name+" at "+self.location.name+" has expired!")
            self.remove()

    def remove(self):
        self.location.hazards.remove(self)
        hazardList.remove(self)

    def placeInRandomRoom(self):
        from random import randint
        goto = randint(0,len(roomList)-1)
        newRoom = roomList[goto]
        self.location = newRoom
        newRoom.hazards.append(self)
        newRoom.allHazards.append(self)
        print(self.name+" was added somewhere! ("+newRoom.name+")")

    def tripCheck(self):
        t = self.trip + self.tripAdd
        d = cl_Game.rollDice(20,1,0)
        if(d <= t):
            # Trip number rolled under
            # Activate hazard
            # Reset added likeliness to 0
            self.tripAdd = 0
            return True
        else:
            # Trip number rolled over
            # Don't activate hazard
            # make it more likely to activate next time
            self.tripAdd += 1
            return False

    def hazardActivate(self,target):
        from cl_Mob import Mob
        if(isinstance(target,Mob)):
            def addToTargets(h=self.damageTargets,c=1):
                if(str(target.name) in h):
                    h[str(target.name)] += c
                else:
                    h[str(target.name)] = c
            
            damage = cl_Game.rollDice(self.sides,self.dice,self.mod)
            if(target.buffTimer > 0 and target.buffType == "Defence"):
                damage = int(damage/2)

            target.hitpoints -= damage
            target.lastHitBy = "Room Hazard"
            target.lastHitWith = self
            addToTargets()
            addToTargets(self.damageDone,damage)
            print(self.name+" "+self.atkDesc+" "+target.name+" for "+str(damage)+" points of damage!")
            target.updateHitpoints()

            if(target.hitpoints <= 0):
                from random import choice
                #Apply Salvation Sphere effects if buff active
                if(target.buffTimer > 0 and target.buffType == "Salvation"):
                    print(target.name+"'s Salvation Sphere activates!")
                    target.alive = True
                    target.hitpoints = 25
                    target.buffType = None
                    target.buffTimer = 0
                    target.cheatedDeath += 1
                    target.healingGot += 25
                    target.updateHitpoints()
                    if(target.think(target.ai_talk) == True):
                        target.sayDoSomething(choice(target.readyStrings))
                else:
                    if(target.think(target.ai_talk) == True):
                        target.sayDoSomething(choice(target.loseStrings))
                    self.kills.append(target.name)
        else:
            pass

    def reportStats(self):
        print(self.name+" hazard statistics:")
        print("  TARGETS: "+str(self.damageTargets))
        if(len(self.damageDone)):
            print("  DAMAGE: "+str(self.damageDone))
        if(len(self.kills)):
            print("  KILLS: "+str(self.kills))

class Map(object):
    def __init__(self,
                 name="UNNAMED MAP",
                 shortName="NOSHORTS",
                 desc="Undescribed Map",
                 roomCount=-1,
                 minFighters=-1,
                 maxFighters=-1,
                 img=""):
        # Derived from CSV File
        self.name   = name
        self.sname  = shortName
        self.desc   = desc
        self.rCount = roomCount
        self.minFig = minFighters
        self.maxFig = maxFighters
        self.image  = img

        # Derived from Self/OS Functions
        self.path   = ""

    def __repr__(self):
        return self.name+" | "+self.sname

    def updateName(self,newName):
        # Update name.
        pass

    def updateShortName(self,newName):
        # Update short name.
        pass

    def updateDesc(self,newDesc):
        # Update description.
        pass

    def updatePath(self,newPath):
        # Update file path to Map.
        if(isinstance(newPath,str)):
            self.path = newPath
        else:
            pass        

####################
## Lone Functions ##
####################

def getMapFiles(md):
    ml = []
    mapFileList = os.scandir(mapDir)

    if(mapFileList == []):
        # No files at all in the map directory
        input("No files found in map directory! Cannot run a game without a map!\nPress [ENTER] to exit!")
        quit()
    
    else:
        # Read maps, create Map objects.
        for m in mapFileList:
            fileType = m.path.split(".")[-1]
            mi = []     # Map Info goes here, gets read sequentially.
            if(fileType == "csv"):
                # Double checked that its a CSV file being read...
                print("Found CSV File '"+m.name+"'. Adding to Maps...")
                with open(m, newline="") as mapFile:
                    # Open file, get dictionary reader.
                    mapReader = csv.DictReader(mapFile)
                    for r in mapReader:
                        # Check that the 'meta' row isn't empty.
                        if(r["meta"] != "" and r["meta"] != None):
                            # Add meta info to local map info list.
                            mi.append(r["meta"])
    
                    # Create new map object, write meta info into it
                    newMap = Map(mi[0], # Name
                                 mi[1], # Short Name
                                 mi[2], # Description
                                 mi[3], # Room Count
                                 mi[4], # Minimum Fighters
                                 mi[5], # Maximum Fighters
                                 mi[6]) # Image
                    # Get filepath for map, then append to Maps List.
                    newMap.updatePath(m.path)
                    ml.append(newMap)
            else:
                # Different file to a csv being read. Skip it.
                print("Found a non CSV file '"+m.name+"' in map directory. Skipping...")
                continue

    # No map files loaded
    if(ml == []):
        input("No maps found! Cannot run a game without a map!\nPress [ENTER] to exit!")
        quit()
    else:
        return ml

def mapSelection():
    # Create namelists for maps for map selection screen.
    mapNames    = []
    shortNames  = []
    mapToPick = None
    confirmed = None
    for m in mapList:
        mapNames.append(m.name)
        shortNames.append(m.sname)
    
    mapInfo = "Pick a Map by typing its short name.\nExample: "+shortNames[0]+" = "+mapNames[0]
    print(mapInfo)
    print(mapNames)
    print(shortNames)
    
    while(mapToPick == None):
        
        i = input(">")
        preInput = i.upper()
        
        if(preInput in shortNames):
            # Player entered a valid map name.
            mapIndex = shortNames.index(preInput)
    
            if(isinstance(mapList[mapIndex],Map)):
                mapToPick = mapList[mapIndex]
                print("You have chosen \'"+mapToPick.name+"\'.")
                print(mapToPick.desc)
                print("Rooms: "+str(mapToPick.rCount)+" | Min Fighters: "+str(mapToPick.minFig)+" | Max Fighters: "+str(mapToPick.maxFig))
                print("Would you like to fight on this map? (Y/N)")
                
                # Give additional map info, let player decide if its for them.
                while(confirmed == None):
                    pick = input(">")
                    if(pick.upper() == "Y"):
                        confirmed = True
                    elif(pick.upper() == "N"):
                        confirmed = False
                    else:
                        print("Please enter Y or N.")
                if(confirmed == True):
                    print("Map \'"+mapList[mapIndex].name+"\' selected!")
                    input("Press [ENTER] To Proceed!")
                else:
                    # While loop continues.
                    # Reset important loop deciders.
                    mapToPick = None
                    confirmed = None
    
                    print(mapInfo)
                    print(mapNames)
                    print(shortNames)
            else:
                print("Somehow, a non-map is in the map list. C'mon now...")
                quit()
            
            # Old code.
            #mapName = preInput[:-4]
            #print("Map \'"+mapName+"\' selected!")
            #input("Press [ENTER] To Proceed!")
            #mapToPick = preInput
        else:
            print("Not a valid Map!")

    roomCSV = mapToPick.path

    with open(roomCSV, newline="") as csvfile:
        #CSV Function to read rooms from a file
        print("CSV Room import function, starting on Static elements...")
    
        #pass through first time to populate static elements of rooms and add the rooms to roomlist
        reader = csv.DictReader(csvfile)
        for row in reader:
            newRoom = Room(int(row["id"]),row["name"],row["desc"])
            roomList.append(newRoom)
            #print("New room id: "+str(newRoom.id)+" appended to room list.")
        print(roomList)
        print("CSV Room import function, static elements finishing...")
    
    with open(roomCSV, newline="") as csvfile:
        #pass through a second time to add dynamic elements (mobs, objects, exits...)
        #(it would freak out if I did this before, as it would look for things that won't exist yet)
        print("CSV Room import function, starting on Dynamic elements...")
        reader = csv.DictReader(csvfile)
        for row in reader:
            RoomID = int(row["id"])
            updateRoom = roomList[RoomID]
    
            #Adding Reciprocal Exits
            if(row["exits_r"] != ""):
                exits = row["exits_r"]
                exitsList = exits.split("|")
                for newExit in exitsList:
                    updateRoom.addExit(roomList[int(newExit)],True)
    
            #adding One-Way exits.
            if(row["exits_s"] != ""):
                exits = row["exits_s"]
                exitsList = exits.split("|")
                for newExit in exitsList:
                    updateRoom.addExit(roomList[int(newExit)],False)
        
        print("CSV Room import function, dynamic elements finishing...")

#Add starting locations and exits
#Create indexed list for rooms to live in and reference from
mapDir = "./maps"

roomList = []
hazardList = []
mapList = getMapFiles(mapDir)
