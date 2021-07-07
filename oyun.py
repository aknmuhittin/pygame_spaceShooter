import pygame,sys,os,random
pygame.init()


width=800
height=600

size=(width,height)
window=pygame.display.set_mode(size)


klasor=os.path.dirname(__file__)
imageKlosor=os.path.join(klasor,"images")
voiceKlosor=os.path.join(klasor,"voices")

background=pygame.image.load(os.path.join(imageKlosor,"black.png"))
fire=pygame.image.load(os.path.join(imageKlosor,"fire.png"))
player=pygame.image.load(os.path.join(imageKlosor,"player.png"))


hitEffect=pygame.mixer.Sound(os.path.join(voiceKlosor,"hit.mp3"))
laser=pygame.mixer.Sound(os.path.join(voiceKlosor,"laser.ogg"))
explode=pygame.mixer.Sound(os.path.join(voiceKlosor,"exp.mp3"))


clock=pygame.time.Clock()

font=pygame.font.SysFont("Helvetica",50)
score=0
allienSpaces=["enemy.png","enemy.png","enemy.png","enemy.png","health.png","health.png"]


all_sprites=pygame.sprite.Group()


class Parca(pygame.sprite.Sprite):
    def __init__(self,x=width/2,y=height/2):
        super().__init__()
        self.image=player.convert()
        #self.image.fill((0,255,0))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=y
        self.health=3

    
    
    def update(self,*args):
        up,down,right,left=args
        if self.rect.y<0:
            self.rect.y=0
        if self.rect.y+self.rect.size[1]>height:
            self.rect.y=height-self.rect.size[1]
        if up:
            self.rect.y+=-10
        if down:
            self.rect.y+=10
      
    def shoot(self):
        laser.play()
        fuze=Fuze(self.rect.y)
        all_sprites.add(fuze) 
        fuzeler.add(fuze) 



class Mermi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.secim=random.choice(allienSpaces)
        allienSpace=pygame.image.load(os.path.join(imageKlosor,self.secim)) 
        
        self.image=allienSpace.convert()
        self.image.set_colorkey((255,255,255))
        #self.image.fill((255,0,0))
        self.rect=self.image.get_rect()

        self.rect.y=random.randrange(height-self.rect.height)
        self.rect.x=random.randrange(width+30,width+100)
        
        self.speedx=random.randrange(5,18)
        self.speedy=random.randrange(-1,1)
    def update(self,*args):
        self.rect.x-=self.speedx
        self.rect.y+=self.speedy

        if self.rect.right<0:
            self.rect.y=random.randrange(height-self.rect.height)
            self.rect.x=random.randrange(width+30,width+100)

            self.speedx=random.randrange(5,18)
            self.speedy=random.randrange(-1,1)
          
class Fuze (pygame.sprite.Sprite):
    def __init__(self,parcaY) :
        super().__init__()
        self.image=fire.convert()
        self.image.set_colorkey((255,255,255))

        #self.image.fill((0,255,0))
        self.rect=self.image.get_rect()
        self.rect.x=30
        self.rect.y=parcaY+20
    def update(self,*args):
        self.rect.x+=8

        if self.rect.left>width:
            self.kill()


all_sprites=pygame.sprite.Group()
mermiler=pygame.sprite.Group()
fuzeler=pygame.sprite.Group()
for i in range(8):
    mermi=Mermi()
    all_sprites.add(mermi)
    mermiler.add(mermi)

    
    
  

        



parca1=Parca()

all_sprites.add(parca1)


        

while True:
    window.fill((0,0,0))
    window.blit(background,background.get_rect())
    clock.tick(60)
    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                parca1.shoot()
 

    
    up,down,right,left=keys[pygame.K_UP],keys[pygame.K_DOWN],keys[pygame.K_RIGHT],keys[pygame.K_LEFT]
    all_sprites.update(up,down,right,left)
    
    all_sprites.draw(window)
    fontScore=font.render("Skor : {}".format(score),1,(120,60,0))
    window.blit(fontScore,(width-fontScore.get_size()[0],height-fontScore.get_size()[1]))
    
    
    durum= pygame.sprite.spritecollide(parca1,mermiler,True)
    
    isHit=pygame.sprite.groupcollide(fuzeler,mermiler,True,True)
    if isHit:
        pygame.mixer.music.load(os.path.join(voiceKlosor,"hit.mp3"))
        pygame.mixer.music.play()
        for enemies in isHit.values():
            for enemie in enemies:
               if enemie.secim=="health.png":
                   if parca1.health+1<4:
                       parca1.health+=1
                   else:
                       parca1.health=3

                   
                   
        for enemies in isHit.values():
            for enemie in enemies:
               if enemie.secim=="health.png"or"enemy.png":
                  score+=1
                   
                  

        
   
           
                
      
        
    
    
    if durum:
        for enemie in durum:
             parca1.health-=1
            
    fontHealth=font.render("kalan can : {}".format(parca1.health),1,(120,60,0))
    window.blit(fontHealth,(0,0))
    
          
    if parca1.health<=0:
        pygame.mixer.music.load(os.path.join(voiceKlosor,"exp.mp3"))
        pygame.mixer.music.play()
        
        window.fill((0,0,0))
        window.blit(pygame.font.SysFont("Helvetica", 60).render("GAME OVER",1,(255,0,0)),(250,200))
        fontScore=font.render("Skor : {}".format(score),1,(120,60,0))
        window.blit(fontScore,(width-fontScore.get_size()[0],height-fontScore.get_size()[1]))

        
        pygame.display.update()
        pygame.time.wait(1000)
        
        pygame.mixer.music.stop()
    
    pygame.display.update()
    




