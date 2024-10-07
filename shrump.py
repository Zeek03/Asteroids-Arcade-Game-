import pygame
import random
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60
 
# defining color for the game
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CYAN = (0,255,255)
YELLOW = (255,255,0)

img_dir = path.join(path.dirname(__file__),'shrump_assets')
snd_dir = path.join(path.dirname(__file__),'shump_sounds')

font_name = pygame.font.match_font('ariel')
def draw_text(surface,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render('SCORE '+text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

# Drawing shield for the player
def draw_shield(surf,text,x,y,percent):
    if percent < 0:
        percent = 0
    bar_len = 100
    bar_height = 10
    fill = (percent / 100) * bar_len
    out_rect = pygame.Rect(x,y,bar_len,bar_height)
    fill_rect = pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE,out_rect,3)

    font = pygame.font.Font(font_name, 20)
    text_surface = font.render('SHIELD'.format(text), True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (40, 10)
    surf.blit(text_surface, text_rect)

# Defining new mob function
def newmob():
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

class Player(pygame.sprite.Sprite):
    # creating sprites for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        #self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10
        self.speedx = 0
        self.shield = 100
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
    def update(self):
        self.speedx  = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7
        if keystate[pygame.K_UP]:
            self.speedy = -7
        if keystate[pygame.K_DOWN]:
            self.speedy = 7
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > 250:
            self.last_shoot = now
            bullet = Bullets(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_snd.play()
        
# Creating sprites for the enemies

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.85 /2)
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-120,-90)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now 
            self.rot = (self.rot + self.rot_speed ) % 360
            new_image = pygame.transform.rotate(self.image_orig,self.rot)
            old_center = self.rect.center
            self.image = new_image  
            self.rect = self.image.get_rect()
            self.rect.center = old_center     
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT +10 or self.rect.left < -15 or self.rect.right > WIDTH + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)
 # Creating sprites for the meteiors
'''
class Meteiors(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(WIDTH * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100 , -40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3 ,3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange9(-100,-40)
            self.speedy = random.randrange(1,8) 
   '''     
# Creating sprites for the bullets

class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy

        # kills if bullets moves the top of the screen 
        if self.rect.bottom < 0:
            self.kill() # kill command terminates the sprite 
# initializing the pygame and set game window

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shrump!")
Clock = pygame.time.Clock()

# Load all game graphics

background = pygame.image.load(path.join(img_dir,"blue.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"playerShip2_blue.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir,"meteorBrown_small1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir,"laserRed01.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_med1.png',
               'meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_small2.png',
               'meteorBrown_tiny1.png','meteorBrown_tiny2.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

shoot_snd = pygame.mixer.Sound(path.join(snd_dir,'shoot.wav'))
explode_snd = pygame.mixer.Sound(path.join(snd_dir,'explode.wav'))
gameover_snd = pygame.mixer.Sound(path.join(snd_dir,'gameover.wav')) 
pygame.mixer.music.load(path.join(snd_dir,'backgrnd_snd.ogg'))
pygame.mixer.music.set_volume(0.4)



all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
#meteors = pygame.sprite.Group()
player = Player()
enemy = Enemy()
#mete = Meteiors()
all_sprites.add(player)
for i in range(8):
    newmob()

score = 0
'''for i in range(8):
    m = Meteiors()
    all_sprites.add(m)
    mete.add(m)'''
pygame.mixer.music.play(loops= -1)
# creating game loop
running = True
while running: 
    Clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
                           

    # update the game 
    all_sprites.update()

    # Check to see if a bullet hits a mob then kill the mob
     
    hits = pygame.sprite.groupcollide(enemies,bullets,True,True)
    for hit in hits:
        score += 50 - hit.radius
        explode_snd.play()
        newmob()

    # check to see if a mob hits the player

    hits = pygame.sprite.spritecollide(player,enemies,True,pygame.sprite.collide_circle)
    
    for hit in hits:
        player.shield -= hit.radius * 2
        if player.shield <= 0:
            gameover_snd.play()
            pygame.time.delay(2000)
            running = False
        
    pygame.display.flip()
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),20, WIDTH/2,10)
    #draw_text(screen,"GAME OVER ",40,WIDTH/2,HEIGHT/2)
    #draw_text(screen,"PRESS SPACE TO RESTART THE GAME",20,WIDTH/2,HEIGHT*3/4)
    draw_shield(screen,player.shield,70,10,player.shield)
    pygame.display.flip()
pygame.quit()    