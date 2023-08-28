from cmu_graphics import *
from PIL import Image
import os, pathlib
import random

class Snowball:
    def __init__(self, app):
        self.ballX = -20
        self.ballY = random.randint(0,app.height)
        self.dY = random.randint(-2,2)
    
    def drawBall(self,app):
        newWidth, newHeight = (app.imageWidth2/4, app.imageHeight2/4)
        drawImage(app.image3,self.ballX, self.ballY, width=newWidth,
                  height=newHeight, align = "center")
    
    def moveBall(self):
        if self.ballX >= app.width:
            self.ballX = -20
            self.ballY = random.randint(0,app.height)
            self.dY = random.randint(-2,2)

        else:
            self.ballX += 5
            self.ballY += self.dY

    def touchingSkier(self, other):
        d = distance(self.ballX, self.ballY, other.skiCx, other.skiCy)
        return d < 30
    
    def distance(x1,y1,x2,y2):
        return ((x2-x1)**2 + (y2-y1)**2)**0.5

        
        