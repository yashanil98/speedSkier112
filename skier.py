from cmu_graphics import *
import random
from PIL import Image
import os, pathlib
from physics import *

#####skier.py   

class Skier():
    def __init__(self, app):
        #position
        self.skiCx = app.width/2
        self.skiCy = app.height/4
        #thetaLeft and thetaRight created to solve onKeyHold issue
        #theta wasn't restarted because you can't have an else in onKeyHold
        #creating self for left and right solved the issue
        self.thetaLeft = 0
        self.thetaRight = 0
        
    def moveLeft(self, app):
        #constant increase in theta for every call
        self.thetaLeft += 0.05 # change later
        #restarts right theta (solved issue)
        self.thetaRight = 0
        #if theta wouldn't decrease speed to negatives
        if app.speed - bankedCurve(self.thetaLeft) <= 0:
            #then change speed
            app.speed -= bankedCurve(self.thetaLeft)
        #also use left theta to change x
        self.skiCx -= forceTurn(self.thetaLeft, app.hillAngle) + 1
        
    def moveRight(self, app):
        #constant increase in theta for every call
        self.thetaRight += 0.05
        #restarts left theta (solved issue)
        self.thetaLeft = 0
        #if theta wouldn't decrease speed to negatives
        if app.speed - bankedCurve(self.thetaRight) <= 0:
            #then change speed
            app.speed -= bankedCurve(self.thetaRight)
            
        #also use right theta to change x
        self.skiCx += forceTurn(self.thetaRight, app.hillAngle) + 1
        #print(self.skiCx)

#draws the skier based on image in app
    def drawSkier(self, app):
        newWidth, newHeight = (app.imageWidth/8, app.imageHeight/8)
        drawImage(app.image,self.skiCx, self.skiCy,
                   width=newWidth,height=newHeight, align = "center")

