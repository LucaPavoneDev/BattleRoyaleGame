# Dice rolling/random chance function
def rollDice(sides=6, number=1, mod=0):
    total = 0
    add = 0
    rolls = []
    for i in range(number):
        add = randint(1,sides)
        total += add
        rolls.append(add)
    total = total + mod
    #print(str(total-mod)+"("+str(mod)+")"+str(rolls))
    return total

# Import all the useful bobbinses.
from random import randint
from random import choice
from random import shuffle
from time import sleep
from cl_Room import roomList
from cl_Room import hazardList
from cl_Mob import mobList
from cl_Mob import teamList
from cl_Items import itemList

class GameSystem(object):
    def __init__(self):
        # Init game control systems
        self.turnCounter = 0
        self.maxTurns = -1

        # Fighter, Team and Turn Order tracking.
        self.fighterList    = mobList.copy()
        self.teamsList      = teamList.copy()
        self.turnOrder      = self.fighterList.copy()
        self.teamsList      = []    # This gets filled in when needed.

        # Dead Lists
        self.deadList       = []
        self.deadTeams      = []

        # Individual Death Statistics
        self.diedOn         = []
        self.diedWhere      = []
        self.killedBy       = []
        self.killedWith     = []

        # Game Modes
        self.gameOn = True
        self.gameMode = ""
        self.allModes = ["LMS","LTS","DUOS","TRIS","QUADS"]

        # Game Options
        # Randomly dropped items and hazard options.
        # Higher numbers = more time needed/more dice rolled between spawns.
        self.randomDrops = {"pf":1,"hf":2,"p":1,"h":1}
        # pf = first powerup. hf = first hazard.
        # p = subsequent powerups. h = subsequent hazards
        # Where these dice go:
        self.powerupDropIn = rollDice(6,self.randomDrops["pf"])
        self.newHazardIn = rollDice(6,self.randomDrops["hf"])

        # Visuals
        self.sep = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
        self.smallSep = "  -=-=-=-=-=-=-"

        print("Game System Initialised!")

    def selectGameMode(self):
        gameModeChosen = False
        # Put in default choices.
        choices = ["LAST MAN STANDING"]
        shorts = ["LMS"]
        # Check fighter count and add extra modes.
        fCount = len(self.fighterList)
        if(fCount % 2 == 0):
            if(fCount >= 10):
                # 10+ players. Roll out Last Team Standing Match!
                choices.append("LAST TEAM STANDING")
                shorts.append("LTS")
            # Even Number. Eligible to do pairs.
            choices.append("DOUBLES BATTLE")
            shorts.append("DUOS")
        if(fCount % 3 == 0):
            # Dividable by 3. Can do trios.
            choices.append("TRIPLES BATTLE")
            shorts.append("TRIS")
        if(fCount % 4 == 0):
            # Dividable by 4. Go for quads.
            choices.append("QUARTETS BATTLE")
            shorts.append("QUADS")
        
        question = ("Choose a Game Mode. There are "+str(fCount)+" fighters.\n"+str(choices)+
                    "\n"+str(shorts)+"\nEnter a choice or a shorthand.")
        print(question)
        while(gameModeChosen == False):
            choice = input(">").upper()
            if(choice == ""):
                # Empty default.
                # Repeat question.
                continue
            elif(choice in shorts or choice in choices):
                # What they entered is a shorthand or full name.
                if(choice == "LAST MAN STANDING" or choice == "LMS"):
                    self.gameMode = "LMS"
                if(choice == "LAST TEAM STANDING" or choice == "LTS"):
                    self.gameMode = "LTS"
                if(choice == "DOUBLES BATTLE" or choice == "DUOS"):
                    self.gameMode = "DUOS"
                if(choice == "TRIPLES BATTLE" or choice == "TRIS"):
                    self.gameMode = "TRIS"
                if(choice == "QUARTETS BATTLE" or choice == "QUADS"):
                    self.gameMode = "QUADS"
                input("Game Mode is now '"+self.gameMode+"'. [Hit ENTER]")
                
                gameModeChosen = True
            else:
                # They entered something else completely.
                # Repeat question!
                continue

    def pregameTeamAssignment(self,originalTeams=teamList):
        self.teamsList = originalTeams.copy()
        gm = self.gameMode
        fl = self.fighterList
        perTeam = 0
        teamsNeeded = 0
        
        if(gm == "LMS"):
            # Default Game Mode
            # Do not assign any teams. Its everyone for themselves.
            print("It's everyone for themselves in this mode.")
        else:
            # Team based mode.
            if(gm == "LTS"):
                # Split characters into two large teams.
                perTeam = int(len(fl)/2)
                teamsNeeded = 2
                print("We're splitting our contestants into two even teams.")
            elif(gm == "DUOS"):
                # Split characters into teams of two each.
                perTeam = 2
                teamsNeeded = int(len(fl)/perTeam)
                print("Our contestants will be put in groups of two.")
            elif(gm == "TRIS"):
                # Split characters into teams of three each.
                perTeam = 3
                teamsNeeded = int(len(fl)/perTeam)
                print("Our contestants will be put in groups of three.")
            elif(gm == "QUADS"):
                # Split characters into teams of four each.
                perTeam = 4
                teamsNeeded = int(len(fl)/perTeam)
                print("Our contestants will be put in groups of four.")

            input("We'll need "+str(teamsNeeded)+" teams for "
                  +str(perTeam)+" fighters each. [Hit ENTER]")

            # Scramble fighter list to jumble teams
            # instead of linearly assigning them.
            shuffle(fl)
            shuffle(self.teamsList)

            self.teamsList = self.teamsList[:teamsNeeded]

            # Assign mobs to teams
            for m in fl:
                for t in self.teamsList:
                    if(len(t.members) < perTeam and m.team == None):
                        # Team doesn't have enough members and mob isn't assigned.
                        # Let us change that.
                        t.addMember(m)
                        t.updateStatus()
            
            # Put fighter list back in team order.
            fl.sort(key=lambda Mob: Mob.id)
            print("Your Teams For This Fight Are...\n"+str(self.teamsList))
        input("Teams are now sorted. [Hit ENTER]")

    def scrambleFighterLocations(self):
        for i in self.fighterList:
            roomToPick = randint(0,len(roomList)-1)
            currentRoom = roomList[roomToPick]
            i.placeInRoom(currentRoom,False)
            print(currentRoom.desc)
            print(self.smallSep)

    def scrambleTurnOrder(self):
        return shuffle(self.turnOrder)

    def incrementTurnCounter(self):
        self.turnCounter += 1
        return self.turnCounter

    def itemCountdown(self):
        # Count down existing items on field, drop new powerup
        for it in itemList:
            it.countDown()
            
        self.powerupDropIn -= 1
        if(self.powerupDropIn > 0):
            pass
        else:
            self.spawnItem()
            self.powerupDropIn = rollDice(6,self.randomDrops["p"])
        print("New powerup dropping in "+str(self.powerupDropIn)+" turns!")
        sleep(1.5)

    def hazardCountdown(self):
        # Count down existing hazards on field, drop new hazard
        for haz in hazardList:
            haz.countDown()
            
        self.newHazardIn -= 1
        if(self.newHazardIn > 0):
            pass
        else:
            self.spawnHazard()
            self.newHazardIn = rollDice(6,self.randomDrops["h"])
        print("New hazard appearing in "+str(self.newHazardIn)+" turns!")

    def spawnItem(self):
        # Spawn a random item on the field.
        import cl_Items as it
        from random import choice
        itemRange = ["h","h","h","h","h","h","H","H","H","H",
                     "d","a","t","s","S","r","r","i","w","w"]
        itemType = choice(itemRange)
        if(itemType == "h"):
            newItem = it.healthPickup()
        elif(itemType == "H"):
            newItem = it.healthPickup(30)
            newItem.name = "Big Health Pack"
        elif(itemType == "d"):
            newItem = it.defenceBuff()
        elif(itemType == "a"):
            newItem = it.attackBuff()
        elif(itemType == "t"):
            newItem = it.teleportPickup()
        elif(itemType == "s"):
            newItem = it.speedBuff()
        elif(itemType == "S"):
            newItem = it.salvationBuff()
        elif(itemType == "r"):
            newItem = it.regenBuff()
        elif(itemType == "i"):
            newItem = it.invisibleBuff()
        elif(itemType == "w"):
            newItem = it.warningBuff()
        else:
            #If not found, default to health pickup
            newItem = it.healthPickup()
        newItem.placeInRandomRoom()
        newItem.createdOn = self.turnCounter
        return newItem

    def spawnHazard(self):
        # Spawn a random hazard on the field
        import cl_Room as ro
        newHazard = ro.Hazard()
        newHazard.name = choice([
            "16 Tonne Weight","Blunt, Heavy Object","Herd of Cattle",
            "Hell's Grannies","Crunchy Frog","George Crushington",
            "Spiny Norman","Blancmange","Scotsmen","Australia",
            "Rolling Boulder","Dirty Fork","Alien Invaders",
            "Keep Left Sign","Stompy Foot","Architects"])
        newHazard.placeInRandomRoom()
        newHazard.createdOn = self.turnCounter
        return newHazard
    
    def fighterTurns(self):
        for f in self.turnOrder:
            f.playGame()
            if(f.buffType == "Speed"):
                # Speed Sphere allows for second turn.
                f.playGame()
            f.countDownBuff()
            if(f not in self.deadList):
                f.hpPerRound.append(f.hitpoints)
                print(self.smallSep)
                sleep(1.5)

    def matchStatus(self):
        gm = self.gameMode
        gameModes = ["LTS","DUOS","TRIS","QUADS"]
        
        # Should update this to do teamplay display.
        print(self.sep)
        print("  CURRENT TURN: "+str(self.turnCounter))
        print(self.smallSep)
        if(gm in gameModes):
            # Teams are enabled. List in team order.
            for t in self.teamsList:
                for f in t.members:
                    if(f not in self.deadList):
                        f.reportStatus()
                        print(self.smallSep)
                        sleep(0.75)
                print(self.smallSep)
        else:
            # No Teams. List fighters individually in ID order.
            for f in self.fighterList:
                if(f not in self.deadList):
                    f.reportStatus()
                    print(self.smallSep)
                    sleep(0.75)

    def showItems(self):
        if(len(itemList)):
            print(self.sep)
            print("  ITEMS ON BATTLEFIELD")
            for it in itemList:
                print(it.name+" located in "+it.location.name+" ("+str(it.lifeTime)+" turns left to get)")
            else:
                print(self.smallSep)

    def showHazards(self):
        if(len(hazardList)):
            print(self.sep)
            print("  HAZARDS ON BATTLEFIELD")
            for haz in hazardList:
                print(haz.name+" located in "+haz.location.name+" ("+str(haz.expiry)+" turns until expiry)")
            else:
                print(self.smallSep)

    def updateFighterStatus(self):
        gm = self.gameMode
        gameModes = ["LTS","DUOS","TRIS","QUADS"]
        
        # Add dead fighters to the figher list.
        for f in self.fighterList:
            if(f.alive == False and f not in self.deadList):
                self.deadList.append(f)
                self.diedOn.append(self.turnCounter)
                self.diedWhere.append(f.location)
                self.killedBy.append(f.lastHitBy)
                self.killedWith.append(f.lastHitWith)
                fightersLeft = len(self.fighterList)-len(self.deadList)
                # Print obituary
                print(f.name+" "+f.lastHitWith.killString+" "+str(f.lastHitBy)
                      +"'s "+str(f.lastHitWith)+". "+str(fightersLeft)+" fighters remain.")

        # If teamplay is on, add dead teams to list
        if(gm in gameModes):
            for t in self.teamsList:
                if(t.updateStatus() == False and t not in self.deadTeams):
                    self.deadTeams.append(t)
                    # print Obituary
                    teamsLeft = len(self.teamsList)-len(self.deadTeams)
                    print(t.name+" Team has been wiped out. "+str(teamsLeft)+" teams remain.")
        
        # Check if only 1 person is left alive in Last Man Standing.
        # Check if one team is left alive in team games.
        if(gm in gameModes):
            if(len(self.deadTeams) >= len(self.teamsList)-1):
                for f in self.fighterList:
                    if(f.alive == True and f.team.updateStatus() == True):
                        f.sayDoSomething(choice(f.winStrings))
                self.gameOn = False
        elif(gm == "LMS"):
            if(len(self.deadList) >= len(self.fighterList)-1):
                for f in self.fighterList:
                    if(f.alive == True):
                        f.sayDoSomething(choice(f.winStrings))
                self.gameOn = False
        
    def fighterMetrics(self):
        # Put these here and alias them cause its easier.
        fl = self.fighterList
        dl = self.deadList
        do = self.diedOn
        dw = self.diedWhere
        kb = self.killedBy
        kw = self.killedWith
        tc = self.turnCounter
        
        for i in fl:
            if(i in dl):
                print(i.name+": DEAD.")
                di = dl.index(i)
                print("Killed by "+str(kb[di])+" with "+str(kw[di]))
                print("Died on turn: "+str(do[di])+" | Died at: "+str(dw[di]))
            else:
                print(i.name+": ALIVE!")
                print("Survived for "+str(tc)+" turns.")
            print("Items Grabbed: "+str(i.itemsGot))
            if(i.healingGot > 0):
                print("Healing Received: "+str(i.healingGot))
            if(i.cheatedDeath > 0):
                print(i.name+" cheated death "+str(i.cheatedDeath)+" times!")
            print(self.sep)
            
            i.reportAttackStats()
            
            print(self.sep)
            print(i.name+"'s Travel statistics (By ID):")
            print("  "+str(i.travel))
            
            # using funny non-statistics mode function since it keeps
            # freaking out when there's more than one mode in the data
            print("  Travel Distance: "+str(i.travelSteps)+" Steps")
            favRoom = max(i.travel, key=i.travel.count)
            print("  Favourite Room: "+str(roomList[favRoom].name))
            if(len(i.travelFight) > 0):
                fightRoom = max(i.travelFight, key=i.travelFight.count)
                print("  Room Most Attacks Made In: "+str(roomList[fightRoom].name))
            if(len(i.travelAttacked) > 0):
                attackRoom = max(i.travelAttacked, key=i.travelAttacked.count)
                print("  Room Most Attacked In: "+str(roomList[attackRoom].name))
            input("Hit [ENTER] to see next fighter.")
            print(self.sep)

    def roomMetrics(self):
        for r in roomList:
            print(self.sep)
            print("Statistics for Room \'"+r.name+"\' | ID: "+str(r.id))
            print("Room Exits: "+r.getExits())
            print(self.smallSep)
            print("Movements To: "+str(r.travelledTo))
            print("Movements From: "+str(r.travelledFrom))
            print(self.smallSep)
            print("Attacks By: "+str(r.attacksBy))
            print("Attacks On: "+str(r.attacksOn))
            print(self.smallSep)
            print("Pickups Placed Here: "+str(r.pickupsDropped))
            print(self.smallSep)
            print("Hazards Placed Here: "+str(r.allHazards))
            for ah in r.allHazards:
                ah.reportStats()
            print(self.smallSep)
            input("Hit [ENTER] to see Next Room")
        else:
            print(self.sep)

    def totalMetrics(self):
        # Fighter metrics
        f_totalHits     = 0
        f_totalMisses   = 0
        f_totalDamage   = 0
        f_totalMoves    = 0
        f_totalHeals    = 0
        f_totalSalvs    = 0

        for fl in self.fighterList:
            f_totalHeals += fl.healingGot
            f_totalSalvs += fl.cheatedDeath
            f_totalMoves += fl.travelSteps
            for at in fl.attacks:
                f_totalHits += at.hits
                f_totalMisses += at.misses
                f_totalDamage += at.damage

        print("OVERALL FIGHTER DATA")
        print("  TURNS TAKEN:         "+str(self.turnCounter))
        print("  TOTAL ATTACKS:       "+str(f_totalHits+f_totalMisses))
        print("  TOTAL HITS:          "+str(f_totalHits))
        print("  TOTAL MISSES:        "+str(f_totalMisses))
        print("  HIT RATIO:           "+str(float(f_totalHits/f_totalMisses)))
        print("  TOTAL DAMAGE:        "+str(f_totalDamage))
        print("  DAMAGE PER FIGHTER:  "+str(float(f_totalDamage/len(self.fighterList))))
        print("  DAMAGE PER TURN:     "+str(float(f_totalDamage/self.turnCounter)))
        print("  ATTACKS PER FIGHTER: "+str(float((f_totalHits+f_totalMisses)/len(self.fighterList))))
        print("  ATTACKS PER TURN:    "+str(float((f_totalHits+f_totalMisses)/self.turnCounter)))
        print("  TOTAL MOVEMENTS:     "+str(f_totalMoves))
        print("  TOTAL HEALING:       "+str(f_totalHeals))
        print("  SALVATIONS:          "+str(f_totalSalvs))
        
        print("\nINDIVIDUAL FIGHTER OBSERVATIONS/COMMENTARY")
        # Item related achievements/accolades
        import cl_Items as it
        for fl in self.fighterList:
            print(self.smallSep)
            
            ind_kills   = 0
            ind_damage  = 0
            ind_hits    = 0
            ind_misses  = 0
            ind_team    = fl.team
            ind_heals   = fl.healingGot
            ind_travel  = fl.travelSteps
            ind_hazards = fl.hazardsTripped
            ind_avoids  = fl.hazardsAvoided
            for at in fl.attacks:
                ind_kills   += len(at.kills)
                ind_damage  += at.damage
                ind_hits    += at.hits
                ind_misses  += at.misses

            # Team
            if(ind_team != None):
                print(fl.name+" was a member of "+str(ind_team)+".")
            else:
                # Character is not part of a team.
                pass
            
            # Kills
            if(ind_kills == 1):
                print(fl.name+" got a single kill.")
            elif(ind_kills == 2):
                print(fl.name+" got a twofer.")
            elif(ind_kills == 3):
                print(fl.name+" bagged them a threefer!")
            elif(ind_kills == 4):
                print(fl.name+" killed four others!")
            elif(ind_kills == 5):
                print("JEY-SUS! "+fl.name+" got five of 'em!")
            elif(ind_kills >= 6):
                print(fl.name+" went on a rampage and got "+str(ind_kills)+" kills!")

            # Damage
            if(ind_damage >= 250):
                print(fl.name+" was beyond unstoppable, dealing 250+ damage or more!")
            elif(ind_damage >= 225):
                print(fl.name+" was ripping and tearing, dealing 225+ damage!")
            elif(ind_damage >= 200):
                print(fl.name+" couldn't be restrained from violence, dealing 200+ damage!")
            elif(ind_damage >= 175):
                print(fl.name+" was destroying the joint, dealing 175+ damage!")
            elif(ind_damage >= 150):
                print(fl.name+" was a walking disaster zone, dealing 150+ damage!")
            elif(ind_damage >= 125):
                print(fl.name+" was running riot, dealing 125+ damage!")
            elif(ind_damage >= 100):
                print(fl.name+" was kicking ass and taking names, dealing 100+ damage!")
            elif(ind_damage >= 75):
                print(fl.name+" smashed their way through, dealing 75+ damage!")
            elif(ind_damage >= 50):
                print(fl.name+" did lots of damage to others, dealing 50+ damage.")
            elif(ind_damage >= 25):
                print(fl.name+" fought the others a bit, dealing 25+ damage.")
            elif(ind_damage >= 15):
                print(fl.name+" didn't fight the others very much, only getting 15+ damage.")
            elif(ind_damage > 0):
                print(fl.name+" barely fought at all, dealing less than 15 damage...")
            else:
                print(fl.name+" didn't deal any damage at all.")

            # Healing
            if(ind_heals == 0):
                pass
                #print(fl.name+" didn't heal themselves during the fight.")
            elif(ind_heals > 75):
                print(fl.name+" applied massive healing (>75) to themselves!")
            elif(ind_heals > 50):
                print(fl.name+" applied major healing (>50) to themselves!")
            elif(ind_heals > 25):
                print(fl.name+" applied moderate healing (>25) to themselves.")
            elif(ind_heals >= 15):
                print(fl.name+" applied minor healing (>15) to themselves.")
            elif(ind_heals < 15):
                print(fl.name+" applied miniscule healing (<15) to themselves.")

            # Hits and Misses
            if(ind_hits > 0):
                if(ind_misses > 0):
                    # Two if statements here to avoid dividing by zero.
                    hitRatio = float(ind_hits/ind_misses)
                    if(hitRatio <= 0.25):
                        print(fl.name+" couldn't hit the broad side of a barn.")
                    elif(hitRatio <= 0.50):
                        print(fl.name+" wasn't a consistent hitter.")
                    elif(hitRatio <= 0.75):
                        print(fl.name+" had a below average hit ratio.")
                    elif(hitRatio <= 1.00):
                        print(fl.name+" was around one for one on hits and misses.")
                    elif(hitRatio <= 1.25):
                        print(fl.name+" was above average for hits to misses.")
                    elif(hitRatio <= 1.50):
                        print(fl.name+" had a good hitting ratio.")
                    elif(hitRatio <= 1.75):
                        print(fl.name+" had a great hitting ratio.")
                    elif(hitRatio <= 2.50):
                        print(fl.name+" was two-for-one on hits!")
                    elif(hitRatio <= 3.50):
                        print(fl.name+" was three-for-one on hits!")
                    elif(hitRatio <= 4.50):
                        print(fl.name+" was four-for-one on hits!")
                    elif(hitRatio <= 5.50):
                        print(fl.name+" was five-for-one on hits!")
                    else:
                        print(fl.name+" was over five-for-one on hits!")
                else:
                    print(fl.name+" landed all of their attacks! How accurate!")
            else:
                print(fl.name+" didn't land a single one of their attacks...")

            # Travel
            if(ind_travel):
                if(ind_travel < 6):
                    print(fl.name+" barely moved during the fight.")
                elif(ind_travel < 12):
                    print(fl.name+" walked a short distance during the fight.")
                elif(ind_travel < 18):
                    print(fl.name+" jogged a medium distance during the fight.")
                elif(ind_travel < 24):
                    print(fl.name+" ran a long distance during the fight.")
                elif(ind_travel < 30):
                    print(fl.name+" wandered very long distance during the fight.")
                elif(ind_travel >= 36):
                    print(fl.name+" went an extremely long distance during the fight.")
            else:
                print(fl.name+" didn't move at all during the fight.")

            # Hazard Trips/Avoids
            from cl_Room import Hazard
            if(ind_hazards > 0):
                print(fl.name+" tripped "+str(ind_hazards)+" hazards.")
            if(ind_avoids > 0):
                print(fl.name+" avoided "+str(ind_avoids)+" hazards.")
            if(isinstance(fl.lastHitWith,Hazard) and fl.alive == False):
                print(fl.name+" was killed by a hazard. Oopsy doodle.")

            # Item related achievements
            for its in fl.itemsGot:
                # Died while Regenerating
                if(isinstance(its,it.regenBuff)):
                    if(fl.buffType == "Regen" and fl.alive == False):
                        print(fl.name+" died while regenerating health! Oh dear!")
                # Salvation Sphere Comments
                if(isinstance(its,it.salvationBuff)):
                    if(fl.cheatedDeath > 0):
                        print(fl.name+" cheated death with a Salvation Sphere "+str(fl.cheatedDeath)+" times.")
                    else:
                        # Unused Salvation Sphere, dead and alive.
                        if(fl.alive == False):
                            print(fl.name+" got a Salvation Sphere, but it expired before they died! How tragic!")
                        else:
                            print(fl.name+" got a Salvation Sphere, but they didn't need it! Awesome!")

            # Pacifist Win, Not On Team!
            if(fl.alive and ind_kills == 0 and ind_team == None):
                print(fl.name+" won the battle... without killing anybody! Whoa!")
            elif(fl.alive):
                print(fl.name+" won the battle, and is victorious!")
            else:
                print(fl.name+" didn't survive the battle.")
        print(self.sep)

        # Room Metrics
        '''
        r_
        '''

        # Hazard Metrics
        h_placedCount   = 0
        h_activateCount = 0
        h_damageCount   = 0
        h_killCount     = 0
        h_killList      = []
        for ro in roomList:
            h_placedCount += len(ro.allHazards)
            for haz in ro.allHazards:
                h_activateCount += sum(haz.damageTargets.values())
                h_damageCount += sum(haz.damageDone.values())
                h_killCount += len(haz.kills)
                h_killList.extend(haz.kills)

        print("OVERALL DATA FROM HAZARDS")            
        print("  HAZARDS PLACED:     "+str(h_placedCount))
        print("  HAZARD ACTIVATIONS: "+str(h_activateCount))
        print("  ACTIVATION RATIO:   "+str(float(h_activateCount/h_placedCount)))
        print("  HAZARD DAMAGE:      "+str(h_damageCount))
        if h_killCount > 0:
            print("  HAZARD KILLS:       "+str(h_killCount))
            print("WAIT, WHO DIED TO A HAZARD, EXACTLY...?")
            print("  "+str(h_killList))
            print("DEARY ME!")
        print(self.sep)
        
