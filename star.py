from cmu_graphics import *
from PIL import Image
import os, pathlib
import random

class Star:
    def __init__(self, app):
        self.starX = -20
        self.starY = random.randint(0,app.height)
        self.dY = random.randint(-2,2)
    
    def drawStar(self,app):
        newWidth, newHeight = (app.imageWidth4/4, app.imageHeight4/4)
        drawImage(app.image4,self.starX, self.starY, width=newWidth,
                  height=newHeight, align = "center")
    
    def moveStar(self):
        if self.starX >= app.width:
            self.starX = -20
            self.starY = random.randint(0,app.height)
            self.dY = random.randint(-2,2)
        else:
            self.starX += 5
            self.starY += self.dY

    def touchingSkier(self, other):
        d = distance(self.starX, self.starY, other.skiCx, other.skiCy)
        return d < 30
    
    def distance(x1,y1,x2,y2):
        return ((x2-x1)**2 + (y2-y1)**2)**0.5

        
        