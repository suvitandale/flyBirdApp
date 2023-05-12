import random # To generate random numbers
import sys  # we'll use sys.exit to exit the program
import pygame
from pygame import *    # basic pygame imports

# Global Variables for the game
FPS = 32    #Frames per seconds # Randering of images in seconds
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))   #Initialings game screen using pygame module by providing screen width and height
GROUNDY = SCREENHEIGHT * 0.8 # Decide base image axis of game over a screen
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreens():
    """
    Show welcome images on screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey =int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            # if user clicks on cross button then quit the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user presses up or space key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getRandomPipe():
    """
    Generate positions of two pipes for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex = SCREENWIDTH+10
    y1 = pipeHeight-y2+offset

    pipe = [
        {'x':pipex,'y': -y1},   #upper pipe
        {'x':pipex,'y': y2}      #lower pipe
    ]
    return pipe



def isColide(playerx,playery,upperpipes,lowerpipes):
    if playery > GROUNDY-25 or playery<0 :
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight+pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery+GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx-pipe['x']) > GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/2)
    playery = int(SCREENHEIGHT/5)
    basex = 0

    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()


    upperpipes = [
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x': SCREENWIDTH +200+(SCREENWIDTH/2),'y': newpipe2[0]['y']}
    ]

    lowerpipes = [
        {'x': SCREENWIDTH + 200, 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH + 200 +(SCREENWIDTH / 2), 'y': newpipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVely = -9
    playerMinVelY = -8
    playerMaxVelY = 10
    playerAccY = 1
    playerFlapAccv = -8 # Velocity while bird flapping
    playerFlaped = False # It is true only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                # if user presses up or space key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
                if playery > 0 :
                    playerVely = playerFlapAccv
                    playerFlaped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = isColide(playerx,playery,upperpipes,lowerpipes) # This fun will return True if you are crashed
        if crashtest:
            return

        #check for score
        playerMidPos = playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score+=1
                print('your score is {score}',score)
                GAME_SOUNDS['point'].play()

            elif playerVely < playerMaxVelY and not playerFlaped:
                playerVely += playerAccY

            if playerFlaped:
                playerFlaped = False

            playerHeight = GAME_SPRITES['player'].get_height()
            playery = playery + min(playerVely, GROUNDY-playery-playerHeight)

            # move pipe to the left
            for upperpipe, lowerpipe in zip(upperpipes,lowerpipes):
                upperpipe['x'] += pipeVelX
                lowerpipe['x'] += pipeVelX

            # add new pipe to add when old pipe is about to cross
            if 0<upperpipes[0]['x']<5:
                newpipe = getRandomPipe()
                upperpipes.append(newpipe[0])
                lowerpipes.append(newpipe[1])

            # if pipe is out of the screen then remove it
            if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                upperpipes.pop()
                lowerpipes.pop()

            #now blit our sprites
            SCREEN.blit(GAME_SPRITES['background'],(0,0))
            for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))

            SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digits in myDigits:
                width += GAME_SPRITES['numbers'][digits].get_width()
            xoffset = (SCREENWIDTH - width)/2

            for digits in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digits],(xoffset, SCREENHEIGHT*0.12))
                xoffset+=GAME_SPRITES['numbers'][digits].get_width()

            pygame.display.update()
            FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    # This will be the main point from where our game will start
    pygame.init()   # initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()  # It will control our game FPS
    pygame.display.set_caption('FlappyBird by Suvidha')
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(), #convert_alpha() makes your image to get optimized for game
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['message'] = (pygame.image.load('gallery/sprites/harry.png').convert_alpha())
    GAME_SPRITES['base'] = (pygame.image.load('gallery/sprites/base.png').convert_alpha())
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha())
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreens()  #shows welcome screen to user until it presses any button
        mainGame()
