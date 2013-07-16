"""
 Author Name: Justin Hellsten
 Last Modified by: Justin Hellsten
 Last Modified Date: July 15 2013
 
 Program Description: A side scroller game for assignment 4 Intro to Graphics.
 
 Revision History: 0.1.0
 
    -> Added Missile Counter (Collectable Item)
    -> Added bouncer missile item on screen every now and then
    -> Added missile counter check in update
    -> Added life counter check in update
    
"""

""" Import and Initialize """
import pygame, utility, sys, random, resource
from resource import *


pygame.init()
utility.init()
resource.init()

""" Read configuration file """
utility.set_config_file(CONFIG_DIRECTORY)
    
width = int(utility.get_config_value('width', 800))
height = int(utility.get_config_value('height', 600))
title = utility.get_config_value('title', 'War Thunder by Justin Hellsten')
depth = int(utility.get_config_value('depth', 32))
mode = int(utility.get_config_value('mode', 0))

if not pygame.display.get_init():
    print 'Could not initialize display screen'
    sys.exit()

#Check if depth is okay for display mode
depth = pygame.display.mode_ok((width, height), mode, depth)  
    
# Create our screen window
screen = pygame.display.set_mode((width, height), mode, depth)    
pygame.display.set_caption(title)
    
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


""" Explosion """
class Explosion(pygame.sprite.Sprite):

    STANDING = 0
    EXPLODING = 1
        
    def __init__(self, center, dx):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.frame = 0
        self.pause = 0
        self.delay = 0
        self.state = Explosion.STANDING
        self.dx = dx
        
        self.imageStand = GfxResource.explosion[len(GfxResource.explosion)-1]
        self.image = self.imageStand
        
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.center = center
         
    def update(self):
        
        # Make sure to move explosion base on center and delta x
        self.center = (self.center[0] + self.dx, self.center[1])
        
        # Check up on the explosion animation
        if self.state == Explosion.STANDING:
            self.image = self.imageStand
        else:
            self.pause += 1
            if self.pause > self.delay:
                #reset pause and advance animation
                self.pause = 0
                self.frame += 1
                if self.frame >= len(GfxResource.explosion):
                    self.frame = 0
                    self.state = Explosion.STANDING
                    self.image = self.imageStand
                    self.kill()
                else:
                    self.image = GfxResource.explosion[self.frame]
                 
        self.rect = self.image.get_rect()
        self.rect.center = self.center
                
        
""" Enemy Classes """ 
class RandomEnemy(pygame.sprite.Sprite):
    
    HIT_POINTS = 30
    
    MAX_SPEED = 10
    MIN_SPEED = 5
    
    def __init__(self, screen, player):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.player = player
        self.bullets = []
        
        self.image = GfxResource.re
        self.health = RandomEnemy.HIT_POINTS
        
        self.isHit = False
        self.isAttacking = False
        
        self.rect = self.image.get_rect()        
        self.reset()        

        self.sndHit = SfxResource.reHit
        self.sndDeath = SfxResource.reDeath

    def update(self):
        """ 
            AI:
                -> Moves right to left
                -> If gets to left side of screen it resets
                -> Upon reset randomizes its entry into the screen again
                -> Will be killed if destroyed by player
                -> If the player is in the path we shoot at the player
                """
        self.rect.left += self.dx        
        if self.rect.right <= 0:
            self.reset()

        if self.isHit:
            self.image.set_colorkey((25, 12, 255))
            self.isHit = False

            
             
        #Attack the player if he is in plain sight
        if self.player.rect.right < self.rect.left and self.player.rect.top > self.rect.top and self.player.rect.top < self.rect.bottom:            
            self.isAttacking = True
            
    def reset(self):
        #Randomize entry point onto screen
        self.rect.center = (self.screen.get_width()+self.image.get_width()*2, 
                            random.randint(self.image.get_height(),screen.get_height()-self.image.get_height()/2))
        self.dx = random.randrange(-RandomEnemy.MAX_SPEED, -RandomEnemy.MIN_SPEED)
       
"""
class HorizontalLinearEnemy(pygame.sprite.Sprite):
    def __init__(self, screen, player):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load( IMG_DIRECTORY + 'random_enemy.png')
        self.rect = self.image.get_rect()        
        self.dx = -5
        self.reset()
        
    def update(self):
        self.rect.left += self.dx        
        if self.rect.right <= 0:
            self.reset()
            
    def reset(self):
        #Randomize entry point onto screen
        self.rect.center = (self.screen.get_width()+self.image.get_width()*2, 
                            random.randint(self.image.get_height()/2,screen.get_height()-self.image.get_height()/2))
        
"""

"""
class VerticalLinearEnemy(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load( IMG_DIRECTORY + 'random_enemy.png')
        self.rect = self.image.get_rect()        
        self.dy = -5
        self.reset()
        
    def update(self):
        self.rect.left += self.dx        
        if self.rect.right <= 0:
            self.reset()
            
    def reset(self):
        #Randomize entry point onto screen
        self.rect.center = (self.screen.get_width()+self.image.get_width()*2, 
                            random.randint(self.image.get_height()/2,screen.get_height()-self.image.get_height()/2))

"""
                
""" Classes """ 
class Parallax(pygame.sprite.Sprite):    
    def __init__(self, screen, sprite, dx):         
        pygame.sprite.Sprite.__init__(self)        
        self.screen = screen
        self.sprite = sprite
        self.image = pygame.surface.Surface((self.sprite.get_width()*3, self.sprite.get_height()), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.dx = dx
        
        self.image.blit(self.sprite, (0, 0))
        self.image.blit(pygame.transform.flip(self.sprite, True, False), (self.sprite.get_width(), 0))
        self.image.blit(self.sprite, (self.sprite.get_width()*2, 0))

    def update (self):
        self.rect.right += self.dx
        if self.rect.right <= self.screen.get_width():
            self.rect.left = self.screen.get_width() - self.sprite.get_width()
      
class Cloud(pygame.sprite.Sprite):
    def __init__(self, screen, center):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.dx = -6
        self.image = GfxResource.clouds[random.randint(0, 2)]
        self.rect = self.image.get_rect()
        self.rect.center = center

        
    def update(self):
        self.rect.right += self.dx
        if self.rect.right <= 0:
            self.reset()
        
    def reset(self):
        #Randomize vertical location         
        self.rect.center = (self.screen.get_width()+self.image.get_width()*2, 
                            random.randint(-self.image.get_height()/2,screen.get_height()/2-self.image.get_height()/2))


   
class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, image, startx, starty, damage):   
        pygame.sprite.Sprite.__init__(self)  
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (startx, starty)
        self.damage = damage
        
    def update(self):
        if self.rect.left >= screen.get_width():
            self.kill()
                    
class Bullet(Projectile):
    def __init__(self, screen, startx, starty):   
        Projectile.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + 'bullet.png'), startx, starty, 10)
        self.dx = 20
        
    def update(self):
        Projectile.update(self)
        self.rect.left += self.dx
        
class SpecialShot(Projectile):
    def __init__(self, screen, startx, starty):
        Projectile.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + 'missile.png'), startx, starty, 100)
        self.speed = 0.0
        self.dx = 1
        
    def update(self):
        Projectile.update(self)
        self.speed += self.dx
        self.rect.right += self.speed
        
class CollectableMissile(pygame.sprite.Sprite):
    MAX_SPEED = 10
    MIN_SPEED = 5
    
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = GfxResource.collectableMissile
        self.rect = self.image.get_rect()
        self.reset()
        
    def update(self):
        self.rect.left += self.dx
        self.rect.top += self.dy
        if self.rect.top < 0:
            self.rect.top = 0
            self.dy *= -1
        elif self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            self.dy *= -1

        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.dx = -random.randint(CollectableMissile.MIN_SPEED, CollectableMissile.MAX_SPEED)
        self.dy = random.randrange(-1, 1, 2) * random.randint(CollectableMissile.MIN_SPEED / 2, CollectableMissile.MAX_SPEED / 2)
        self.rect.center = (self.screen.get_width()+self.image.get_width()/2, random.randint(0, screen.get_height())) 
        
class MyFont(pygame.sprite.Sprite):
    def __init__(self, text, centerx, centery, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", size)
        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
               
class MissileCounter(pygame.sprite.Sprite):
    def __init__(self, centerx, centery):   
        pygame.sprite.Sprite.__init__(self)    
        self.missiles = 3
        self.center = (centerx, centery)
        self.font = pygame.font.SysFont("None", 24)
        self.noMissiles = False
        self.update()
        
    def update(self):
        self.text = "Missiles: %d" % self.missiles
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
    def removeMissile(self):
        self.missiles -= 1
        if self.missiles <= 0:
            self.missiles = 0
            self.noMissiles = True

    def addMissile(self):
        self.missiles += 1
        self.noMissiles = False
        
class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self, centerx, centery):   
        pygame.sprite.Sprite.__init__(self)    
        self.score = 0
        self.font = pygame.font.SysFont("None", 24)
        self.center = (centerx, centery)
        self.update()
        
    def update(self):
        self.text = "Score: %d" % self.score
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
class LifeCounter(pygame.sprite.Sprite):
    def __init__(self, centerx, centery):   
        pygame.sprite.Sprite.__init__(self)    
        self.lifeImage = pygame.image.load( IMG_DIRECTORY + 'life.png')
        self.lives = 3
        self.isDead = False
        self.center = (centerx, centery)
        self.update()
        
    def update(self):

        self.image = pygame.surface.Surface((self.lifeImage.get_width()*self.lives, self.lifeImage.get_height()), pygame.SRCALPHA)
        for x in range(self.lives):
            self.image.blit(self.lifeImage, (x * self.lifeImage.get_width(), 0))
    
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
    def removeLife(self):
        self.lives -= 1
        #Check if life counter is less than zero. Than set a flag indicating that the player is dead
        if self.lives < 0:
            self.isDead = True
            self.lives = 0
            
class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.screen = screen   
        
        # Set mouse track fields
        self.lastmousey = 0
        self.curmousey = 0

    def update (self):                
        mousex, mousey = pygame.mouse.get_pos()
        
        # Collision check on screen boundaries
        if mousey - self.rect.height / 2 < 0:
            self.rect.centery = self.rect.height / 2
        elif mousex + self.rect.height / 2 > self.screen.get_height():
            self.rect.centery = self.screen.get_height() - self.rect.height / 2
        else:
            self.rect.centery = mousey

        #Set last and current mouse positions
        self.lastmousey = self.curmousey
        self.curmousey = mousey
                      
            
class MiGX3(Ship):
    def __init__(self, screen, centerx, centery):
        Ship.__init__(self, screen, pygame.image.load( IMG_DIRECTORY + "MiG-X3.png" ))
        self.image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)

        self.image.blit(self.spritesheet, (0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (centerx, centery)
        
        if not pygame.mixer:
            print("Cannot Load Sounds")
        else:
            pygame.mixer.init()
            #Make sound a list so we can have multiple weapon bullet shots
            self.sndPrimaryWeapon = pygame.mixer.Sound( SOUND_DIRECTORY + "bullet.ogg")
            self.sndSecondaryWeapon = pygame.mixer.Sound( SOUND_DIRECTORY + "missile.ogg")

    def update(self):
        Ship.update(self)
        
        dmy = self.curmousey - self.lastmousey 
        
        if dmy != 0:
            self.flyVertically() 
        else:
            self.flyStraight()  
               
            
                
    def flyVertically(self):  
        tmp_image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)
        tmp_image.blit(self.spritesheet, (0,0), pygame.rect.Rect((64,0), (64,50)))
        self.image = tmp_image
        
    def flyStraight(self):
        tmp_image = pygame.surface.Surface((64, 50), pygame.SRCALPHA)
        tmp_image.blit(self.spritesheet, (0,0))
        self.image = tmp_image
        
         
    
def startScreen():
    running = True
    
    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #Declare background sprites 
    citySprite = Parallax(screen, pygame.image.load( STAGE_BACKGROUNDS[0][0] ), -5)
    skySprite = Parallax(screen, pygame.image.load( STAGE_BACKGROUNDS[0][1] ), -1)
    cloudSprites =  []
    cloudSprites.append(Cloud(screen, (0, 000)))
    cloudSprites.append(Cloud(screen, (300, 100)))
    cloudSprites.append(Cloud(screen, (600, 200)))
    
    #Declare sprites
    shipSprite = MiGX3(screen, screen.get_width()/2, 0)
        
    mainTitle = MyFont('War Thunder', screen.get_width()/2, 100, 50, (255, 255, 255))
    movementText = MyFont('Move the mouse up/down to move your ship.', screen.get_width()/2*0.45, 200, 22, (225, 225, 225))
    shootBulletText = MyFont('Left mouse click to shoot primary weapon.', screen.get_width()/2*0.45, 250, 22, (225, 225, 225))
    shootSpecialText = MyFont('Right mouse click to shoot secondary weapon (limited)!', screen.get_width()/2*0.55, 300, 22, (225, 225, 225))
    clickAnywhereText = MyFont('Click any key to continue...', screen.get_width()/2, screen.get_height()/2+100, 30, (255, 255, 255))
    
    #Define groups
    backgroundSprites = pygame.sprite.OrderedUpdates(skySprite, cloudSprites, citySprite)
    playerSprites = pygame.sprite.Group(shipSprite)
    fontSprites = pygame.sprite.Group(mainTitle, movementText, shootBulletText, shootSpecialText, clickAnywhereText)
    pwBulletSprites = pygame.sprite.Group()
    swMissileSprites = pygame.sprite.Group()
    
    # Play intro theme
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_DIRECTORY + "intro_theme.ogg")
        pygame.mixer.music.play(-1)
            
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                toContinue = False
            if event.type == pygame.KEYDOWN:
                toContinue = True
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseState = pygame.mouse.get_pressed()
                if mouseState[0]: #Shoot primary weapon
                    shipSprite.sndPrimaryWeapon.stop()
                    shipSprite.sndPrimaryWeapon.play()
                    pwBulletSprites.add(Bullet(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
                            
                if mouseState[2]: #Shoot secondary weapon
                    shipSprite.sndSecondaryWeapon.stop()
                    shipSprite.sndSecondaryWeapon.play()    
                    swMissileSprites.add(SpecialShot(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
        
        backgroundSprites.update()
        playerSprites.update()
        fontSprites.update()
        pwBulletSprites.update()
        swMissileSprites.update()
        
        backgroundSprites.draw(screen)
        pwBulletSprites.draw(screen)
        swMissileSprites.draw(screen)
        playerSprites.draw(screen)
        fontSprites.draw(screen)
        
        
        pygame.display.flip()
        
    return toContinue


def setupStageOne(randomEnemies,player):
    # Add 20 random enemy sprites
    for i in range(20):
        randomEnemies.add(RandomEnemy(screen, player))
        
    return randomEnemies

"""
def updateStageOne(randomEnemySprites, linearHorizontalEnemySprites):
    numOfRandomEnemySprites = 100
    numOfLinearEnemySprites = 50
    
    return randomEnemySprites, numOfLinearEnemySprites
"""
    
def gamePlayScreen():
    running = True
    keepPlaying = True
    countRandomEnemies = 20
    
    currentStage = 1
    
    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    #Declare background sprites 
    citySprite = Parallax(screen, pygame.image.load( STAGE_BACKGROUNDS[currentStage-1][0] ), -5)
    skySprite = Parallax(screen, pygame.image.load( STAGE_BACKGROUNDS[currentStage-1][1] ), -1)
    cloudSprites =  []
    cloudSprites.append(Cloud(screen, (0, 000)))
    cloudSprites.append(Cloud(screen, (300, 100)))
    cloudSprites.append(Cloud(screen, (600, 200)))
    
    shipSprite = MiGX3(screen, 50, 0)
    collectableMissileSprite = CollectableMissile(screen)
    
    scoreBoard = ScoreBoard(screen.get_width() / 2 * 1.5, 25)
    lifeCounter = LifeCounter(screen.get_width() / 2 * 0.5, 25)
    missileCounter = MissileCounter(screen.get_width() / 2 * 1.75, 25)
    
    #Define groups
    backgroundSprites = pygame.sprite.OrderedUpdates(skySprite, cloudSprites, citySprite)
    boardPanelSprites = pygame.sprite.Group(scoreBoard, lifeCounter, missileCounter)
    playerSprites = pygame.sprite.Group(shipSprite)
    pwBulletSprites = pygame.sprite.Group()
    swMissileSprites = pygame.sprite.Group()
    randomEnemySprites = pygame.sprite.Group()
    explosionSprites = pygame.sprite.Group()
    collectableMissiles = pygame.sprite.Group(collectableMissileSprite)
    
    # Set up stage one
    randomEnemySprites = setupStageOne(randomEnemySprites, shipSprite)
    
    # Play intro theme
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_DIRECTORY + "stage1_theme.ogg")
        pygame.mixer.music.play(-1)
            
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                keepPlaying = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseState = pygame.mouse.get_pressed()
                if mouseState[0]: #Shoot primary weapon
                    shipSprite.sndPrimaryWeapon.stop()
                    shipSprite.sndPrimaryWeapon.play()
                    pwBulletSprites.add(Bullet(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))
                            
                if mouseState[2]: #Shoot secondary weapon
                    if missileCounter.noMissiles == False:
                        shipSprite.sndSecondaryWeapon.stop()
                        shipSprite.sndSecondaryWeapon.play()    
                        swMissileSprites.add(SpecialShot(screen, shipSprite.rect.centerx, shipSprite.rect.centery-3))  
                        missileCounter.removeMissile()
                    
        backgroundSprites.update()
        playerSprites.update()
        pwBulletSprites.update()
        swMissileSprites.update()
        boardPanelSprites.update()
        randomEnemySprites.update()
        explosionSprites.update()
        collectableMissiles.update()
        
        #Check if collision between player and collectable item occured
        CollectableItem_Player_Collision = pygame.sprite.spritecollide(shipSprite, collectableMissiles, False)
        if CollectableItem_Player_Collision:
            missileCounter.addMissile()
            for missiles in collectableMissiles:
                missiles.reset()
                
        #Check collision between objects
        Player_RandomEnemy_collision = pygame.sprite.spritecollide(shipSprite, randomEnemySprites, False)
                
        if Player_RandomEnemy_collision:
            lifeCounter.removeLife()
            if lifeCounter.isDead == True:
                running = False
          
            for res in randomEnemySprites:
                res.reset()
        
        #Check if primary weapon bullet hit any enemies 
        for pwBullet in pwBulletSprites:
            pwBullet_RandomEnemy_collision = pygame.sprite.spritecollide(pwBullet, randomEnemySprites, False)
            
            if pwBullet_RandomEnemy_collision:
                # Kill the enemy if we did enough damage to it
                for re in pwBullet_RandomEnemy_collision:                    
                    re.health -= pwBullet.damage
                    if re.health <= 0:
                        # Play death sound effect
                        scoreBoard.score += 100
                        re.sndDeath.play()
                        re.kill()
                        countRandomEnemies -= 1
                        explosion = Explosion(re.rect.center, re.dx)
                        explosion.state = Explosion.EXPLODING
                        explosionSprites.add(explosion)                                       
                    else:
                        # Play hit sound effect
                        scoreBoard.score += 10
                        re.sndHit.play()
                        re.isHit = True
                        
                pwBullet.kill()
        
        #Check if secondary weapon bullet hit any enemies     
        for swMissile in swMissileSprites:  
            swMissile_RandomEnemy_collision = pygame.sprite.spritecollide(swMissile, randomEnemySprites, False)
            
            if swMissile_RandomEnemy_collision:
                # Kill the enemy if we did enough damage to it
                for re in swMissile_RandomEnemy_collision:                    
                    re.health -= swMissile.damage
                    if re.health <= 0:
                        # Play death sound effect
                        scoreBoard.score += 100
                        re.sndDeath.play()
                        re.kill()
                        countRandomEnemies -= 1
                        explosion = Explosion(re.rect.center, re.dx)
                        explosion.state = Explosion.EXPLODING
                        explosionSprites.add(explosion)                           
                    else:
                        # Play hit sound effect
                        scoreBoard.score += 10
                        re.sndHit.play()
                swMissile.kill()
           
        #If there are zero ships left on the screen add more
        if countRandomEnemies == 0:
            countRandomEnemies = 20
            randomEnemySprites = setupStageOne(randomEnemySprites, shipSprite)
                     
        backgroundSprites.draw(screen)
        pwBulletSprites.draw(screen)
        collectableMissiles.draw(screen)
        swMissileSprites.draw(screen)
        playerSprites.draw(screen)
        boardPanelSprites.draw(screen)
        randomEnemySprites.draw(screen)
        explosionSprites.draw(screen)
        
        
        pygame.display.flip()
          
    return keepPlaying, scoreBoard.score
          
def gameEndScreen(score):
    running = True
    keepPlaying = True
    
    currentStage = 1
    
    #Clear Screen
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    #Declare background sprites 
    citySprite = Parallax(screen, pygame.image.load( STAGE_BACKGROUNDS[currentStage-1][0] ), -5)
    skySprite = Parallax(screen, pygame.image.load( STAGE_BACKGROUNDS[currentStage-1][1] ), -1)
    cloudSprites =  []
    cloudSprites.append(Cloud(screen, (0, 000)))
    cloudSprites.append(Cloud(screen, (300, 100)))
    cloudSprites.append(Cloud(screen, (600, 200)))
  
    #Font text
    youDiedText = MyFont('You died!.', screen.get_width()/2*0.45, 250, 22, (225, 225, 225))
    scoreText = MyFont('Your score was: %d' % score, screen.get_width()/2*0.55, 300, 22, (225, 225, 225))
    clickAnywhereText = MyFont('Click any key to continue...', screen.get_width()/2, screen.get_height()/2+100, 30, (255, 255, 255))
    
    #Ship sprite (not shown in end screen
    shipSprite = MiGX3(screen, 50, 0)
    
    #Define groups
    backgroundSprites = pygame.sprite.OrderedUpdates(skySprite, cloudSprites, citySprite)
    pwBulletSprites = pygame.sprite.Group()
    swMissileSprites = pygame.sprite.Group()
    randomEnemySprites = pygame.sprite.Group()
    fontSprites = pygame.sprite.Group(youDiedText, scoreText, clickAnywhereText)
    
    # Set up stage one
    randomEnemySprites = setupStageOne(randomEnemySprites, shipSprite)
    
    # Play end theme (same as intro theme
    if not pygame.mixer:
        print("Cannot Load Sounds")
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_DIRECTORY + "intro_theme.ogg")
        pygame.mixer.music.play(-1)
            
                        
    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                keepPlaying = False
            if event.type == pygame.KEYDOWN:
                keepPlaying = True
                running = False


        backgroundSprites.update()
        pwBulletSprites.update()
        swMissileSprites.update()
        randomEnemySprites.update()
        fontSprites.update()
        
        backgroundSprites.draw(screen)
        pwBulletSprites.draw(screen)
        swMissileSprites.draw(screen)
        randomEnemySprites.draw(screen)
        fontSprites.draw(screen)
        
        pygame.display.flip()
        
        
    return keepPlaying


def main():
    
    keepPlaying = True
    
    while keepPlaying:
        toContinue = startScreen()
        if toContinue:
            keepPlaying, score = gamePlayScreen()
            if keepPlaying:
                keepPlaying = gameEndScreen(score)
        else:
            keepPlaying = False

    
    
if __name__ == '__main__': 
    main()
