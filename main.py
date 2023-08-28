from cmu_graphics import *
from gate import *
from skier import *
from ghost import *
from snowball import *
from star import *
import random
from PIL import Image
import os, pathlib
#####app1.py   
     
def onAppStart(app):
    #model variables
    app.stepsPerSecond = 20
    app.gameStarted = False
    app.hillAngle = 30
    #if the game hasn't started restart app (starting the game)
    if not app.gameStarted:
        restartApp(app)
    #images defined in app
    getImages(app)
    
def restartApp(app):
    #Ski racer 
    app.gameStarted = False
    app.racer = Skier(app)
    app.lives = 3
    app.proper = None
    app.speed = 5 
    #gates
    Gates.allGates = []
    Gates.points = []
    app.side = bool(random.randint(0,1))
    #used for seconds
    app.steps = 0
    #show guide or not
    app.points = False
    #ghost
    app.ghost = Ghost(100,1)
    app.pointIndex = -1
    app.quadWait = 0
    #snowballs 
    app.snowball = Snowball(app)
    app.touching = False
    #stars
    app.star = Star(app)
    app.touching1 = False
    
def onStep(app):
    #only once the game starts start adding gates, et
    if app.gameStarted and app.lives != 0:
        Gates.gateSteps(app)
        app.steps  += 1
        checkProper(app)
        app.snowball.moveBall()
        app.star.moveStar()

        if app.snowball.touchingSkier(app.racer):
            if not app.touching:
                app.lives -= 1
                app.touching = True
        else:
            app.touching = False

        if app.star.touchingSkier(app.racer):
            if not app.touching1:
                app.lives += 1
                app.touching1 = True
        else:
            app.touching1 = False


        if app.steps % 2 == 0 and app.steps >= 150 and app.points:
            ghostMoving(app)  
            if app.ghost.ghostWins(app.racer): app.lives = 0
        if len(Gates.points) > 400: 
            delete = len(Gates.points) - 400
            Gates.points = Gates.points[delete:]
            app.pointIndex -= delete
    #this is for the first step
        if app.steps == 1:
            Gates(app, 50)
            app.side = not app.side
            Gates(app, 350)
 
def onKeyHold(app, keys):
    #only once the game starts start start checking left or right
    if app.gameStarted:
        if 'left' in keys: 
            x = 1
            app.racer.moveLeft(app)
        elif 'right' in keys: 
            x = 1
            app.racer.moveRight(app)
        elif 'up' in keys and app.speed >= 5:
            app.speed -= 0.5

def onKeyPress(app, key):
    #start game and pause using space
    if key == 'space':
        app.gameStarted = not app.gameStarted
    #only once the game starts start start guide if wanted
    if app.gameStarted:
        if key == 'g':
            app.points = not app.points
        if key == "r":
            restartApp(app)
def redrawAll(app):
    drawBackground(app)
    #game starter page
    if not app.gameStarted:
        drawStarter(app)
    elif app.lives == 0:
        #game ending page
        drawEnd(app)
    else:
        #while game going
        drawScore(app)#scoreboard
        #only draw points once
        if app.points == True:
            #print(app.ghost.x, app.ghost.y)
            Gates.drawPoints()
            app.ghost.drawGhost(app)
        app.racer.drawSkier(app)
        Gates.drawGates()

        app.snowball.drawBall(app)
        app.star.drawStar(app)

        #timer and lives leftapp.width/2, 3 * app.height/8
        drawScore(app)
        #proper turn or not
        if app.proper:
            drawLabel("You made a proper turn! :)" , 
                    app.width/2, app.height/8)
        elif app.proper != None:
            drawLabel("You missed a gate! You lost a live :(" , 
                    app.width/2, app.height/8)

#onStep functions

def ghostMoving(app):
    firstIndex = -1
    for i in range(len(Gates.points)):
            if type(Gates.points[i]) != bool:
                x,y = Gates.points[i]
                if (x >= 0 and x <= app.width and y >= 0 and y <= app.width):
                    firstIndex = i
                    break
            else:
                app.quadWait += 1
                x,y = app.ghost.x, app.ghost.y
                app.ghost.moveGhost((x,y - app.speed))

    if app.quadWait % 1 == 0:
        if app.pointIndex != -1:
            app.ghost.moveGhost(Gates.points[app.pointIndex])
        elif firstIndex != -1:
            app.pointIndex = 0
            app.ghost.moveGhost(Gates.points[firstIndex])
        app.pointIndex += 8




def checkProper(app):
    for gate in Gates.allGates:
            if app.racer.skiCy >= gate.gateCy and not gate.checked:
                properTurn = gate.properTurn(app.racer)
                if not properTurn:
                    #now label "You missed a gate!" can be drawn
                    app.proper = False
                    #if not a properTurn skier loses a life
                    app.lives -= 1
                else:
                    #now label "you made a proper turn" can be drawn
                    app.proper = True


#view
def drawStarter(app):
    newWidth, newHeight = (0.82 * app.imageWidth7, 0.82 * app.imageHeight7)
    drawImage(app.image7,0, 0, width=newWidth,height=newHeight)

def drawEnd(app):
    newWidth, newHeight = (0.37 * app.imageWidth8, 0.37 * app.imageHeight8)
    drawImage(app.image8,0, 0, width=newWidth,height=newHeight)
    drawLabel(app.steps // 20, 0.85 * app.width, 0.72 * app.height,size=50,
              fill='white')
'''
def drawEnd(app):
    drawLabel("Thanks for playing Speed Skier!" , app.width/2, app.height/8)
    drawLabel(f"You survived {app.steps/20} seconds, congrats!",
              app.width/2, 2 * app.height/8)
    drawLabel("Press the r to restart the Game" , 
    app.width/2, 3 * app.height/8)
'''
def drawBackground(app):
        newWidth, newHeight = (app.imageWidth5, app.imageHeight5)
        drawImage(app.image5,0, 0, width=newWidth,height=newHeight)

def drawScore(app):
        newWidth, newHeight = (app.imageWidth6/3, app.imageHeight6/3)
        drawImage(app.image6,4*app.width/6, 0, width=newWidth,
                  height=newHeight)
        drawLabel(app.lives, .92 * app.width, 45)
        drawLabel(app.steps // 20, .85 * app.width, 60)

def getImages(app):
    #Citation:https://pillow.readthedocs.io/en/stable/reference/Image.html 
    app.image = Image.open("images/testSkier.jpg")
    def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))
    
    #Citation: https://www.istockphoto.com/vector/athlete-skier-super-slalom-gm
    # 899914160-248312797
    app.image = openImage("images/testSkier.jpg")
    app.imageWidth,app.imageHeight = app.image.width,app.image.height
    app.image = CMUImage(app.image)

    #Citation : https://www.freeimages.com/premium-clipart/giant-slalom-ski-rac
    # er-silhouette-vector-illustration-4967187?ref=clipartlogo
    app.image1 = Image.open("images/gateImage.jpg")
    app.image1 = openImage("images/gateImage.jpg")
    app.imageWidth1,app.imageHeight1 = app.image1.width,app.image1.height
    app.image1 = CMUImage(app.image1)

    #Citation: https://pearlyarts.com/product/ghost-clipart-1/
    app.image2 = Image.open("images/ghostImage.png")
    app.image2 = openImage("images/ghostImage.png")
    app.imageWidth2,app.imageHeight2 = app.image2.width,app.image2.height
    app.image2 = CMUImage(app.image2)

    #Citation: https://www.stickpng.com/img/miscellaneous/snowballs/blue-rimmed
    # -snowball-clipart
    app.image3 = Image.open("images/snow.png")
    app.image3 = openImage("images/snow.png")
    app.imageWidth3,app.imageHeight3 = app.image3.width,app.image3.height
    app.image3 = CMUImage(app.image3)

    #Citation: https://pngtree.com/free-star-clipart
    app.image4 = Image.open("images/star.png")
    app.image4 = openImage("images/star.png")
    app.imageWidth4,app.imageHeight4 = app.image4.width,app.image4.height
    app.image4 = CMUImage(app.image4)

    #Citation: https://www.istockphoto.com/illustrations/ski-background
    app.image5 = Image.open("images/background.jpg")
    app.image5 = openImage("images/background.jpg")
    app.imageWidth5,app.imageHeight5 = app.image5.width,app.image5.height
    app.image5 = CMUImage(app.image5)

    #Citation: https://www.canva.com/design/DAFrKysbvfQ/ZGj2w4u4frKepa8NZ-JFdg/
    # edit?utm_content=DAFrKysbvfQ&utm_campaign=designshare&utm_medium=link2&utm
    # _source=sharebutton
    #I created this by myself in canva
    app.image6 = Image.open("images/score.png")
    app.image6 = openImage("images/score.png")
    app.imageWidth6,app.imageHeight6 = app.image6.width,app.image6.height
    app.image6 = CMUImage(app.image6)

    #Citation: https://www.canva.com/design/DAFrK6uWtSE/RKWP83rHqTptja1VXHpfQQ/
    # edit?utm_content=DAFrK6uWtSE&utm_campaign=designshare&utm_medium=link2&utm
    # _source=sharebutton
    app.image7 = Image.open("images/starterPage.png")
    app.image7 = openImage("images/starterPage.png")
    app.imageWidth7,app.imageHeight7 = app.image7.width,app.image7.height
    app.image7 = CMUImage(app.image7)

    #Citation: https://www.canva.com/design/DAFrLALGOvc/kNREVF_LF87MzFdo1UP9QQ/
    # edit?utm_content=DAFrLALGOvc&utm_campaign=designshare&utm_medium=link2&utm
    # _source=sharebutton
    app.image8 = Image.open("images/gameEnd.png")
    app.image8 = openImage("images/gameEnd.png")
    app.imageWidth8,app.imageHeight8 = app.image8.width,app.image8.height
    app.image8 = CMUImage(app.image8)

def main():
    runApp()

main()

