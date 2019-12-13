import random
 
class caveLayout(object):
    
    ##use __init__ reserve method to initialize a data dictionary called cave
    ##assign each space on the game board to a key and its values to the spaces
    ##reachable from that space
    def __init__(self):
        
        cave = {1:[8],8:[1,9,15],9:[2,8,16],15:[8,16,22],16:[9,15,17,23],
                    17:[16,24],19:[20,26],20:[19],22:[15,23],23:[16,22,24,30],24:[17,23,25,31],
                    25:[24,26],26:[19,25,33],30:[23,31,37],31:[24,30,38],33:[26,34,40],
                    34:[33,41],36:[37,43],37:[30,36,38],38:[31,37,39,45],39:[38,40],
                    40:[33,39,41,47],41:[34,40,42,48],42:[41,49],43:[36],45:[38],47:[40,48],
                    48:[41,47,49],49:[48,42]}

        ##binds attributes with given arguments using self  class
        self.cave = cave
        self.hazard = {}
        self.arrows = 3
        self.monsterHorn = 0                                  
        self.player_pos = -1
        self.torchlight=100
 
 
    ## return a list of all spaces without hazards on them
    def safe_spaces(self):

        return list(set(self.cave.keys()).difference(self.hazard.keys()))
 
 
    ## create a list of hazards
    def setHazards(self):

        for hazard in ['monster','monster','monster','monster','pit','pit','pit','pit','Exit']:
            pos = random.choice(self.safe_spaces())
            self.hazard[pos] = hazard
        self.player_pos = random.choice(self.safe_spaces())
 
    ##present warnings to user
    def warning(self, hazard):

        if hazard == 'pit':
            print("You feel a breeze below.")
        elif hazard == 'monster':
            print("You feel somthing watching you from the dark")
        elif hazard == 'exit':
            print("You see a light in the distance, escape is near!")
 
    ##determne  what action was chosen by the player and run the prompt
    def playerAction(self):

        while 1:                                
            #get action from user
            action = input("Shoot, move, check bag, or quit?")
            try:                                
                answer = str(action).lower()
                assert answer in ['move','shoot', 'quit','check bag']
                break
            except (ValueError, AssertionError):
                print("You must pick a valid action (shoot,move,check bag,quit)")
       
        ##no need to ask where your going if your doing these actions
        if answer == 'quit':
            return ['quit']
        
        elif answer == 'check bag':
            return ['check bag']

        while 1:                                
 
            action = input("Where to?")
            
            ##give option to quit at any  time during move
            if action == 'quit':
                return ['quit']
            
            #set target to player choice, print error message if user picks a value
            #not in the key of the dictionary
            try:                                
                target = int(action)
            except ValueError:
                print("must select a room that exists")
                continue                        
 
            if answer == 'move':
                try:                            
                    assert target in self.cave[self.player_pos]
                    break
                except AssertionError:
                    print("You cannot move there")
 
            elif answer == 'shoot':
                return[answer,target]
 
        return[answer,target]
##simulate te action of entering a room with potential hazards
##if you dont die and a hazard is nearby give the user a warning if necessary
##if you die you loose all your horns
    def enter(self, room):
        ##print the room you just entered in the prompt
        print("You enter room {}".format(room))

        #you found the monster
        if self.hazard.get(room) == 'monster':
            print("You are eaten by a grue.")
            self.monsterHorn == 0
            return -1
        
        #you fall to your doom
        elif self.hazard.get(room) == 'pit':
            print("You fall into a pit.")
            self.monsterHorn == 0
            return -1
        #you escape the cave
        elif self.hazard.get(room) == 'exit':
            print("You climb out of the caves to your escape. Congratulations!")
            return -1
        
        #check for hazards
        for i in self.cave[room]:
            self.warning(self.hazard.get(i))
 

        return room
 
 ##simualte shooting an arrow if you hit a monster you get it back
 ##if you hit the exit you destroy your only escape route
    def shoot(self, room):
        if self.arrows >  0:
            
            print("You aim and shoot into the darkness of room {}".format(room))

            specialSquare = self.hazard.get(room)
    
            if specialSquare == 'monster':
                print("You have killed a grue, You loot its horn and continue")
                self.monsterHorn += 1
        
            elif specialSquare == 'exit':
                print("you sever the  escape rope with your arrow")
                print("Guess your not getting out of here...")
                return -1
            
            elif specialSquare in ['pit', None]:
                self.arrows -= 1
                print("You miss and the arrow is lost.")
                print("you have {} arrows left".format(self.arrows))
        else:
            print("your out of arrows")
 
        return self.player_pos
 
    def checkbag(self):
        while 1:
            
            answer = input("you check your bag, what do you wish to count?(arrows, horns, check map,close bag)")
            if answer == 'arrows':    
                print()
                print("you have {} arrows left".format(self.arrows))
            
            elif answer  == 'horns':   
                print()
                print("you have {} monster horn(s)".format(self.monsterHorn))
                if self.monsterHorn == 3:
                    print("time to get out of here")
            elif answer == 'check map':
                print()
                print(self.hazard)
            elif answer == 'close bag':
                return
 
    def gameloop(self):
 
        print("Game start")
        print("----------")
        print("Ok new recruit the time has come to go back into the cave ")
        print("and thin out the beasts. try to come back with at least 3 horns if you can.")
        print()
        print("NOTE: there is a map of the cave in your bag")
        print()
        ##set hazard spaces
        self.setHazards()
        ##set player position 
        self.enter(self.player_pos)
        
        while self.torchlight > 0:
            
            print("You are in room {}.".format(self.player_pos))
            
            #use " " as a delimiter and make an iteratable string called leads_to
            #to print element of the list to the user prompt
            leads_to = " ".join([str(x) for x in self.cave[self.player_pos]])
            print("Tunnels lead to {0}".format(leads_to))
 
            answer = self.playerAction()        
            print()                                
            if answer[0] == 'move':
                target = answer[1] 
                self.player_pos = self.enter(target)
                self.torchlight -=1
                print("Your torch has {} steps left before going out".format(self.torchlight))   

                
            elif answer[0] == 'shoot':                
                target = answer[1]
                self.player_pos = self.shoot(target)
                
            elif answer[0] == 'check bag':
                self.checkbag()
                
            elif answer[0] == 'quit':
                self.monsterHorn == 0
                print("you drop your monster horns and run for the exit")
                self.player_pos = -1
            
 
            if self.torchlight == 0:
                print("Your torch flickers out, you cant see a thing")
                self.player_pos = -1
                
            if self.player_pos == -1:
                break                        
        
        ##if you didn' quit count the loot you got
        if self.monsterHorn == 0:
            print("Better luck next time")
        elif self.monsterHorn == 1:
            print("Bronze star, you can do better!")
        elif self.monsterHorn  == 2:
            print("Silver star, not bad try to kill one more")
        elif self.monsterHorn == 3:
            print("Gold star, good job hunter")
        print()
        print("Game over!")    
 
 
if __name__ == '__main__':                        

 
    CL = caveLayout()
    CL.gameloop()
