# Pickups/Powerups Classes
class Item(object):
    def __init__(self,name="Blank Item"):
        self.name = name
        self.location = None
        self.createdOn = -1
        self.takenBy = None
        itemList.append(self)

    def __repr__(self):
        return self.name

    def remove(self):
        self.location.items.remove(self)
        itemList.remove(self)

class Pickup(Item):
    def __init__(self,name="Blank Pickup"):
        Item.__init__(self,name)
        self.timer = 0
        self.lifeTime = 8

    def countDown(self):
        self.lifeTime += -1
        if(self.lifeTime <= 0):
            print(self.name+" at "+self.location.name+" has expired!")
            self.remove()

    def placeInRandomRoom(self):
        from cl_Room import Room
        from cl_Room import roomList
        from random import randint

        #spawn only in a room without living mobs
        roomsNoMobs = roomList.copy()
        for i in roomsNoMobs:
            if(len(i.mobs)):
                for m in i.mobs:
                    if(m.alive):
                        roomsNoMobs.remove(i)
                        break

        if(len(roomsNoMobs)):
            goto = randint(0,len(roomsNoMobs)-1)
            dropRoom = roomList[goto]
            dropRoom.items.append(self)
            dropRoom.pickupsDropped.append(self)
            self.location = dropRoom
            print("A "+self.name+" was dropped into "+dropRoom.name+"!")
        else:
            # No empty room to spawn item in. Drop!
            pass

class healthPickup(Pickup):
    def __init__(self,healPower=15):
        # Heals health.
        Pickup.__init__(self,"Health Pack")
        self.power = healPower

class defenceBuff(Pickup):
    def __init__(self,defTimer=8):
        # Halves all incoming damage, rounding down.
        Pickup.__init__(self,"Defence Sphere")
        self.timer = defTimer

class attackBuff(Pickup):
    def __init__(self,atkTimer=8):
        # Doubles outgoing damage, rounding up.
        Pickup.__init__(self,"Attack Sphere")
        self.timer = atkTimer

class regenBuff(Pickup):
    def __init__(self,rgnTimer=4):
        # Provides regeneration of health.
        Pickup.__init__(self,"Regen Sphere")
        self.timer = rgnTimer

class speedBuff(Pickup):
    def __init__(self,spdTimer=4):
        # User makes two actions a turn.
        Pickup.__init__(self,"Speed Sphere")
        self.timer = spdTimer

class salvationBuff(Pickup):
    def __init__(self,salvTimer=16):
        # User can spring back from fatal attack once.
        Pickup.__init__(self,"Salvation Sphere")
        self.timer = salvTimer

class teleportPickup(Pickup):
    def __init__(self):
        # Teleports to somewhere random on the battlefield.
        Pickup.__init__(self,"Teleport Sphere")

class invisibleBuff(Pickup):
    def __init__(self,invTimer=4):
        # Makes Mob unable to be targetted by other mobs.
        Pickup.__init__(self,"Invisibility Sphere")
        self.timer = invTimer

class warningBuff(Pickup):
    def __init__(self,warnTimer=8):
        # Makes mob unable to trip traps.
        Pickup.__init__(self,"Warning Sphere")
        self.timer = warnTimer

# New powerup thingy for when I feel like needing it...
'''
class ():
    def __init__(self,):
        pass
'''

# List
itemList = []
