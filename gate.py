from cmu_graphics import *
import random
from PIL import Image
import os, pathlib

#####gate.py          
        
class Gates():
    #class Attributes
    #all the gates being printed on screen
    allGates = []
    #points to draw
    points = []
    def __init__(self, app, height = 0):
        #if left gate / right gate different random position to choose from
        if app.side:
            self.gateCx = random.randint(4 * app.width/8, 6 * app.width/8)
        elif not app.side:
            self.gateCx = random.randint(2 * app.width/8, 3 * app.width/8)
        self.gateCy = app.height + height
        #left or right gate
        self.rightSide = app.side
        #add gate to allGates
        Gates.allGates.append(self)
        #only checks properTurn onces so cleaner display
        self.checked = False
    
    def properTurn(self, skier):
        self.checked = True
        if self.rightSide:
            #is the skier on the right or wrong side of the gate
            return self.gateCx < skier.skiCx
        else:
            return skier.skiCx < self.gateCx
            
    def drawGates():
        #draws gate using image given in app
        for gate in Gates.allGates:
            newWidth, newHeight = (app.imageWidth1/10, app.imageHeight1/10)
            drawImage(app.image1, gate.gateCx, gate.gateCy, opacity = 70,
                      width=newWidth,height=newHeight, align = "center")
            
    @staticmethod
    #draws all the points using class attribute (so must be a static method)
    def drawPoints():
        for i in range(1, len(Gates.points)):
            if (type(Gates.points[i]) != bool and 
                type(Gates.points[i - 1]) != bool):
                x1, y1 = Gates.points[i - 1]
                x2, y2 = Gates.points[i]
                #current and previous points (draws a line between them) giving
                #allusion of it being a curve
                drawLine(x1, y1, x2, y2)
            
    
    @staticmethod
    def pathToPoints(connectPoints):
        points = None
        for gatetogate in connectPoints:
            x1, x2, x3, y1, y2, y3, c, rightSide = gatetogate
            #print(x1, x2, x3, c)
            gatesDistance = abs(x2 - x1)
            points = []
            for i in range(43, gatesDistance - 43):
                if not rightSide:
                    x = x1 + i
                    y = (x - x1) * (x - x2) * c
                    if gatesDistance / 2 <= i:
                        y = (y3 - y) + y3
                elif rightSide:
                    x = x2 + i
                    y = (x - x1) * (x - x2) * c
                    if not gatesDistance / 2 <= i:
                        y = (y3 - y) + y3
                #print(x)
                points.append((x,y))
        if rightSide:
            Gates.points += points[::-1] + [True] * 8
        else:
            Gates.points += points + [True] * 8
        
            
    @staticmethod     
    def makePath(app):
        connectPoints = []
        for i in range(1, len(Gates.allGates)):
            gate1 = Gates.allGates[i - 1]
            gate2 = Gates.allGates[i]
            #current gate and previous gate
            #so you don't "double dip" gates
            #print(gate1.gateCx,gate1.gateCy,gate2.gateCx,gate2.gateCy)
            if gate1.rightSide:
                #different positions for x, y based on whether 
                #it is right or left
                x1,y1 = gate1.gateCx + 60, gate1.gateCy  - 100
                x2,y2 = gate2.gateCx - 60, gate2.gateCy  + 100
            else:
                x1,y1 = gate1.gateCx - 60, gate1.gateCy + 100
                x2,y2 = gate2.gateCx + 60, gate2.gateCy - 100 
            #midpoint skier
            x3,y3 = (x1 + x2)/2, (y1 + y2)/2
            #uses midpoint to find the c in quadratic
            c = y3 / ((x3 - x1) * (x3 - x2))
            
            #big tuple added to connectPoints
            gatetogate = (x1,x2,x3,y1, y2, y3, c,gate1.rightSide)
            connectPoints.append((gatetogate))
        Gates.pathToPoints(connectPoints)
    
    @staticmethod
    #heart of the program
    def gateSteps(app):
        #change mod to change gates speed
        for gate in Gates.allGates:
            #once a gates fully off screen and does effect the path
            if gate.gateCy < -100:
                #change sides
                app.side = not app.side
                #create a new gate
                Gates(app)
                #make a new path
                Gates.makePath(app)
                #increase speed constantly based on gravity
                app.speed += 0.10
                #remove the old gate
                Gates.allGates.remove(gate)
                #Gates.points = Gates.points[:(len(Gates.points)/2)]
            gate.gateCy -=  app.speed
        
            #5 can be customized based on speed
        for i in range(len(Gates.points)):
            if type(Gates.points[i]) != bool:
                x,y = Gates.points[i]
                Gates.points[i] = (x, y - app.speed)
