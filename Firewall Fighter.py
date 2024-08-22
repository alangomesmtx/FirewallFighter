import sys
import pygame
from pygame.constants import K_DOWN, K_ESCAPE, K_SPACE, KEYDOWN, KEYUP 
from pygame.constants import QUIT
import random
import math
from pygame import mixer


#Initialize the pygame
pygame.init()

#Image Paths
icon=pygame.image.load('Python/Games/gallery/images/ball32.png')
backgroundimg1 =pygame.image.load('Python/Games/gallery/images/background1.png')
backgroundimg2 =pygame.image.load('Python/Games/gallery/images/background2.png')
floorimg = pygame.image.load('Python/Games/gallery/images/floor.jpg')
ceilingimg = pygame.transform.rotate(floorimg, 180)
messageimg = pygame.image.load('Python/Games/gallery/images/message.png')
empimg = pygame.image.load('Python/Games/gallery/images/emp32.png')
gameovermessageimg=pygame.image.load('Python/Games/gallery/images/gameovermessage.png')
lineimg=pygame.image.load('Python/Games/gallery/images/line.png')
GAME_SPRITES={}
GAME_SPRITES['numbers'] = ( 
        pygame.image.load('Python/Games/gallery/images/0.png'),
        pygame.image.load('Python/Games/gallery/images/1.png'),
        pygame.image.load('Python/Games/gallery/images/2.png'),
        pygame.image.load('Python/Games/gallery/images/3.png'),
        pygame.image.load('Python/Games/gallery/images/4.png'),
        pygame.image.load('Python/Games/gallery/images/5.png'),
        pygame.image.load('Python/Games/gallery/images/6.png'),
        pygame.image.load('Python/Games/gallery/images/7.png'),
        pygame.image.load('Python/Games/gallery/images/8.png'),
        pygame.image.load('Python/Games/gallery/images/9.png'),
)

#Background Music
mixer.music.load('Python/Games/gallery/sounds/background.wav')
mixer.music.play(-1)

#Creating a Screen
screenwidth=1080
screenheight=720
screen=pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Firewall Fighter")
pygame.display.set_icon(icon)

#Image Positions
messagex = int((screenwidth - messageimg.get_width())/2)
messagey = 50
floorx = 0
floory = 570
ceilingx = 0
ceilingy = 0

#Player
ballimg=pygame.image.load('Python/Games/gallery/images/ball48.png')
ballx = int((screenwidth - ballimg.get_width())/2)
bally = int((screenheight - ballimg.get_height())*(4/5))

def ball(ballx, bally):
    screen.blit(ballimg, (ballx, bally))

#Enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemymovx=[]
enemymovy=[]
numofenemies=10

for i in range(numofenemies):
    enemyimg.append(pygame.image.load('Python/Games/gallery/images/hacker-codes.png'))
    enemyx.append(random.randint(0, (1080-64)))
    enemyy.append(random.randint(0, (400-64)))
    enemymovx.append(5)
    enemymovy.append(70)


def enemy(enemyx, enemyy, i):
    screen.blit(enemyimg[i], (enemyx[i], enemyy[i]))

#EMP
empimg=pygame.image.load('Python/Games/gallery/images/emp32.png')
empx=ballx+((ballimg.get_width())/2)
empy=600
empmovx=0
empmovy=50
empstate="ready"

def launchemp(empx, empy):
    global empstate
    empstate="launch"
    screen.blit(empimg, (empx, empy))


def iscollision(enemyx, enemyy, empx, empy):
    distance = math.sqrt((math.pow(enemyx-empx, 2)) + (math.pow(enemyy-empy, 2)))
    if distance<64:
        return True
    else:
        return False



def welcomescreen():

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return
            else:
                screen.blit(backgroundimg1, (0, 0))
                ball(ballx, bally)
                screen.blit(floorimg, (floorx, floory))
                screen.blit(ceilingimg, (ceilingx, ceilingy))
                screen.blit(messageimg, (messagex, messagey))
                pygame.display.update() 

def maingame():
    
    global ballx
    global bally
    global empstate
    global empx
    global enemyx
    global enemyy
    ceilingy=0
    floory=570
    messagey=50
    ballmovx=0
    ballmovy=0 
    empy=600
    empmovy=20
    score=0
    backgroundimg1x=0
    backgroundimg1y=0
    backgroundimg2x=0
    backgroundimg2y=-640
    gameover=False
    gameovermessagey=-500
    collisionsound=mixer.Sound('Python/Games/gallery/sounds/explosion.wav')

    while True:

        screen.blit(backgroundimg1, (backgroundimg1x, backgroundimg1y))
        screen.blit(backgroundimg2, (backgroundimg2x, backgroundimg2y))
        backgroundimg1y+=0.5
        backgroundimg2y+=0.5
        if backgroundimg1y>=640:
            backgroundimg1y=-640
        if backgroundimg2y>=640:
            backgroundimg2y=-640

        for event in pygame.event.get():
            if event.type==QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    ballmovx=-6
                if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    ballmovx=6
                if event.key==pygame.K_SPACE:
                    if empstate is "ready":
                        empsound=mixer.Sound('Python/Games/gallery/sounds/laser.wav')
                        empsound.play()
                        empx=ballx+8
                        launchemp(empx, empy)
                        pygame.display.update() 
            if event.type==KEYUP:
                ballmovx=0
                ballmovy=0
                if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                    continue
                if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                    continue

        ceilingy-=12
        floory+=4
        messagey-=9
        if ceilingy==-600:
            ceilingy=-600
        if floory==750:
            floory=750
        if messagey==-600:
            messagey=-600

        #Ball Movement

        ballx+=ballmovx
        bally+=ballmovy


        if 0>=ballx:
            ballx=0
        if ballx>(1080-ballimg.get_width()):
            ballx=(1080-ballimg.get_width())
        if 0>=bally:
            bally=0
        if bally>(720-ballimg.get_height()):
            bally=(720-ballimg.get_height())

        #EMP Movement
        if empy<=0:
            empy=int(bally)
            empstate="ready"
        if empstate is "launch":
            launchemp(empx, empy)
            empy-=empmovy

        #Enemy Movement

        for i in range(numofenemies):
            enemyx[i]+=enemymovx[i]

            if 0>=enemyx[i]:
                enemymovx[i]=5
                enemyy[i]+=enemymovy[i]
            if enemyx[i]>(1080-64):
                enemymovx[i]=-5
                enemyy[i]+=enemymovy[i]
            if enemyy[i]>=600:
                enemyy[i]=random.randint(0, (400-64))

            #Collision
            collision=iscollision(enemyx[i], enemyy[i], empx, empy)
            if collision:
                collisionsound.play()
                empy=600
                empstate="ready"
                score+=1
                print("Your Score:",score)
                enemyx[i] = random.randint(0, (1080-64))
                enemyy[i] = random.randint(0, (400-64))
            if enemyy[i]>=int(250+((lineimg.get_height())/2)-64):
                gameover=True
            
            enemy(enemyx, enemyy, i)
        
        if gameover:
            gameoversound=mixer.Sound('Python/Games/gallery/sounds/gameover.wav')
            gameoversound.play()
            gameovermessagey=50
            ceilingy=0
            floory=570
            collisionsound=mixer.Sound('Python/Games/gallery/sounds/silence.wav')           
         
        
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (1080 - width)/2

        for digit in myDigits:
            screen.blit(GAME_SPRITES['numbers'][digit], (Xoffset, 720*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        #Props
        ball(ballx, bally)
        screen.blit(lineimg, (0, 250))
        screen.blit(floorimg, (floorx, floory))
        screen.blit(ceilingimg, (ceilingx, ceilingy))
        screen.blit(messageimg, (messagex, messagey))
        screen.blit(gameovermessageimg, (messagex, gameovermessagey))

        pygame.display.update()

while True:
    welcomescreen()
    maingame() 