    # Update Body Status
    def updateBody(self):
        print(self.name+" has torso? "+str(self.body["torso"]))
        print(self.name+" has groin? "+str(self.body["groin"]))
        print(self.name+"'s head count: "+str(self.body["heads"]))

        if(self.alive == True):
            # Cannot be alive without torso, groin, or no heads.
            if(self.body["torso"] == False):
                self.alive = False
                print(self.name+" is now dead - Torso is missing.")
            elif(self.body["groin"] == False):
                self.alive = False
                print(self.name+" is now dead - Groin is missing.")
            elif(self.body["heads"] <= 0):
                self.alive = False
                print(self.name+" is now dead - No heads left.")
            else:
                print(self.name+" is alive. All necessary parts are intact.")
        else:
            print(self.name+" is dead.")

    # Remove Body Parts
    def getDecapitated(self):
        if(self.body["heads"] > 0):
            self.body["heads"] = self.body["heads"] - 1
            print(self.name+" was decapitated! They have "+str(self.body["heads"])+" heads remaining.")
            self.updateBody()
        else:
            print(self.name+" has no more heads to cut off!")
            if(self.alive == False):
                print("...and they're already dead anyway!")

    def getDetorsoed(self):
        if(self.body["torso"] == True):
            self.body["torso"] = False
            print(self.name+" was de-torso'd!")
            self.updateBody()
        else:
            print(self.name+" doesn't have a torso to remove!")

    def getDegroined(self):
        if(self.body["groin"] == True):
            self.body["groin"] = False
            print(self.name+" was de-groin'd!")
            self.updateBody()
        else:
            print(self.name+" doesn't have a groin to remove!")

    def regenerateBodyparts(self):
        if(self.body["heads"] <= 0):
            self.body["heads"] = 1
        self.body["torso"] = True
        self.body["groin"] = True
        print(self.name+" has regenerated all vital parts!")
        self.updateBody()

    def growAnotherHead(self):
        if(self.alive == True):
            self.body["heads"] = self.body["heads"]+1
            print(self.name+" grew another head! They have "+str(self.body["heads"])+" now.")
            self.updateBody()
        else:
            print(self.name+" cannot grow another head. They are dead.")

    def resurrect(self):
        if(self.alive == False):
            self.regenerateBodyparts()
            self.hitpoints = 100
            self.alive = True
            print(self.name+" has risen from the dead!")
        else:
            print(self.name+" is already alive.")