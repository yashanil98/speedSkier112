from cmu_graphics import *
from PIL import Image
import os, pathlib

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def drawGhost(self, app):
        newWidth, newHeight = (app.imageWidth2/4, app.imageHeight2/4)
        drawImage(app.image2,self.x, self.y, width=newWidth,height=newHeight,
                   align = "center")
        
    def moveGhost(self, tup):
        if type(tup) != bool:
            x,y = tup
            self.x = x
            self.y = y
            #print(x, y)

    def ghostWins(self,skier):
        return self.y > skier.skiCy + 20
