# Create the Game Control Class
from cl_Game import GameSystem as gameSys
import cl_Room, cl_Mob, cl_Postgame

useGUI = False

if(useGUI == True):
    import cl_GUI
else:
    cl_Room.mapSelection()
    cl_Mob.chooseFighters()
    
    input("Press [ENTER] to continue...")
    gs = gameSys()
    
    # Select Game Mode  
    print(gs.sep)
    gs.selectGameMode()
    
    # Assign teams, if its a team game.
    print(gs.sep)
    gs.pregameTeamAssignment()
    
    # Scramble each fighter's location.
    print(gs.sep)
    gs.scrambleFighterLocations()
    
    # And away. We. Go.
    print(gs.sep)
    input("Fighters have been placed! Press [ENTER] to start the fight!")
    
    # Commence the gibblin until one of them dies.
    if(gs.gameMode in ["LTS","DUOS","TRIS","QUADS"]):
        input("*** Commence fight! Fight ends when one team remains! ****")
    else:
        input("*** Commence fight! Fight ends when one fighter remains! ***")
    
    # Start the main game loop
    while(gs.gameOn):
        print("*** New turn starting! ***")
        # Count down existing items/hazards, and add new ones as they appear
        gs.itemCountdown()
        gs.hazardCountdown()
        print(gs.smallSep)
    
        # Scramble fighter's Turn order
        gs.scrambleTurnOrder()
        
        # Do Fighter Turns
        gs.fighterTurns()
    
        # Increment overall turn.
        gs.incrementTurnCounter()
    
        # Check Match Status
        input("Press [ENTER] to see the match status.")
        gs.matchStatus()
        
        # Show current items on field.
        gs.showItems()
    
        # Show current Hazards on field.
        gs.showHazards()
    
        # Check for only one person left alive.
        print(gs.sep)
        gs.updateFighterStatus()
    
        # Press to proceed
        input("Press [ENTER] to start the next round!")
        print(gs.sep)
    
    input("*** We have a winner! *** (Hit [ENTER])")
    
    # Fighter metrics
    input("*** Let's go over some fighter metrics... *** (Hit [ENTER])")
    print(gs.sep)
    gs.fighterMetrics()
    
    # Room metrics
    input("*** Now let's go over some room metrics... *** (Hit [ENTER])")
    print(gs.sep)
    gs.roomMetrics()
    
    # Total metrics/achievements
    input("*** And finally, some overall metrics... *** (Hit [ENTER])")
    print(gs.sep)
    gs.totalMetrics()
    
    # Postgame File choice
    pg_choice = ""
    while(pg_choice == ""):
        pg_preinput = ""
        pg_upper = ""
    
        print("Would you like to generate some postgame files? (Y/N)")
        pg_preinput = input(">")
        pg_upper = pg_preinput.upper()
        
        if(pg_upper in ["Y","N"]):
            pg_choice = pg_upper
        else:
            print("Please enter Y or N.")
            
    if(pg_choice == "Y"):
        # Make a postgame file
        print("Postgame files will be written.")
        cl_Postgame.fighterMetricsToFile(gs)
        cl_Postgame.attackMetricsToFile(gs)
        cl_Postgame.roomMetricsToFile(gs)
        cl_Postgame.hazardMetricsToFile(gs)
        cl_Postgame.itemMetricsToFile(gs)
        cl_Postgame.gameMetricsToFile(gs)
        if(gs.gameMode != "LMS"):
            # Write team postgame only if its a team fight.
            cl_Postgame.teamMetricsToFile(gs)
    else:
        print("Postgame files will not be written.")
    
    print("THANKS FOR PLAYING/WATCHING - WRITTEN BY LUCA PAVONE 2019")
