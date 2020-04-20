import cl_Game
from random import randint
from random import choice
from random import shuffle

# import CSV and folder stuff
import csv

# Mob Class
class Mob(object):
    def __init__(self,
                 newID=-1,
                 mobName="Unnamed Thing",
                 mobType="Untyped Mob",
                 mobDesc="Undescribed Mob",
                 mobHP=50):
        self.id                = newID
        self.alive             = True
        self.deaths            = 0
        self.name              = mobName
        self.sname             = ""
        self.type              = mobType
        self.desc              = mobDesc
        self.team              = None
        self.score             = 0
        self.stats             = {"ATK":3, "DEF":3, "AGI":3, "SPD":3, "MAG":3, "MDF":3}
        self.image             = None

        #Statistics
        self.maxHitpoints      = mobHP
        self.hitpoints         = self.maxHitpoints
        self.hpPerRound        = []
        self.buffTimer         = 0
        self.buffType          = None
        self.itemsGot          = []
        self.cheatedDeath      = 0
        self.hazardsTripped    = 0
        self.hazardsAvoided    = 0
        self.healingGot        = 0

        #Attacks
        self.attacks           = []
        self.currentTarget     = None
        self.lastAttacked      = None
        self.lastHitBy         = None
        self.lastHitWith       = None
        self.lastMissedBy      = None

        #Movement and Travel
        self.location          = None
        self.travel            = []
        self.travelFight       = []
        self.travelAttacked    = []
        self.travelSteps       = 0

        # Chatter
        self.readyStrings      = [] # Triggered upon game start.
        self.winStrings        = [] # Triggered upon victory.
        self.loseStrings       = [] # Triggered upon death.
        self.attackStrings     = [] # Triggered upon attack.
        self.hurtStrings       = [] # Triggered upon taking damage.
        self.insultStrings     = [] # Triggered upon seeing a horrendous miss against them or an ally misses (by -6, by -12 if an ally misses).
        self.complimentStrings = [] # Triggered upon seeing a solid hit by an ally or against themselves (by +6, by +12 for an enemy hitting them).
        self.moveStrings       = [] # Triggered upon movement.
        self.healStrings       = [] # Triggered upon health recovery.
        self.hazardStrings     = [] # Triggered upon tripping a hazard.
        self.waitStrings       = [] # Triggered upon wait.
        self.threeKillStrings  = [] # Triggered after getting 3 kills.
        self.fiveKillStrings   = [] # Triggered after getting 5 kills.
        
        # Intelligence/Decision Making
        self.ai_memory         = 3  # How many turns of Memories the Mob retains with which to make decisions.
        # Generally, all AI parameters default to being 3/6 (1/2).
        # A score in an AI stat of 1 is highly unlikely, while a 5 is highly likely. (no 0 or 6)
        self.ai_brave          = 3  # How likely they are to be brave (attack when injured, and pursue fights).
        self.ai_coward         = 3  # How likely they are to be cowardly (run away when injured, and avoid fights).
        self.ai_wait           = 3  # How likely they are to wait in place.
        self.ai_help           = 3  # How likely they are to move toward a teammate, when teams are turned on.
        self.ai_talk           = 3  # How likely they are to talk/comment on what happens around them.

    # Get Name
    def __repr__(self):
        if(self.alive):
            if(self.team != None):
                return self.name+" ["+str(self.team.name)+"]"
            else:
                return self.name
        else:
            if(self.team != None):
                return self.name+" ["+str(self.team.name)+"] (DEAD)"
            else:
                return self.name+" (DEAD)"
    
    # Rename
    def rename(self,newName):
        prevName = self.name
        self.name = newName
        print(prevName+" is now called "+self.name+".")
        return self.name

    # Change mob type
    def retype(self,newType):
        prevType = self.type
        self.type = newType
        print(self.name+" was a "+prevType+", and is now a "+self.type)
    
    def updateImage(self,prefix="/fighters/img/"):
        self.image = prefix+self.sname.lower()+".png"

    # Change team
    def changeTeam(self,newTeam):
        if(newTeam == None):
            self.team = newTeam
            print(self.name+" is no longer on a team.")
        elif(isinstance(newTeam,Team)):
            self.team = newTeam
            print(self.name+" is on the "+newTeam.name+" team.")
    
    # Remove self from team.
    def leaveTeam(self):
        self.team = None
    
    def locateTeammates(self):
        if(self.team == None):
            pass
        else:
            teammateLocs = {}
            teammates = []
            locations = []
            for mob in self.team.members:
                teammates.append(mob)
                locations.append(mob.location)
            teammateLocs.fromkeys(teammates,locations)
            #print(teammateLocs)
            return teammateLocs

    # Update/Check Hitpoints
    def updateHitpoints(self):
        # Cannot be alive if hitpoints less than 0
        if(self.alive == True):
            if(self.hitpoints <= 0):
                self.alive = False
                print(self.name+" is now dead. "+str(self.hitpoints)+"/"+str(self.maxHitpoints)+" hitpoints.")
            else:
                print(self.name+" has "+str(self.hitpoints)+"/"+str(self.maxHitpoints)+" hitpoints.")
        else:
            print(self.name+" is dead. "+str(self.hitpoints)+"/"+str(self.maxHitpoints)+" hitpoints.")
        return self.hitpoints

    # Add Attack by creating it dynamically.
    def addAttack(self,aid=-1,params=["Blank Attack","ATK","DEF",0,6,3,0],killString="was killed by",report=False):
        # [name,satk,sdef,dds,ddn,ddm]
        newAttack = Attack()
        newAttack.id = aid
        newAttack.name = params[0]
        newAttack.statAttack = params[1]
        newAttack.statDefend = params[2]
        newAttack.toHit = params[3]
        newAttack.damDiceSides = params[4]
        newAttack.damDiceNumber = params[5]
        newAttack.damDiceMod = params[6]
        newAttack.killString = killString

        self.attacks.append(newAttack)
        if(report):
            print(self.name+" is now armed with "+newAttack.name+" (+"+str(newAttack.toHit)+
                  " To Hit, "+str(newAttack.damDiceNumber)+"d"+str(newAttack.damDiceSides)+
                  "+"+str(newAttack.damDiceMod)+" Damage)")
    
    # Add Attack Object as a whole.
    def addAttackObject(self,newAttack,report=False):
        self.attacks.append(newAttack)
        
        if(report):
            print(self.name+" is now armed with "+newAttack.name+" (+"+str(newAttack.toHit)+
                  " To Hit, "+str(newAttack.damDiceNumber)+"d"+str(newAttack.damDiceSides)+
                  "+"+str(newAttack.damDiceMod)+" Damage)")

    # Remove Attack
    def removeAttack(self,attack):
        if(attack in self.attacks):
            # attack found in list
            pass
        else:
            # specified attack isn't in attack list
            pass

    # Count Down Buff Timer
    def countDownBuff(self):
        if(self.buffTimer > 0):
            self.buffTimer -= 1
        else:
            self.buffType = None

    # Gameplay Loop
    def playGame(self):
        if(self.alive):
            from cl_Room import Room
            from cl_Room import roomList
            
            if(isinstance(self.location,Room)):
                # Initialise the 'brain' of the mob.
                attacks = randint(0,len(self.attacks)-1)
                targets = self.location.mobs.copy()
                targets.append(self.lastMissedBy)
                targets.append(self.lastHitBy)
                targets.append(self.lastAttacked)
                targets.append(self.currentTarget)
                targets.reverse()
                targetChoices = []
                allies = self.locateTeammates()

                # Pick up something in the room at the start of turn.
                self.getPickup()

                #With list of targets, remove self, and remove None-s.
                for t in targets:
                    if(self.lookForMob(t)):
                        targetChoices.append(t)
                    if(self in targetChoices):
                        targetChoices.remove(self)
                    if(None in targetChoices):
                        targetChoices.remove(None)
                        continue

                    # Figure out what's a mob, and if they're a target.
                    # Then remove teammates, the dead, and the invisible.
                    # from the targets list.
                    if(isinstance(t,Mob) and t in targetChoices):
                        if(self.team == t.team and t.team != None):
                            targetChoices.remove(t)
                            continue
                        if(t.alive == False):
                            targetChoices.remove(t)
                            continue
                        if(t.buffType == "Invisible"):
                            targetChoices.remove(t)
                            continue

                # If target list is at least 1 or more, fight.
                # If attack fails or no choices, go to another room.
                if(len(targetChoices)):
                    # Targets available. Choose to fight or move.
                    if(self.buffType != None or self.hitpoints > int(self.maxHitpoints/2)):
                        # Don't run while got powerup or healthy
                        do = "fight"
                    else:
                        # 1 in 3 chance of moving normally
                        do = choice(["fight","fight","move"])

                    # Act on choice.
                    if(do == "fight"):
                        if(self.think(self.ai_talk) == True):
                            self.sayDoSomething(choice(self.attackStrings))
                        self.attackMob(attacks,choice(targetChoices))
                    else:
                        if(self.think(self.ai_talk) == True):
                            self.sayDoSomething(choice(self.moveStrings))
                        self.goToAnotherRoom()
                else:
                    # No targets in sight. Move or wait.
                    if(self.buffType != None or len(self.location.hazards)):
                        # Don't idle while mob has a powerup, or location has a hazard in it
                        do = "move"
                    else:
                        do = choice(["move","move","move","wait"])
                    
                    if(do == "move"):
                        # Prioritise going to rooms with pickups or other Mobs
                        # with a chance of just going somewhere random because
                        roomChoices = [-1]
                        for ex in self.location.exits:
                            if(len(roomList[ex].items)):
                                roomChoices.append(ex)
                        # Add rooms with mobs in them
                        for ex in self.location.exits:
                            if(len(roomList[ex].mobs)):
                                for m in roomList[ex].mobs:
                                    if(m.alive and m.buffType != "Invisible"):
                                        roomChoices.append(ex)
                        # Remove hazardous rooms from set choices
                        for ex in self.location.exits:
                            if(len(roomList[ex].hazards) and ex in roomChoices):
                                roomChoices.remove(ex)

                        #print(roomChoices)
                        if(len(roomChoices)):
                            # Go to specific Room
                            goto = choice(roomChoices)
                        else:
                            # Go to random room
                            goto = -1
                        if(self.think(self.ai_talk) == True):
                            self.sayDoSomething(choice(self.moveStrings))
                        self.goToAnotherRoom(goto)
                    elif(do == "wait"):
                        self.travel.append(self.location.id)
                        print(self.name+" waits at "+self.location.name+"...")
                        if(self.think(self.ai_talk) == True):
                            self.sayDoSomething(choice(self.waitStrings))

                # Try picking up something in the room at end step.
                self.getPickup()

                # Do regeneration
                if(self.buffTimer > 0 and self.buffType == "Regen"):
                    if(self.hitpoints < self.maxHitpoints):
                        regen = cl_Game.rollDice(6,1,0)
                        self.hitpoints += regen
                        if(self.hitpoints > self.maxHitpoints):
                            self.hitpoints = self.maxHitpoints
                        print(self.name+" regenerates "+str(regen)+" HP!")
                        self.healingGot += regen
                        self.updateHitpoints()
                # Do hazard check
                if(len(self.location.hazards)):
                    for h in self.location.hazards:
                        if(h.tripCheck() and self.alive):
                            print(self.name+" triggered the "+h.name+"!")
                            if(self.buffType != "Warning"):
                                if(self.think(self.ai_talk) == True):
                                    self.sayDoSomething(choice(self.hazardStrings))
                                h.hazardActivate(self)
                                self.hazardsTripped += 1
                            else:
                                print(self.name+" was warned of "+h.name+" and took no damage!")
                                if(self.think(self.ai_talk) == True):
                                    self.sayDoSomething(choice(self.insultStrings))
                        elif(self.alive):
                            self.hazardsAvoided += 1
                # Update HP Per Turn
                self.hpPerRound.append(self.hitpoints)
            else:
                print(self.name+" has not been placed in a room. They can't play the game!")
                self.placeInRoom(0)
        else:
            # Character is dead. Cannot take actions.
            pass

    # Report Status
    def reportStatus(self,loc=True):
        if(self.alive == True):
            # Return current HP
            # Report Team Name if available.
            if(self.team == None):
                print(self.name+" Health: "+str(self.hitpoints)+"/"+str(self.maxHitpoints))
            else: 
                print(self.name+" Health: "+str(self.hitpoints)+"/"+str(self.maxHitpoints)+" ["+str(self.team.name)+"]")
            
            # Report Buffs if active.
            if(self.buffTimer > 0 and self.buffType != None):
                print("Buff: "+str(self.buffType)+" | Duration: "+str(self.buffTimer)+" Rounds")
        else:
            print(self.name+" Health: DEAD")
        if(loc):
            # Return Location.
            print(self.name+" Location: "+str(self.location.name))
    
    # Attack other Mob
    def attackMob(self,attack,target=None):
        # Returns true or false if the attack succeeds or fails
        # in being carried out, regardless of hitting or missing.
        
        # Check if attack used is an attack.
        if(isinstance(self.attacks[attack],Attack)):
            atk = self.attacks[attack]
            #Attack is correct. Is target correct?
            if(isinstance(target,Mob)):
                if (self.lookForMob(target) == True):
                    # Target is a mob, define adding function for statistics...
                    def addToTargets(t=atk.targets,c=1):
                        if(str(target.name) in t):
                            t[str(target.name)] += c
                        else:
                            t[str(target.name)] = c
                    
                    # Check if target is alive.
                    if(target.alive == True):
                        # Target is alive, therefore can be attacked. Sweet!
                        # Roll the dices! If attacker is equal/higher to defender, its a hit.
                        attackRoll = cl_Game.rollDice(20,1,self.stats[atk.statAttack]+atk.toHit)
                        defendRoll = cl_Game.rollDice(20,1,target.stats[atk.statDefend])
                        
                        def attackDefendDifference():
                            return attackRoll - defendRoll
                        chatThreshold = 6 # How much of a difference needs to occur between attack and defence rolls make the character think about talking.

                        if(attackRoll >= defendRoll):
                            # Attack hits!
                            diceSides = atk.damDiceSides
                            diceNumber = atk.damDiceNumber
                            diceMod = atk.damDiceMod
                            
                            # Roll damage
                            damage = cl_Game.rollDice(diceSides,diceNumber,diceMod)
                            if(self.buffTimer > 0 and self.buffType == "Attack"):
                                damage = damage*2
                            if(target.buffTimer > 0 and target.buffType == "Defence"):
                                damage = int(damage/2)
                            target.hitpoints -= damage
                            print(self.name+"'s "+str(atk.name)+" hits "+str(target.name)+" for "+str(damage)+" points of damage! ("+str(attackRoll)+" vs "+str(defendRoll)+")")

                            # Report and Apply damage
                            if(target.think(target.ai_talk) == True):
                                target.sayDoSomething(choice(target.hurtStrings))
                            atk.hits += 1
                            target.updateHitpoints()
                            atk.damage += damage
                            addToTargets(atk.targetHits)
                            addToTargets(atk.targetDamage,damage)
                            target.lastHitBy = self
                            target.lastHitWith = atk
                            
                            '''
                            if(attackDefendDifference() >= 8):
                                if(target.think(target.ai_talk) == True):
                                        target.sayDoSomething(choice(target.complimentStrings))
                            '''
                            
                            # add to attack's Kill List if target killed.
                            if(target.hitpoints <= 0):
                                #Apply Salvation Sphere effects if buff active
                                if(target.buffTimer > 0 and target.buffType == "Salvation"):
                                    # Activate salvation sphere! Another soul saved!
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
                                    # Die normally
                                    atk.kills.append(target.name)
                                    target.hpPerRound.append(target.hitpoints)
                                    if(target.think(target.ai_talk) == True):
                                        target.sayDoSomething(choice(target.loseStrings))
                        else:
                            # Attack misses!
                            print(self.name+"'s "+atk.name+" misses "+target.name+"! ("+str(attackRoll)+" vs "+str(defendRoll)+")")
                            atk.misses += 1
                            addToTargets(atk.targetMisses)
                            target.lastMissedBy = self
                            
                            if(attackDefendDifference() <= -chatThreshold):
                                if(target.think(target.ai_talk) == True):
                                        target.sayDoSomething(choice(target.insultStrings))
                        # Regardless of hit/miss, do logging
                        addToTargets()
                        self.travel.append(self.location.id)
                        self.travelFight.append(self.location.id)
                        self.lastAttacked = target
                        self.currentTarget = target
                        target.travelAttacked.append(target.location.id)

                        self.location.addToAttacksBy(self)
                        target.location.addToAttacksOn(target)
                        return True
                    else:
                        # Target isn't alive. Shouldn't/Can't attack...
                        print(self.name+"'s target "+target.name+" is already dead!")
                        return False
                else:
                    # Target not in same room as Mob.
                    print(self.name+" can't find "+target.name+"!")
                    return False
            elif(target == None):
                # No target set.
                print(self.name+" has no target set.")
                return False
            else:
                #Target doesn't exist/isn't a mob.
                print(self.name+"'s specified target "+target.name+" is not a Mob!")
                return False
        else:
            #Attack is not correct. Abort!
            print(self.name+"'s specified attack is not an Attack!")
            return False

    # Place Mob in Room
    def placeInRoom(self,newRoom,record=True):
        from cl_Room import Room
        if(isinstance(newRoom,Room)):
            # Remove mob from current room
            if(self.location != None):
                prevRoom = self.location
                self.location = None
                if(self in prevRoom.mobs):
                    prevRoom.mobs.remove(self)
                    print(self.name+" has been removed from "+prevRoom.name)
                    print(prevRoom.name+" now contains "+str(prevRoom.mobs))
                else:
                    print("That's weird, "+self.name+" isn't in "+prevRoom.name+" but is. Eh, moving on...")
                    print(self.name+" has been removed from "+prevRoom.name)
            # Place mob
            self.location = newRoom
            if(record):
                self.travel.append(self.location.id)
                self.travelSteps += 1
            newRoom.mobs.append(self)
            print(self.name+" has been placed in "+self.location.name)
            print(newRoom.name+" now contains "+str(newRoom.mobs));
        else:
            print("Specified Room is not a Room object.")

    # Move to another room via an exit
    def goToAnotherRoom(self, specific = -1):
        from cl_Room import Room
        from cl_Room import roomList
        if(isinstance(self.location,Room)):
            exits = self.location.exits
            if(len(exits) > 0):
                # Pick an exit, go there.
                if(specific == -1 or specific not in exits):
                    goto = choice(exits)
                else:
                    goto = specific
                
                nextRoom = roomList[goto]
                prevRoom = self.location
                
                prevRoom.mobs.remove(self)
                nextRoom.mobs.append(self)
                self.location = nextRoom
                self.travel.append(self.location.id)
                self.travelSteps += 1
                
                prevRoom.addToTravelledTo(nextRoom.id)
                nextRoom.addToTravelledFrom(prevRoom.id)
                
                print(self.name+" has moved from "+prevRoom.name+" to "+self.location.name)
                print(prevRoom.name+" now contains "+str(prevRoom.mobs))
                print(self.location.name+" now contains "+str(self.location.mobs))
            else:
                print(self.location.name+" has no exits.")
        else:
            print(self.name+" has not been placed in a room.")

    # See if another Mob is in the same room.
    def lookForMob(self,target = None):
        if(isinstance(target,Mob)):
            # target is a mob
            if(target.location == self.location):
                # target is in same room
                return True
            else:
                # target not in same room
                return False
        else:
            #target not a mob
            return False

    # Report detailed attack statistics
    def reportAttackStats(self):
        th = 0
        tm = 0
        td = 0
        tk = []
        # Report character overall
        for i in self.attacks:
            td += i.damage
            th += i.hits
            tm += i.misses
            tk.extend(i.kills)
        print(self.name+"'s Overall Combat Statistics:")
        print("  HITS: "+str(th)+" | MISSES: "+str(tm)+" | DAMAGE DONE: "+str(td))
        if(len(tk)):
            print("  KILLS: "+str(tk))
        
        # Report individually
        for i in self.attacks:
            print(self.name+"'s attack \'"+i.name+"\' statistics:")
            print("  HITS: "+str(i.hits)+" | MISSES: "+str(i.misses)+" | DAMAGE: "+str(i.damage))
            if(len(i.targets)):
                print("  TARGET DATA: "+str(i.targets))
            if(len(i.targetHits)):
                print("  TARGET HITS: "+str(i.targetHits))
            if(len(i.targetMisses)):
                print("  TARGET MISSES: "+str(i.targetMisses))
            if(len(i.targetDamage)):
                print("  TARGET DAMAGE: "+str(i.targetDamage))
            if(len(i.kills)):
                print("  KILLS: "+str(i.kills))
    
    def sayDoSomething(self,string=""):
        # Say something, or emote if ()'s are around the string, or yell if {}'s are around string.
        # TODO: Make it so Yells indicate a character's position/gives them away/invites fights?
        
        # Is there a string to process, if so, is it not blank?
        if(string != "" and isinstance(string,str)):
            # Are there brackets?
            if(string.startswith("(") == True and string.endswith(")") == True):
                # Emote!
                emote = string.strip("()")
                print(self.name+" "+emote)
            elif(string.startswith("{") == True and string.endswith("}")):
                # Yell!
                yell = string.strip("{}")
                print(self.name+" yells: \""+yell+"\"")
            elif(string.startswith("[") == True and string.endswith("]")):
                # Think!
                think = string.strip("[]")
                print(self.name+" thinks: \'"+think+"\'")
            else:
                # Speak Normally!
                print(self.name+" says: \""+string+"\"")
        else:
            # Blank string/not a string. Can't do anything with that.
            pass

    def think(self,thought):
        # Think about something. Rolls a d6, and checks
        # if its less/equal to the parameter given (1 to 5).
        # Returns True/False
        #dice = 3
        dice = cl_Game.rollDice(6,1,0)
        return dice <= thought

    def getPickup(self):
        if(len(self.location.items) > 0):
            items = self.location.items
            pick = choice(items)
            self.usePickup(pick)

    def usePickup(self,pickup):
        import cl_Items as it
        if(isinstance(pickup,it.Pickup)):
            taken = True
            
            if(isinstance(pickup,it.healthPickup)):
                # Health Pickup!
                if(self.hitpoints < self.maxHitpoints):
                    self.hitpoints += pickup.power
                    if(self.hitpoints > self.maxHitpoints):
                        self.hitpoints = self.maxHitpoints
                    print(self.name+" got a "+pickup.name+"! Recovered "+str(pickup.power)+" HP!")
                    self.healingGot += pickup.power
                    self.updateHitpoints()
                    if(self.think(self.ai_talk) == True):
                        self.sayDoSomething(choice(self.healStrings))
                else:
                    # Health already full. Don't pick up.
                    print(self.name+" walked over a Health Pickup.")
                    taken = False
            elif(isinstance(pickup,it.defenceBuff)):
                # Defence Sphere!
                self.buffTimer = pickup.timer
                self.buffType = "Defence"
                print(self.name+" got a Defence Sphere! (halves incoming damage)")
            elif(isinstance(pickup,it.attackBuff)):
                # Attack Sphere!
                self.buffTimer = pickup.timer
                self.buffType = "Attack"
                print(self.name+" got an Attack Sphere! (doubles outgoing damage)")
            elif(isinstance(pickup,it.speedBuff)):
                # Speed Sphere!
                self.buffTimer = pickup.timer
                self.buffType= "Speed"
                print(self.name+" got a Speed Sphere! (Extra Action per turn)")
            elif(isinstance(pickup,it.regenBuff)):
                # Regen Sphere!
                self.buffTimer = pickup.timer
                self.buffType= "Regen"
                print(self.name+" got a Regen Sphere! (Slowly regains health)")
            elif(isinstance(pickup,it.teleportPickup)):
                # Teleport Sphere!
                print(self.name+" got a Teleport Sphere! (Teleports to random location)")
                from cl_Room import roomList
                from random import randint
                roomToPick = randint(0,len(roomList)-1)
                newRoom = roomList[roomToPick]
                self.placeInRoom(newRoom)
            elif(isinstance(pickup,it.salvationBuff)):
                # Salvation Sphere!
                self.buffTimer = pickup.timer
                self.buffType= "Salvation"
                print(self.name+" got a Salvation Sphere! (Self-resurrect once while active)")
            elif(isinstance(pickup,it.invisibleBuff)):
                # Invisibility Sphere!
                self.buffTimer = pickup.timer
                self.buffType = "Invisible"
                print(self.name+" got an Invisibility Sphere! (Cannot be targetted by other mobs)")
            elif(isinstance(pickup,it.warningBuff)):
                # Warning Sphere!
                self.buffTimer = pickup.timer
                self.buffType = "Warning"
                print(self.name+" got a Warning Sphere! (Cannot activate hazards)")
                
            # If pickup not taken for some reason (Health full, etc) then don't remove
            if(taken):
                self.itemsGot.append(pickup)
                pickup.takenBy = self
                pickup.remove()
        else:
            pass
    
    def specifyChatStrings(self,chatLists):
        self.winStrings        = chatLists[0].split("|")
        self.readyStrings      = chatLists[1].split("|")
        self.loseStrings       = chatLists[2].split("|")
        self.attackStrings     = chatLists[3].split("|")
        self.hurtStrings       = chatLists[4].split("|")
        self.insultStrings     = chatLists[5].split("|")
        self.complimentStrings = chatLists[6].split("|")
        self.moveStrings       = chatLists[7].split("|")
        self.healStrings       = chatLists[8].split("|")
        self.hazardStrings     = chatLists[9].split("|")
        self.waitStrings       = chatLists[10].split("|")
    
    @classmethod
    def createMobs(self,mob_file="\\fighters\\fighters.csv"):
        mobList = []
        
        # Import via CSV
        with open(mob_file,newline="") as ff:
            mobRead = csv.DictReader(ff)
        
            for r in mobRead:
                ini = (int(r["id"]),
                       str(r["name"]),
                       str(r["type"]),
                       str(r["desc"]),
                       int(r["hp"])
                      )
                stat = {"ATK":int(r["atk"]),"DEF":int(r["def"]),
                        "AGI":int(r["agi"]),"SPD":int(r["spd"]),
                        "MAG":int(r["mag"]),"MDF":int(r["mdf"])
                        }
                # Init Mob Vitals and Stats
                newMob = Mob(ini[0],ini[1],ini[2],ini[3],ini[4])
                newMob.stats = stat
                
                # Short Name
                newMob.sname = str(r["sname"])
                
                # Get Chat Strings
                chat_win    = str(r["winstrings"])
                chat_ready  = str(r["readystrings"])
                chat_lose   = str(r["losestrings"])
                chat_attack = str(r["attackstrings"])
                chat_hurt   = str(r["hurtstrings"])
                chat_insult = str(r["insultstrings"])
                chat_comp   = str(r["complimentstrings"])
                chat_move   = str(r["movestrings"])
                chat_heal   = str(r["healstrings"])
                chat_hazard = str(r["hazardstrings"])
                chat_wait   = str(r["waitstrings"])
                
                chatList = [chat_win,chat_ready,chat_lose,chat_attack,chat_hurt,chat_insult,
                            chat_comp,chat_move,chat_heal,chat_hazard,chat_wait]
                
                newMob.specifyChatStrings(chatList)
                
                ai_talk     = int(r["ai_talk"])
                
                newMob.ai_talk = ai_talk
                newMob.updateImage("./fighters/img/")
                
                mobList.append(newMob)
        
        ff.close()
        return mobList

# Attacks Class
class Attack(object):
    def __init__(self):
        self.id = -1
        self.name = "Blank Attack"
        self.statAttack = "ATK"
        self.statDefend = "DEF"
        self.toHit = 0
        self.damDiceSides = 6
        self.damDiceNumber = 2
        self.damDiceMod = 0
        self.killString = ""

        #Statistics/Logging
        self.hits = 0
        self.misses = 0
        self.damage = 0
        self.targets = dict()
        self.targetHits = dict()
        self.targetMisses = dict()
        self.targetDamage = dict()
        self.kills = []
    
    def __repr__(self):
        return self.name
    
    def setID(self,newID):
        if(isinstance(newID,int)):
            self.id = newID
    
    def rename(self,newName):
        if(isinstance(newName,str)):
            self.name = newName
    
    def setAttackDefend(self,newATK="ATK",newDEF="DEF"):
        self.statAttack = newATK.upper()
        self.statDefend = newDEF.upper()
        
    def setDiceProperties(self,toHit=0,sides=8,num=3,mod=0):
        self.toHit         = toHit
        self.damDiceSides  = sides
        self.damDiceNumber = num
        self.damDiceMod    = mod
    
    def setKillString(self,kString="was ouched by"):
        self.killString    = kString
        pass
        
    @classmethod
    def createAndAssignAttacks(self,attack_file=""):
        # Returns a list of attacks, and assigns them to characters
        result = []
        with open(attack_file, "r") as af:
            attackRead = csv.DictReader(af)
        
            for r in attackRead:
                attackID    = int(r["id"])
                fighterID   = int(r["fid"])
                name        = str(r["name"])
                aStat       = str(r["atkstat"]).upper()
                dStat       = str(r["defstat"]).upper()
                toHit       = int(r["tohit"])
                diceSides   = int(r["dice_sides"])
                diceNum     = int(r["dice_num"])
                diceMod     = int(r["dice_mod"])
                kString     = str(r["killstring"])
                
                newAttack       = Attack()
                newAttack.setID(attackID)
                newAttack.rename(name)
                newAttack.setAttackDefend(aStat,dStat)
                newAttack.setDiceProperties(toHit,diceSides,diceNum,diceMod)
                newAttack.setKillString(kString)
                
                mobList[fighterID].addAttackObject(newAttack)
            
                result.append(newAttack)
        
        return result

# Team Class
class Team(object):
    def __init__(self,tName="Unnamed"):
        self.name = tName
        self.score = 0
        self.members = []
        self.status = False

    def __repr__(self):
        return "Team "+self.name+" ("+str(self.countMembers())+")"

    def updateName(self,newName):
        oldName = self.name
        self.name = newName
        print("Team '"+oldName+"' is now called '"+self.name+"'.")

    def updateScore(self):
        # Gather scores from all members of the team.
        if(len(self.members) > 0):
            self.score = 0
            for m in self.members:
                self.score += m.score
            print("Team Score for "+self.name+": "+str(self.score))
        else:
            print(self.name+" contains no members.")

    def updateStatus(self,p=False):
        if(len(self.members) > 0):
            # Check team status.
            # Count total members, see who's alive.
            total_members = len(self.members)
            live_members  = 0
            dead_members  = 0
            
            for m in self.members:
                if(m.alive == True):
                    live_members += 1 
                else:
                    dead_members  += 1

            if(dead_members == total_members):
                # Everybody's dead, dave!
                self.status = False
                if(p):
                    print("All members of this team are dead.")
                return False
            elif(live_members == total_members):
                # All members are alive.
                self.status = True
                if(p):
                    print("All members of this team are alive.")
                return True
            else:
                # At least one person is still alive.
                self.status = True
                if(p):
                    print(str(live_members)+" out of "
                          +str(total_members)+" remain in this Team.")
                return True
        else:
            self.status = False
            if(p):
                print(self.name+" contains no members.")
            return False

    def addMember(self,newMember):
        if(isinstance(newMember,Mob)):
            if(newMember not in self.members):
                self.members.append(newMember)
                newMember.team = self
                print(newMember.name+" was added to team "+self.name+".")
            else:
                print(newMember.name+" is already a part of "+self.name+".")
        else:
            print("Specified object is not a Mob.")

    def remMember(self,oldMember):
        if(isinstance(oldMember,Mob)):
            if(oldMember in self.members):
                self.members.remove(oldMember)
                oldMember.team = None
                print(oldMember.name+" is no longer part of "+self.team++" Team.")
            else:
                print(oldMember.name+" isn't a part of "+self.name+" Team.")
        else:
            print("Specified object is not a Mob.")

    def countMembers(self,liveOnly=True):
        members_dead  = 0
        members_alive = 0
        for m in self.members:
            if(m.alive == False):
                members_dead  += 1
            else:
                members_alive += 1

        if(liveOnly == True):
            return members_alive
        else:
            return members_alive+members_dead
    
    @classmethod
    def createTeams(self,teams_file="./fighters/teams.csv"):
        result = []
        with open(teams_file, "r") as tf:
            teamRead = csv.DictReader(tf)
            for r in teamRead:
                tn = str(r["name"])
                newTeam = Team(tn)
                result.append(newTeam)
        return result

# Memory Class (tbd)
class MobMemory():
    def __init__(self):
        pass

# Player Class (tbd)
class Player(Mob):
    def __init__(self):
        Mob.__init__(self)
        pass

    def controls(self):
        pass

# Lists
fighterFile = "./fighters/fighters.csv"
attackFile  = "./fighters/attacks.csv"
teamsFile   = "./fighters/teams.csv"

#input("*** Introducing the fighters! (Hit [ENTER]) ***")

# Use Class Methods to generate characters, attacks and teams
mobList = Mob.createMobs(fighterFile)
attackList = Attack.createAndAssignAttacks(attackFile)
teamList = Team.createTeams(teamsFile)

def chooseFighters(ml=mobList):
    # Number of Fighters
    fightersChosen = False
    minimum = 4
    maximum = len(ml)
    question = "How many fighters would you like to join the battle? ("+str(minimum)+" to "+str(maximum)+")\n[Hit ENTER immediately to go for maximum!]\n>"
    
    while(fightersChosen == False):
        pick = -1
        pick = input(question)
    
        if(pick == ""):
            # Go for max number.
            pick = maximum
        else:
            try:
                pick = int(pick)
            except ValueError:
                # Not a number.
                print("That's not a number.")
                continue
        
        if(pick < minimum):
            # Below minimum.
            print("That's below the minimum.")
            continue
        if(pick > maximum):
            # Above maximum.
            print("That's above the maximum.")
            continue
    
        input("You have selected "+str(pick)+" fighters. (Hit [ENTER])")
        shuffle(ml)
        # Shuffle list, then cut list down to number of choices.
        ml = ml[:pick]
        # Then sort list back into ID order.
        ml.sort(key=lambda Mob: Mob.id)
        print(ml)
        fightersChosen = True
        for m in ml:
            if(m.think(m.ai_talk) == True):
                m.sayDoSomething(choice(m.readyStrings))
        input("The fighters are assembled! (Hit [ENTER])")
