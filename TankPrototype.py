import pygame
import time
pygame.init()

WIDTH, HEIGHT = 1200, 800 
FPS = 60
TILE = 32

Fire = pygame.mixer.Sound('fire2.ogg')

Background = pygame.mixer.Sound('backgroundl.ogg')
Background.play(-1)
Victory = pygame.mixer.Sound('victory.ogg')


window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('tanks')

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

class Tank:
    def __init__(self, color, px, py, direct, keyList, player_image):
        objects.append(self)
        self.type = 'tank'

        self.image = pygame.transform.scale(pygame.image.load(player_image), (32, 32))
        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 120




        self.shotTimer = 0
        self.shotDelay = 45
        self.bulletSpeed = 10
        self.bulletDamage = 20

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

    def update(self):
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            self.image = pygame.transform.scale(pygame.image.load('tank.left.png'), (32, 32))
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
            self.image = pygame.transform.scale(pygame.image.load('tank.right.png'), (32, 32))
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            self.image = pygame.transform.scale(pygame.image.load('tank.up.png'), (32, 32))
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
            self.image = pygame.transform.scale(pygame.image.load('tank.down.png'), (32, 32))

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
            Fire.play()

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.image, (self.rect.x, self.rect.y))

        x = self.rect.centerx + DIRECTS[self.direct][0] * 30
        y = self.rect.centery + DIRECTS[self.direct][1] * 30
        pygame.draw.line(window, (0, 0, 0 ), self.rect.center, (x, y), 3)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            self.image = pygame.transform.scale(pygame.image.load('honored.png'), (32, 32))
            Background.stop()
            Victory.play()
            self.hp = 120



class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, (255, 200, 0), (self.px, self.py), 3)
        
    
class Walls():
    def __init__(self):
        self.x = 1
        self.wall_list = []
    def draww(self):
        color_wall = (200, 200, 100)
        w1 = pygame.draw.rect
        w2 = pygame.draw.rect

        self.wall_list = [w1, w2]

    def getwalllist(self):
        return self.wall_list

wall = Walls
bullets = []
objects = []
Tank((200, 200, 200), 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),'tank1.png')
Tank((200, 255, 200), 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RCTRL), 'tank1.png')


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()
    
    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()

    window.fill((0, 0, 0))
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()
