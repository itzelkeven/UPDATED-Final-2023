import random
import pygame
import time
pygame.init()  
pygame.display.set_caption("Jumper!")

WIDTH = 800
HEIGHT = 800



screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
screen.fill((0,0,0))
clock = pygame.time.Clock()
gameover = False

bear = pygame.image.load('bear spritesheet.png')
bear.set_colorkey((255,0,255))
timer = 0


LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

#platform position
pxpos = -10
pypos = -10
#player position $ variables
bxpos = 300
bypos = 350
offset = 0
alive = True
#velocity of player
bx = 0
by = 0
keys = [False, False, False, False]
grounded = False

#animation
frameW = 120
frameH = 120
frameNum = 0
RowNum = 0
tick = 0
direction = DOWN
moving = False
platform_list = [(0,HEIGHT-40,WIDTH,40),(WIDTH/2-25,HEIGHT*3/4,100,20),(125,HEIGHT-350,100,20),(WIDTH/2-50,HEIGHT*1/2,100,20),
                (WIDTH/2-50,HEIGHT*1/4,100,20), (WIDTH/2-10, HEIGHT*1/4, 200, 20)]
for event in pygame.event.get():
     if event.type == pygame.QUIT:
         gameover = True

class platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((w,h))
        self.image.fill((0,255,0))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class pads:
    def __init__(self):
        self.platform_sprite = pygame.sprite.Group()
        for plat in platform_list:
            p = platform(*plat)
            self.platform_sprite.add(p)
    def spawn_new(self):
        while len(self.platform_sprite)<6:
            width = random.randrange(400,600)
            p = platform(random.randange(0,WIDTH-width), random.randrange(-50, -30),width,20)
            self.platform_sprite.add(p)
        while len(self.platform_sprite)<9:
            width = random.randrange(400,600)
            p = platform(random.randrange(0,WIDTH-width),
                         random.randrange(-75,-30),
                         width,30)
            self.platform_sprite.add(p)

    def collision(self, x, y, vy):
        for plat in self.platform_sprite:
            if y + frameH <= plat.rect.top:
                vy = 0
                grounded = True
              
                print("collide")

    def draw(self):
        self.platform_sprite.draw(screen)# *after* drawing everything, flip the display

    def scroll_y(self, xpos, ypos, vx, vy):
        if ypos <= HEIGHT/4:
            ypos += abs(vy)
            for plat in self.platform_sprite:
                plat.rect.y += abs(vy)
                if plat.rect.top>=HEIGHT:
                    plat.kill()#kills platforms when we go up


                    


    def update(self,xpos,ypos,vx,vy):
        self.draw()
        self.collision(xpos,ypos, vy)
        self.scroll_y(xpos,ypos,vx,vy)
        self.spawn_new()
   




pad = pads()


while gameover == False:
    clock.tick(60)
    timer += 1
    #Movement
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
      
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT] = True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = True
        if event.type == pygame.KEYDOWN and grounded == True:
            if event.key == pygame.K_UP:
                keys[UP] = True


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT] = False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = False
            elif event.key == pygame.K_UP:
                keys[UP] = False

    #Gravity
    if grounded == False:
        by += 1.1
       
    if bypos > 800-frameH:
        grounded = True
        by = 0
        bypos = 800-frameH
   
   
     #LEFT MOVEMENT
    if keys[LEFT] == True:
        if bxpos > 400:
            bx = -3
        elif offset < 0:
            offset+=3
            bx = 0
        else:
            bx = -3
        RowNum = 0
        direction = LEFT
        moving = True
        
    #RIGHT MOVEMENT
    elif keys[RIGHT] == True:
        if bxpos < 400:
            bx = 3
        elif offset > -800:
            offset-=3
            bx = 0
        else:
            bx = 3
        RowNum = 1
        direction = RIGHT
        moving = True

    else:
        bx = 0
        moving = False

    if keys[UP] == True and grounded == True: #only jump when on the ground
        by = -8
        RowNum = 2
        grounded = False
        direction = UP
        moving = True
    
    elif keys[UP] ==True:
        by = -12
        RowNum = 2
        grounded = False
        direction = UP


    if bx < 0: #Left
        RowNum = 1
        tick+=1
        if tick%10==0:
            frameNum+=1
        if frameNum>3:
            frameNum = 0

    if bx > 0: #Right
        RowNum = 1
        tick+=1
        if tick%10==0:
            frameNum+=1
        if frameNum>3:
            frameNum = 0

    if by < 0: #down
        RowNum = 2
        tick+=1
        if tick%10==0: 
          frameNum+=1
        if frameNum>1: 
           frameNum = 0

    if by > 0: #up
        RowNum = 2
        tick+=1
        if tick%10==0: 
          frameNum+=1
        if frameNum>1: 
          frameNum = 0

    bxpos += bx
    bypos += by

    screen.fill((0,0,0))
    #turn off velocity
    

    pygame.draw.rect(screen, (255, 0, 0),(bxpos, bypos, 50, 50))
    
    screen.blit(bear, (bxpos, bypos), (frameW * frameNum, RowNum * frameH, frameW, frameH))
    

    pad.update(bxpos, bypos,bx,by)
        

    pygame.display.flip()

pygame.quit()


