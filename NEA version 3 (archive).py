import pygame
import sys
import random
import math
import json
import time
#json area
default = {'cursor': {'color': [20, 20, 20], 'pressed': [255, 255, 255]}, 'genes': {'lower': 12, 'upper': 48, 'NameSyllablesLower': 1, 'NameSyllablesHigher': 3, 'NameLengthLower': 1, 'NameLengthHigher': 8}, 'food': {'SizeLower': 1, 'SizeUpper': 6}, 'misc': {'DrawVector': False,'DrawNodes': False,'ShowDebug': False, 'Background': True,'DrawNames': True}}
# this is the library data for the default json file, only used for recovery
try:
    Json = open("config.json")
    Config = json.load(Json)
    Json.close()
except:
    print("exception occured in parsing/finding config.json... attempting to fix")
    file = open("config.json", "a")
    json.dump(default, file)
    file.close()
    Json = open("config.json")
    Config = json.load(Json)
    Json.close()
    print("succesfully restored config.json")

#pygame initiation
pygame.init()
surface = pygame.display.set_mode((800, 600))
font = pygame.font.Font('freesansbold.ttf', 12)
RED = (100,0,0)
DarkRed = (200,0,0)
GREEN = (0,100,0)
BLUE = (0,0,100)
GREY = (128,128,128)
DarkGrey = (90,90,90)
BLACK = (20,20,20)
WHITE = (255,255,255)
YELLOW = (255,255,0)
pygame.mouse.set_visible(False)
#misc variable definition
CurrentPage = ""
ButtonToggle1 = False
ButtonToggle2 = False
StickyTarget = False
FoodRegister = []
SpeciesRegister = []
Nodes = []
#utility/math functions
def VectorCalculation(ObjectPositionX,ObjectPositionY,Range,color,state): #object x is the host
    global Config
    ChangeInX = abs(ObjectPositionY[0] - ObjectPositionX[0])
    ChangeInY = abs(ObjectPositionY[1] - ObjectPositionX[1])
    distance = math.sqrt(Sqr(ChangeInX) + Sqr(ChangeInY))
    if distance < Range:
        if state:
            pygame.draw.line(surface,color,(ObjectPositionX[0],ObjectPositionX[1]),(ObjectPositionY[0],ObjectPositionY[1]))
        return distance
def Sqr(arg):
    return (arg * arg)
def IsPrime(arg): # this checks for prime numbers
    for i in range(2,int(arg**0.5)+1):
        if arg%i==0:
            return False
    return True

def InHitboxRect(X,Y,posX,posY,sizeX,sizeY):
    if posX > X and posX < (X + sizeX): #checks for allignment on the X axis
        if posY > Y and posY < (Y + sizeY): #checks for allignment on the Y axis
            #print("object allignment, details below")
            #print(X,Y,posX,posY,sizeX,sizeY)
            return True
#def GetPosInArray(find,array):
    #for thing in range(len(array)):
        #if find == array[thing]:
            #return thing + 1
    #print("couldnt find",find)
def GetPositionOnClick(mousepos,mousestate,posX,posY,sizeX,sizeY):
    if mousepos[0] > posX and mousepos[0] < (posX + sizeX):
        if mousepos[1] > posY and mousepos[1] < (posY + sizeY):
            if mousestate[0]:
                return mousepos
#ui functions
def DrawColorPicker(x,y,mousepos,mousestate,offsetX,offsetY):
    pygame.draw.rect(surface, BLACK, pygame.Rect(x,y,261,261))
    pygame.draw.rect(surface, WHITE, pygame.Rect((x+3),(y+3),255,255))
    for color in range(256):
        pygame.draw.line(surface,(offsetX,offsetY,color),((x + color + 3),(y + 3)),((x + color + 3),(y + 258)))
    if (GetPositionOnClick(mousepos,mousestate,x+3,y+3,255,255)) != None:
        Color = list(GetPositionOnClick(mousepos,mousestate,x+3,y+3,255,255))
        SelectedColor = (offsetX,offsetY,(Color[0] - x+3))
        return SelectedColor
class button:
   
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,text,textcolor):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.text = text
        self.textcolor = textcolor
        self.LastPress = False
    def DrawButton(self,mousepos,mousestate):
        pygame.draw.rect(surface, DarkGrey, pygame.Rect(self.position[0] - 3,self.position[1] - 3,self.size[0] + 6,self.size[1] + 6))
        if mousestate[0] == False and InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]): #hovered but not clicked
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #this is the hovered state of the button
        
        elif mousestate[0] == True and InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]) and mousestate[0] != self.LastPress: #pressed
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #pressed state
            self.LastPress = True
            return True
       
        else:
            self.LastPress = False
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])) #this is the static state of the button
           
        text = font.render(self.text, True, self.textcolor, GREY)
        surface.blit(text,(self.position[0] + self.size[0] + 3,self.position[1] + (self.size[1] // 2)))
       
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.text,self.textcolor)
class slider:
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,slidersize,level,text):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.sliderpos = [position[0],(position[1] + level)]
        self.slidersize = slidersize
        self.text = text
    def DrawSlider(self,mousepos,mousestate):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        text = font.render(self.text + ":" + str(self.sliderpos[1] - self.position[1]), True, BLACK, GREY)
        surface.blit(text,(self.position[0] + self.size[0],self.position[1]))
        if InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0] + 10),(self.slidersize[1] + 10)) and mousestate[0] == 1:
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
            if self.sliderpos[1] >= self.position[1]:
                if self.sliderpos[1] <= (self.position[1] + self.size[1]):
                    self.sliderpos[1] = (mousepos[1] - 5)
                else:
                    self.sliderpos[1] = (self.position[1] + (self.size[1] - self.slidersize[1]))
            else:
                self.sliderpos[1] = self.position[1]
        elif InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0]),(self.slidersize[1])):
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
        else:
            pygame.draw.rect(surface, WHITE, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))

        if (self.sliderpos[1] - self.position[1]) < (self.size[1] - self.slidersize[1]):
            if (self.sliderpos[1] - self.position[1]) > 0:
                return (self.sliderpos[1] - self.position[1])
            else:
                return 0
        else:
            return (self.size[1] - self.slidersize[1])
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.sliderpos,self.slidersize)
class SideSlider:
    def  __init__(self,size,position,color,pressedcolor,hoveredcolor,slidersize,text):
        self.size = size
        self.position = position
        self.color = color
        self.pressedcolor = pressedcolor
        self.hoveredcolor = hoveredcolor
        self.sliderpos = [position[0],position[1]]
        self.slidersize = slidersize
        self.text = text
    def DrawSlider(self,mousepos,mousestate):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        text = font.render(self.text + ":" + str(self.sliderpos[0] - self.position[0]), True, BLACK, GREY)
        surface.blit(text,(self.position[0] + self.size[0] + self.slidersize[0],self.position[1]))
        if InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0] + 10),(self.slidersize[1] + 10)) and mousestate[0] == 1:
            pygame.draw.rect(surface, self.pressedcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
            if self.sliderpos[0] >= self.position[0]:
                if self.sliderpos[0] <= (self.position[0] + self.size[0]):
                    self.sliderpos[0] = (mousepos[0] - 10)
                else:
                    self.sliderpos[0] = (self.position[0] + (self.size[0] - self.slidersize[0]))
            else:
                self.sliderpos[0] = self.position[0]
        elif InHitboxRect(self.sliderpos[0],self.sliderpos[1],mousepos[0],mousepos[1],(self.slidersize[0]),(self.slidersize[1])):
            pygame.draw.rect(surface, self.hoveredcolor, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
        else:
            pygame.draw.rect(surface, WHITE, pygame.Rect(self.sliderpos[0],self.sliderpos[1],self.slidersize[0],self.slidersize[1]))
           
        if (self.sliderpos[0] - self.position[0]) < (self.size[0] - self.slidersize[0]):
            if (self.sliderpos[0] - self.position[0]) > 0:
                return (self.sliderpos[0] - self.position[0])
            else:
                return 0
        else:
            return (self.size[0] - self.slidersize[0])
    def Output(self):
        print(self.size,self.position,self.color,self.pressedcolor,self.hoveredcolor,self.sliderpos,self.slidersize)
class CheckBox():
    def __init__(self,size,position,color,HoverColor,CheckColor,state,text):
        self.size = size
        self.position = position
        self.color = color
        self.HoverColor = HoverColor
        self.CheckColor = CheckColor
        self.state = state
        self.text = text
        self.LastPress = False
    def Draw(self,mousepos,mousestate):
        if InHitboxRect(self.position[0],self.position[1],mousepos[0],mousepos[1],self.size[0],self.size[1]):
            pygame.draw.rect(surface, self.HoverColor, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
            if mousestate[0] and mousestate[0] != self.LastPress:
                self.LastPress = mousestate[0]
                self.state = not self.state
            else:
                self.LastPress = mousestate[0]
        else:
            pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        if self.state:
            pygame.draw.line(surface,self.CheckColor,(self.position[0],self.position[1]),(self.position[0] + self.size[0],self.position[1] + self.size[1]))
            pygame.draw.line(surface,self.CheckColor,(self.position[0] + self.size[0],self.position[1]),(self.position[0],self.position[1] + self.size[1]))
        text = font.render(self.text, True, BLACK, GREY)
        surface.blit(text,(self.position[0] + self.size[0],self.position[1]))
        return self.state
def DrawCustomCursor(mousepos,mousestate):
    global Config
    if mousestate[0] == 1:
        pygame.draw.rect(surface, Config["cursor"]["pressed"], pygame.Rect((mousepos[0]+5),(mousepos[1]+5),(3),(3)))
    else:
        pygame.draw.rect(surface, Config["cursor"]["color"], pygame.Rect((mousepos[0]+5),(mousepos[1]+5),(3),(3)))
#simulation functions
def InitiateSpeciesObject():
    global Config
    name = ""
    genes = []
    charcolor = []
    charsize = []
    color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    size = (random.randint(35,65),random.randint(35,65))
    position = [random.randint(100,700),random.randint(100,500)]
    Range = random.randint(100,175) # range at which they will look for food
    Capacity = random.randint(10,size[1]) # capacity for which they can store food
    for i in range(random.randint(Config["genes"]["NameLengthLower"],Config["genes"]["NameLengthHigher"])):
        for o in range(random.randint(Config["genes"]["NameSyllablesLower"],Config["genes"]["NameSyllablesHigher"])): #this generates alien like names
            name += chr(random.randint(65,122))
        name += "-"
    for i in range(random.randint(Config["genes"]["lower"],Config["genes"]["upper"])): #genetic code generator, codes for the appearance
        X = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        genes.append(random.randint(1,size[0]))
        genes.append(random.randint(1,size[1]))
        charcolor.append(X)
        charsize.append(random.randint(1,4))      
    SpeciesRegister.append(Species(name,color,charcolor,size,charsize,position,genes,Range,Capacity))
def CreateFoodObject():
    global Config
    position = [random.randint(100,700),random.randint(100,500)]
    color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
    size = random.randint(1,6)
    dotsize = random.randint(0,(size // 2))
    FoodRegister.append(Food(position,color,size,dotsize))
class Food:
    def __init__(self,position,color,size,dotsize):
        self.position = position
        self.color = color
        self.size = size
        self.dotsize = dotsize
       
    def DrawFoodObject(self):
        pygame.draw.circle(surface, self.color,(self.position[0],self.position[1]),(self.size))
        pygame.draw.circle(surface, BLACK,(self.position[0],self.position[1]),(self.dotsize))
        return self.position
    def Output(self):
        print(self.position,self.color,self.size,self.dotsize)
class Node:
    def __init__(self,position):
        self.position = position
    def DrawNode(self):
        pygame.draw.circle(surface, YELLOW,(self.position[0],self.position[1]),2)
def InitiateNodesLattice():
    x = 100
    y = 100
    for a in range(40):
        for b in range(60):
            Nodes.append(Node((x,y)))
            x += 10
        y += 10
        x = 100
    if Config["misc"]["ShowDebug"]:
        print("succesfully initiated all nodes!")
class Species:
   
    def  __init__(self, name, color, charcolor, size, charsize, position, genes,Range,Capacity):
        self.name = name
        self.color = color
        self.charcolor = charcolor
        self.size = size
        self.charsize = charsize
        self.position = position
        self.genes = genes
        self.range = Range
        self.capacity = Capacity
        self.saturation = 10
        self.RememberedTargetsID = []
        self.RememberedTargetsPositions = []
    def DrawSprite(self):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1]))
        pygame.draw.rect(surface, WHITE, pygame.Rect(self.position[0] - 5,self.position[1],2,self.capacity))
        pygame.draw.rect(surface, BLUE, pygame.Rect(self.position[0] - 5,self.position[1],2,self.saturation))
        if Config["misc"]["DrawNames"]:
            text = font.render(self.name, True, BLACK, GREY)
            surface.blit(text,((self.position[0] + self.size[0]),(self.position[1])))
        factor = 0
        for Pointer in range((len(self.genes) // 2) - 2):
            Horizontal = (self.position[0] + self.size[0])
            Down = (self.position[1] + self.size[1])
            X = (Horizontal - self.genes[factor])
            Y = (Down - self.genes[factor + 1])
            A = (Horizontal - self.genes[factor+2])
            B = (Down - self.genes[factor+3])
           
            if self.genes[factor] % 2 == 0: #even check
                pygame.draw.circle(surface, self.charcolor[Pointer],(X,Y),self.charsize[Pointer])
            elif IsPrime(self.genes[factor]):
                pygame.draw.line(surface,self.charcolor[Pointer],(X,Y),(A,B))
            else:
                pygame.draw.rect(surface, self.charcolor[Pointer], pygame.Rect(X,Y,self.charsize[Pointer],self.charsize[Pointer]))
                 
            factor += 2
        if Config["misc"]["DrawVector"]:
            pygame.draw.circle(surface, RED, (self.position[0] + (self.size[0] // 2),self.position[1] + (self.size[1] // 2)), self.range, 1)
        return self.position
   
    def TargetMove(self):
        global Config
        #print(TargetPos,self.position)
        X = self.position[0] + (self.size[0] // 2)
        Y = self.position[1] + (self.size[1] // 2)
        if X != 0 and X < 800:
            if self.TargetPos[0] < math.floor(X):
                self.position[0] -= 1
            elif self.TargetPos[0] != math.floor(X):
                self.position[0] += 1
        if Y != 0 and Y < 600:
            if self.TargetPos[1] < math.floor(Y):
                self.position[1] -= 1
            elif self.TargetPos[1] != math.floor(Y):
                self.position[1] += 1
        if self.TargetPos[0] == math.floor(X) and self.TargetPos[1] == math.floor(Y):
            if Config["misc"]["ShowDebug"]:
                print("reached food at:" ,self.TargetPos)
            self.saturation += 1
            #print(self.eaten)
            return True
        if Config["misc"]["DrawVector"] and self.TargetType == "Root":
            pygame.draw.line(surface,BLUE,(X,Y),(self.TargetPos[0],self.TargetPos[1]))
        elif Config["misc"]["DrawVector"]:
            pygame.draw.line(surface,GREEN,(X,Y),(self.TargetPos[0],self.TargetPos[1]))
        if self.TargetId not in FoodRegister:
            self.DeleteTarget()
    def ReturnTarget(self):
        try:
            return self.target
        except:
            return None
    def DeleteTarget(self):
        del self.RememberedTargetsID[self.RememberedTargetsID.index(self.TargetId)]
        del self.RememberedTargetsPositions[self.RememberedTargetsPositions.index(self.TargetId.position)]
        del self.target
        del self.TargetPos
        del self.TargetId
        del self.TargetType
    def GoTo(self,TargetPos):
        global Config
        #print(TargetPos,self.position)
        X = self.position[0] + (self.size[0] // 2)
        Y = self.position[1] + (self.size[1] // 2)
        if X != 0 and X < 800:
            if TargetPos[0] < math.floor(X):
                self.position[0] -= 1
            elif TargetPos[0] != math.floor(X):
                self.position[0] += 1
        if Y != 0 and Y < 600:
            if TargetPos[1] < math.floor(Y):
                self.position[1] -= 1
            elif TargetPos[1] != math.floor(Y):
                self.position[1] += 1
        if TargetPos[0] == math.floor(X) and TargetPos[1] == math.floor(Y):
            return True
        if Config["misc"]["DrawVector"]:
            pygame.draw.line(surface,YELLOW,(X,Y),(TargetPos[0],TargetPos[1]))
    def RandomizePos(self):
        self.position[0] = random.randint(100,700)
        self.position[1] = random.randint(100,500)
    def Vector(self,TargetPos,color,state,UseRange):
        if UseRange:
            Ping = VectorCalculation((self.position[0] + (self.size[0] // 2), self.position[1] + (self.size[1] // 2)),TargetPos,self.range,color,state)
        else:
            Ping = VectorCalculation((self.position[0] + (self.size[0] // 2), self.position[1] + (self.size[1] // 2)),TargetPos,1000000,color,state)
        return Ping
    def GetTarget(self,array,index,ID):
        if len(array) != 0:
            self.target = min(array)
            self.target = array.index(self.target)
            self.TargetPos = index[self.target]
            self.TargetId = ID[self.target]
            self.TargetType = "Root"
            for MemoryTargets in ID:
                if MemoryTargets not in self.RememberedTargetsID:
                    self.RememberedTargetsID.append(MemoryTargets)
                    self.RememberedTargetsPositions.append(MemoryTargets.position)
                    #if Config["misc"]["ShowDebug"]:
                        #print(MemoryTargets,"already in target memory")
            #print("selected",self.target,"from",array,index)
            return True
    def RetrieveTargetFromMemory(self):
        Targets = []
        for PotentialTarget in self.RememberedTargetsID:
            if PotentialTarget not in FoodRegister:
                del self.RememberedTargetsID[self.RememberedTargetsID.index(PotentialTarget)]
                del self.RememberedTargetsPositions[self.RememberedTargetsPositions.index(PotentialTarget.position)]
            else:
                Targets.append(self.Vector(PotentialTarget.position,GREEN,Config["misc"]["DrawNodes"],False))
        if len(Targets) != 0:
            self.target = min(Targets)
            self.target = Targets.index(self.target)
            self.TargetPos = self.RememberedTargetsPositions[self.target]
            self.TargetId = self.RememberedTargetsID[self.target]
            self.TargetType = "Memory"
            return True
    def GetNodeTarget(self):
        try:
            return self.NodeTarget
        except:
            return None
    def SetNodeTarget(self,NodeTarget):
        self.NodeTarget = NodeTarget
    def DeleteNodeTarget(self):
        del self.NodeTarget
    def Output(self):
        self.name,self.color,self.charcolor,self.size,self.charsize,self.position,self.genes
def DrawAll():
    for species in range(len(SpeciesRegister)):
        Targets = []
        Indexes = []
        TargetId = []
        ReachableNodes = []
        pos = SpeciesRegister[species].position
        #print(Nodes)
        for Node in Nodes:
            if Config["misc"]["DrawNodes"]:
                Node.DrawNode()
            if abs(Node.position[0] - pos[0]) < 175:
                if abs(Node.position[1] - pos[1]) < 175:
                    NodeCheck = SpeciesRegister[species].Vector(Node.position,YELLOW,Config["misc"]["DrawNodes"],True)
                    if NodeCheck != None:
                        ReachableNodes.append(Node.position)
        for food in range(len(FoodRegister)):
            if abs((FoodRegister[food].DrawFoodObject())[0] - pos[0]) < 175:
                if abs((FoodRegister[food].position)[1] - pos[1]) < 175:
                    Ping = SpeciesRegister[species].Vector(FoodRegister[food].DrawFoodObject(),RED,Config["misc"]["DrawVector"],True)
                    if Ping != None:
                        Targets.append(Ping)
                        Indexes.append(FoodRegister[food].position)
                        TargetId.append(FoodRegister[food])
        if len(Targets) != 0 and SpeciesRegister[species].ReturnTarget() == None:
            SpeciesRegister[species].GetTarget(Targets,Indexes,TargetId)
            if Config["misc"]["ShowDebug"]:
                print("SetFoodTarget at", SpeciesRegister[species].TargetPos)
        elif SpeciesRegister[species].ReturnTarget() != None:
            if (SpeciesRegister[species].TargetMove()):
                try:
                    if Config["misc"]["ShowDebug"]:
                        print("deleted:", FoodRegister.index(SpeciesRegister[species].TargetId), "from food register")
                    del FoodRegister[FoodRegister.index(SpeciesRegister[species].TargetId)]
                    SpeciesRegister[species].DeleteTarget()

                except:
                    if Config["misc"]["ShowDebug"]:
                        print("prevented an exception: overlapping food target")
                    SpeciesRegister[species].DeleteTarget()
                    SpeciesRegister[species].RandomizePos()
        elif SpeciesRegister[species].RetrieveTargetFromMemory():
            if Config["misc"]["ShowDebug"]:
                print("retrieved a target from memory")
        elif SpeciesRegister[species].GetNodeTarget() == None:
            SpeciesRegister[species].SetNodeTarget(random.choice(ReachableNodes))
            if Config["misc"]["ShowDebug"]:
                print("SetNodeTarget at", SpeciesRegister[species].GetNodeTarget())
        else:
            if SpeciesRegister[species].GoTo(SpeciesRegister[species].GetNodeTarget()):
                if Config["misc"]["ShowDebug"]:
                    print("reached node target at", SpeciesRegister[species].GetNodeTarget())
                SpeciesRegister[species].DeleteNodeTarget()
        
        SpeciesRegister[species].DrawSprite()
#loop functions
def OptionPage(mousepos,mousestate):
    global CurrentPage
    global ButtonToggle1
    global ButtonToggle2
    if back.DrawButton(mousepos,mousestate):
        CurrentPage = ""
    if save.DrawButton(mousepos,mousestate):
        json.dump(Config,open("config.json","w"))
        Unsaved = Config
    if DrawVector.Draw(mousepos,mousestate) != Config["misc"]["DrawVector"]:
        Config["misc"]["DrawVector"] = not Config["misc"]["DrawVector"]
    if DrawNodes.Draw(mousepos,mousestate) != Config["misc"]["DrawNodes"]:
        Config["misc"]["DrawNodes"] = not Config["misc"]["DrawNodes"]
    if Debug.Draw(mousepos,mousestate) != Config["misc"]["ShowDebug"]:
        Config["misc"]["ShowDebug"] = not Config["misc"]["ShowDebug"]
    if DrawNames.Draw(mousepos,mousestate) != Config["misc"]["DrawNames"]:
        Config["misc"]["DrawNames"] = not Config["misc"]["DrawNames"]
    if BackGround.Draw(mousepos,mousestate) != Config["misc"]["Background"]:
        Config["misc"]["Background"] = not Config["misc"]["Background"]
    if (GeneRangeUpper.DrawSlider(mousepos,mousestate)) > Config["genes"]["lower"]:
        Config["genes"]["upper"] = (GeneRangeUpper.DrawSlider(mousepos,mousestate))
    if (GeneRangeLower.DrawSlider(mousepos,mousestate) < Config["genes"]["upper"]):
        Config["genes"]["lower"] = (GeneRangeLower.DrawSlider(mousepos,mousestate))
    if not ButtonToggle2:
        if (CustomCursorClicked.DrawButton(mousepos,mousestate)) or ButtonToggle1:
            ButtonToggle1 = True
            offsetX = colorR1.DrawSlider(mousepos,mousestate)
            offsetY = colorG1.DrawSlider(mousepos,mousestate)
            if DrawColorPicker(500,185,mousepos,mousestate,offsetX,offsetY) != None:
                ButtonToggle1 = False
                Config["cursor"]["pressed"] = list(DrawColorPicker(500,185,mousepos,mousestate,offsetX,offsetY))
    if not ButtonToggle1:
        if (CustomCursor.DrawButton(mousepos,mousestate)) or ButtonToggle2:
            ButtonToggle2 = True
            offsetX = colorR2.DrawSlider(mousepos,mousestate)
            offsetY = colorG2.DrawSlider(mousepos,mousestate)
            if DrawColorPicker(500,235,mousepos,mousestate,offsetX,offsetY) != None:
                ButtonToggle2 = False
                Config["cursor"]["color"] = list(DrawColorPicker(500,235,mousepos,mousestate,offsetX,offsetY))
def InfoPage(mousepos,mousestate):
    global CurrentPage
    if back.DrawButton(mousepos,mousestate):
        CurrentPage = ""
    text = font.render("this is a project produced by henry frodsham in 12C, its a simulation of natural selection", True, BLACK, GREY)
    surface.blit(text,(150,400))
def Simulation(mousepos,mousestate):
    DrawAll()
#ui elements
   
SpawnFood = button((50,30),(0,0),(40,40,40),DarkRed,RED,"FOOD",BLACK)
play = button((50,30),(360,500),(40,40,40),DarkRed,RED,"start simulation",BLACK)
back = button((50,30),(3,567),(40,40,40),DarkRed,RED,"BACK",BLACK)
save = button((50,30),(103,567),(40,40,40),DarkRed,RED,"SAVE",BLACK)
options = button((50,30),(200,500),(40,40,40),DarkRed,RED,"OPTIONS",BLACK)
information = button((50,30),(510,500),(40,40,40),DarkRed,RED,"INFO",BLACK)
CustomCursor = button((50,30),(500,200),(40,40,40),DarkRed,RED,"change cursor color",BLACK)
CustomCursorClicked = button((50,30),(500,150),(40,40,40),DarkRed,RED,"change pressed cursor color",BLACK)
GeneRangeLower = slider((20,80),(40,300),BLACK,DarkRed,RED,(20,20),Config["genes"]["lower"],("CHANGE GENE LOWER BOUND"))
GeneRangeUpper = slider((20,80),(40,200),BLACK,DarkRed,RED,(20,20),Config["genes"]["upper"],("CHANGE GENE UPPER BOUND"))
colorR1 = SideSlider((255,20),(500,450),BLACK,DarkRed,RED,(20,20),("RED"))
colorG1 = SideSlider((255,20),(500,490),BLACK,DarkRed,RED,(20,20),("GREEN"))
colorR2 = SideSlider((255,20),(500,500),BLACK,DarkRed,RED,(20,20),("RED"))
colorG2 = SideSlider((255,20),(500,540),BLACK,DarkRed,RED,(20,20),("GREEN"))
DrawVector = CheckBox((20,20),(40,40),BLACK,DarkRed,(0,200,0),Config["misc"]["DrawVector"],"visualie vectors")
DrawNodes = CheckBox((20,20),(40,70),BLACK,DarkRed,(0,200,0),Config["misc"]["DrawNodes"],"visualize nodes")
Debug = CheckBox((20,20),(40,100),BLACK,DarkRed,(0,200,0),Config["misc"]["ShowDebug"],"print debug data to console")
BackGround = CheckBox((20,20),(40,130),BLACK,DarkRed,(0,200,0),Config["misc"]["Background"],"Draw background")
DrawNames = CheckBox((20,20),(40,160),BLACK,DarkRed,(0,200,0),Config["misc"]["DrawNames"],"Draw Names")
InitiateSpeciesObject()
InitiateSpeciesObject()
InitiateSpeciesObject()
InitiateNodesLattice()
for i in range(300):
    CreateFoodObject()
    
#main loop, in a function to allow for partial looping
def main():
    timeX = time.time()
    global CurrentPage
    global Config
    mousepos = pygame.mouse.get_pos()
    mousestate = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print("json dumped",Config)
            json.dump(Config,open("config.json","w")) #more optimised as it saves everytime the user quits not everytime there is a change
            sys. exit()
    if Config["misc"]["Background"]:
        surface.fill(GREY)
    else:
        surface.fill(WHITE)
    if CurrentPage == "":
        if information.DrawButton(mousepos,mousestate):
            CurrentPage = "InfoPage"
        elif options.DrawButton(mousepos,mousestate):
            CurrentPage = "OptionPage"
        elif play.DrawButton(mousepos,mousestate):
             CurrentPage = "Simulation"
    elif CurrentPage == "InfoPage":
        InfoPage(mousepos,mousestate)
    elif CurrentPage == "OptionPage":
        OptionPage(mousepos,mousestate)
    elif CurrentPage == "Simulation":
        Simulation(mousepos,mousestate)
    DrawCustomCursor(mousepos,mousestate) #the cursor should be drawn after everything else
    timeY = time.time()
    try:
        fps = math.ceil(1 / (timeY - timeX))
        text = font.render("fps: " + str(fps), True, BLACK, GREY)
        surface.blit(text,(0,0))
    except:
        text = font.render("fps: 1000", True, BLACK, GREY)
        surface.blit(text,(0,0))
    pygame.display.flip()

while True:
    main()
