#Create your own shooter

import pygame
import random
pygame.init()

wsc = 400
hsc = 400
n = "kapallaut"

bg = "sea (2).png"
p = "ship (1).png"
e = "ship (2).png"
o = "Bomb.png"
cb = "cannonBall.png"
sShot = "fire.ogg"
sBg = "At Launch.mp3"
relod = 0.1
jumlahS = 0
sc = 0
ms = 0
gameRUN = True
gameEND = False

scene = pygame.display.set_mode((wsc, hsc))
scene.fill((0,0,0))
pygame.display.set_caption(n)
belakang = pygame.transform.scale(pygame.image.load(bg), (wsc, hsc))
fps = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load(sBg)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

bum = pygame.mixer.Sound(sShot)

pygame.font.init()
font1 = pygame.font.SysFont("comic mono", 25)
font2 = pygame.font.SysFont("comic mono", 50)
tulisan_score = font1.render("SCORE:"+str(sc), True, (0,0,0))
tulisan_missed = font1.render("MISSED:"+str(ms), True, (0,0,0))


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y, Wi, He, spd):
        super().__init__()
        self.Wi = Wi
        self.He = He
        self.img = pygame.transform.scale(pygame.image.load(img), (self.Wi, self.He))
        self.spd = spd
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        scene.blit(self.img, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        btn = pygame.key.get_pressed()
        if btn[pygame.K_a] and self.rect.x>0:
            self.rect.x -= self.spd
        elif btn[pygame.K_d] and self.rect.x<wsc-self.Wi:
            self.rect.x += self.spd
    def shot(self):
        global jumlahS
        jumlahS += 1
        B = Bullet(img=cb, x=self.rect.centerx, y=self.rect.top, Wi=12, He=12, spd=5)
        grupB.add(B)

class Enemy(GameSprite):
    def fw(self):
        self.rect.y += self.spd
        global ms
        if self.rect.y > hsc:
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(50, wsc-100)
            ms += 1

class Bullet(GameSprite):
    def peciuw(self):
        self.rect.y -= self.spd
        if self.rect.y < -100:
            self.kill()

class Obstacle(GameSprite):
    def fw(self):
        self.rect.y += self.spd
        if self.rect.y > hsc:
            self.rect.y = random.randint(-300, -100)
            self.rect.x = random.randint(50, wsc-100)


PL = Player(img=p, x=185, y=340, Wi=30, He=50, spd=10)

grupE = pygame.sprite.Group()
jumlahE = 5
for jumlah in range(jumlahE):
    E = Enemy(img=e, x=random.randint(50, wsc-100), y=random.randint(-300, -100), Wi=30, He=50, spd=2)
    grupE.add(E)

grupO = pygame.sprite.Group()
jumlahO = 3
for jumlah in range(jumlahO):
    O = Obstacle(img=o, x=random.randint(50, wsc-100), y=random.randint(-300, -100), Wi=35, He=35, spd=2)
    grupO.add(O)

grupB = pygame.sprite.Group()


while gameRUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRUN = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jumlahS >= 1 and relod >= 0:
                    relod -= 0.1 
                elif jumlahS >= 0 and relod <= 0:
                    jumlahS = 0
                    relod = 0.1
                elif jumlahS <= 1 and relod >= 0.1:
                    bum.play()
                    PL.shot()

    if gameEND == False:
        scene.blit(belakang, (0,0))
        tulisan_score = font1.render("SCORE:"+str(sc), True, (0,0,0))
        tulisan_missed = font1.render("MISSED:"+str(ms), True, (0,0,0))
        win = font2.render("Kamu Menang", True, (0,204,102))
        lus = font2.render("Coba Lagi", True, (230, 0, 76))

        scene.blit(tulisan_score, (10, 305))
        scene.blit(tulisan_missed, (10, 325))

        PL.show()
        PL.move()
        for E in grupE:
            E.show()
            E.fw()
        for B in grupB:
            B.show()
            B.peciuw()
        for O in grupO:
            O.show()
            O.fw()
        
        if ms >= 50 :
            scene.blit(lus, (120, 180))
            gameEND = True
        if sc >= 15:
            scene.blit(win, (80, 180))
            gameEND = True

        if pygame.sprite.spritecollide(PL, grupE, True):
            sc -= 1
            E = Enemy(img=e, x=random.randint(50, wsc-100), y=random.randint(-300, -100), Wi=30, He=50, spd=2)
            grupE.add(E)
        if pygame.sprite.spritecollide(PL, grupO, True):
            sc -= 2
            O = Obstacle(img=o, x=random.randint(50, wsc-100), y=random.randint(-300, -100), Wi=35, He=35, spd=2)
            grupO.add(O)
        if pygame.sprite.groupcollide(grupB, grupE, True, True):
            sc += 1
            E = Enemy(img=e, x=random.randint(50, wsc-100), y=random.randint(-300, -100), Wi=30, He=50, spd=2)
            grupE.add(E)
        if pygame.sprite.groupcollide(grupB, grupO, True, False):
            pass

    fps.tick(60)
    pygame.display.update()