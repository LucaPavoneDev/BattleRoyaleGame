# Import relevant lists of objects to be iterated through
from cl_Game import GameSystem
from cl_Mob import mobList
from cl_Mob import attackList
from cl_Room import roomList
from cl_Room import hazardList
from cl_Items import itemList

# Import Python Libraries
from datetime import datetime as dt
import csv
import os

# Get date/time and string it for filename ahead of functions
form = "%Y%m%d_%H%M"
now = dt.strftime(dt.now(),form)

# Postgame Wrapup Files
# Fighter Metrics
def fighterMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        try:
            # Create directory for logs to live in.
            os.mkdir("./postgameLogs/")
        except FileExistsError:
            # Directory already exists. We're fine.
            pass
    
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_fighters.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["id","name","type","location","locid","hps","alive",
                      "died","lasthitby","lasthitwith","hits","misses","kills",
                      "damage","healing","salvations","items","hazards",
                      "avoids","moves","travel","healthtrend"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)            
            writer.writeheader()
            for f in mobList:
                kills   = 0
                hits    = 0
                misses  = 0
                damage  = 0
                diedOn  = None
                if(f in game.deadList):
                    ind = game.deadList.index(f)
                    diedOn = str(game.diedOn[ind])
                heals   = f.healingGot
                salvs   = f.cheatedDeath
                hptrend = f.hpPerRound
                travel  = f.travel
                moves   = f.travelSteps
                hazs    = f.hazardsTripped
                avs     = f.hazardsAvoided
                loc     = f.location
                locid   = f.location.id
                hitBy   = f.lastHitBy
                hitWith = f.lastHitWith
                for at in f.attacks:
                    kills += len(at.kills)
                    hits += at.hits
                    misses += at.misses
                    damage += at.damage
                
                writer.writerow({"id":f.id,"name":f.name,"type":f.type,"location":loc,"locid":locid,
                                 "hps":f.hitpoints,"alive":f.alive,"died":diedOn,"lasthitby":hitBy,
                                 "lasthitwith":hitWith,"hits":hits,"misses":misses,"kills":kills,
                                 "damage":damage,"healing":heals,"salvations":salvs,
                                 "items":f.itemsGot,"moves":moves,"hazards":hazs,
                                 "avoids":avs,"travel":travel,"healthtrend":hptrend})
        print("Fighter Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")

# Attack Metrics
def attackMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_attacks.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["id","name","owner","hits","misses","ratio","damage","kills",
                      "statA","statD","targets","targetHits","targetMisses","targetDamage"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)
            writer.writeheader()
            for f in mobList:
                for a in f.attacks:
                    aid     = a.id
                    name    = a.name
                    owner   = f.name
                    hits    = a.hits
                    misses  = a.misses
                    # Prevent division by zero in this ratio getter.
                    if(hits > 0):
                        if(misses > 0):
                            ratio = float(hits/misses)
                        else:
                            ratio = hits
                    else:
                        ratio = 0
                    damage  = a.damage
                    kills   = a.kills
                    statA   = a.statAttack
                    statD   = a.statDefend
                    targets = a.targets
                    targetH = a.targetHits
                    targetM = a.targetMisses
                    targetD = a.targetDamage
                    writer.writerow({"id":aid,"name":name,"owner":owner,"hits":hits,"misses":misses,
                                     "ratio":ratio,"damage":damage,"kills":kills,"statA":statA,
                                     "statD":statD,"targets":targets,"targetHits":targetH,
                                     "targetMisses":targetM,"targetDamage":targetD})
            print("Attack Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")

# Room Metrics
def roomMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_rooms.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["id","name","exits","mobs","items","hazards",
                      "travelto","travelfrom","attacksby","attackson"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)            
            writer.writeheader()

            for ro in roomList:
                rid         = ro.id
                name        = ro.name
                exits       = ro.exits
                mobs        = ro.mobs
                items       = ro.pickupsDropped
                hazards     = ro.allHazards
                travelTo    = ro.travelledTo
                travelFrom  = ro.travelledFrom
                attacksBy   = ro.attacksBy
                attacksOn   = ro.attacksOn

                writer.writerow({"id":rid,"name":name,"exits":exits,"mobs":mobs,"items":items,
                                 "hazards":hazards,"travelto":travelTo,"travelfrom":travelFrom,
                                 "attacksby":attacksBy,"attackson":attacksOn})
            print("Rooms Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")

# Hazard Metrics
def hazardMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_hazards.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["name","location","locid","created_on","damage","targets","kills"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)            
            writer.writeheader()

            for ro in roomList:
                for h in ro.allHazards:
                    name    = h.name
                    loc     = h.location.name
                    locid   = h.location.id
                    damage  = h.damageDone
                    creat   = h.createdOn
                    targets = h.damageTargets
                    kills   = h.kills

                    writer.writerow({"name":name,"location":loc,"locid":locid,"created_on":creat,
                                     "damage":damage,"targets":targets,"kills":kills})
            print("Hazards Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")

# Item Metrics
def itemMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_items.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["name","location","lifetime","created_on","taken_by"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)            
            writer.writeheader()

            for ro in roomList:
                for i in ro.pickupsDropped:
                    name        = i.name
                    loc         = ro.name
                    life        = i.lifeTime
                    takenBy     = i.takenBy
                    createdOn   = i.createdOn

                    writer.writerow({"name":name,"location":loc,"created_on":createdOn,
                                     "lifetime":life,"taken_by":takenBy})
            print("Items Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")

# Game Metrics
def gameMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_game.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["turns_taken","total_moves","total_attacks","total_hits","total_misses",
                      "total_damage","damage_per_turn","damage_per_fighter","attacks_per_turn",
                      "attacks_per_fighter","total_heals","total_salvs","item_spawns",
                      "item_pickups","hazard_spawns","hazard_trips","hazard_avoids",
                      "hazard_damage","hazard_kills"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)            
            writer.writeheader()

            turnsTaken    = game.turnCounter
            fighterHits   = 0
            fighterMisses = 0
            fighterDamage = 0
            fighterMoves  = 0
            fighterHeals  = 0
            fighterSalvs  = 0
            fighterHazs   = 0
            fighterAvs    = 0
            for f in mobList:
                fighterHeals += f.healingGot
                fighterMoves += f.travelSteps
                fighterSalvs += f.cheatedDeath
                fighterHazs  += f.hazardsTripped
                fighterAvs   += f.hazardsAvoided
                for a in f.attacks:
                    fighterHits += a.hits
                    fighterMisses += a.misses
                    fighterDamage += a.damage
            fighterAttacks = fighterHits + fighterMisses
            damage_per_turn = float(fighterDamage/turnsTaken)
            damage_per_fighter = float(fighterDamage/len(mobList))
            attacks_per_turn = float(fighterAttacks/turnsTaken)
            attacks_per_fighter = float(fighterAttacks/len(mobList))

            itemTotal   = 0
            itemPickups = 0
            hazTotals   = 0
            hazTargets  = 0
            hazDamage   = 0
            hazKills    = 0
            for r in roomList:
                itemTotal += len(r.pickupsDropped)
                for i in r.pickupsDropped:
                    if i.takenBy != None:
                        itemPickups += 1
                hazTotals += len(r.allHazards)
                for h in r.allHazards:
                    hazTargets += sum(h.damageTargets.values())
                    hazDamage += sum(h.damageDone.values())
                    hazKills += len(h.kills)

            writer.writerow({"turns_taken":turnsTaken,"total_moves":fighterMoves,
                             "total_attacks":fighterAttacks,"total_hits":fighterHits,
                             "total_misses":fighterMisses, "total_damage":fighterDamage,
                             "damage_per_turn":damage_per_turn,
                             "damage_per_fighter":damage_per_fighter,
                             "attacks_per_turn":attacks_per_turn,
                             "attacks_per_fighter":attacks_per_fighter,
                             "total_heals":fighterHeals,"total_salvs":fighterSalvs,
                             "item_spawns":itemTotal,"item_pickups":itemPickups,
                             "hazard_spawns":hazTotals,"hazard_trips":fighterHazs,
                             "hazard_avoids":fighterAvs,"hazard_damage":hazDamage,
                             "hazard_kills":hazKills})
            print("Game System Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")

def teamMetricsToFile(game):
    if(isinstance(game,GameSystem)):
        postgameCSV = os.getcwd()+"\\postgameLogs\\postgame_"+now+"_teams.csv"
        with open(postgameCSV,"w+") as csvfile:
            fields = ["name","members","status"]
            writer = csv.DictWriter(csvfile,lineterminator="\n",fieldnames=fields)            
            writer.writeheader()
            
            for t in game.teamsList:
                writer.writerow({"name":t.name,
                                 "members":t.members,
                                 "status":t.status})
            print("Teams Summary Written to "+str(postgameCSV))
    else:
        print("Valid game system not specified. Aborting CSV write.")
