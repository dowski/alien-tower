import pygame
import pygame.locals

clock = pygame.time.Clock()

ON_THE_FLOOR = 180

pygame.init()
screen = pygame.display.set_mode((300,200))
pygame.display.set_caption('Alien Tower')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((240, 240, 240))

base = background.copy()

tower = pygame.Surface((20, 200))
tower = tower.convert()
tower.fill((0, 254, 0))
towerpos = tower.get_rect()
towerpos.centerx = base.get_rect().centerx

platform = pygame.Surface((40, 10))
platform = platform.convert()
platform.fill((50,0,232))
platformpos = pygame.Rect(100,130,40,10)

background.blit(tower, towerpos)

base.blit(tower, towerpos)
base.blit(platform, platformpos)

class Player(object):
    MAX_JUMP = 80
    def __init__(self, pos_x, pos_y, base):
        self.viz = pygame.Surface((20, 20))
        self.viz = self.viz.convert()
        self.viz.fill((0,0,0))
        self.pos = self.viz.get_rect()
        self.pos.x = pos_x
        self.pos.y = pos_y
        self.prev = self.pos.copy()
        self.blank = base
        self.moving = 0
        self.jump_start = self.pos.y
        self.jump_direction = 0
        self.jumping = False

    def draw_on(self, surface):
        surface.blit(self.blank, self.blank.get_rect())
        surface.blit(self.viz, self.pos)

    def move_left_on(self, surface):
        self.pos.x -= 1
        self.draw_on(surface)
        self.prev = self.pos.copy()
        if not self.on_platform and not self.jumping:
            self.fall()

    def move_right_on(self, surface):
        self.pos.x += 1
        self.draw_on(surface)
        self.prev = self.pos.copy()
        if not self.on_platform and not self.jumping:
            self.fall()

    def fall(self):
        self.jumping = True
        self.jump_start = ON_THE_FLOOR
        self.jump_direction = -1

    @property
    def on_platform(self):
        if self.pos.y == ON_THE_FLOOR:
            return True
        elif self.pos.y == 110 and (self.pos.x > 80 and self.pos.x < 140):
            return True
        return False

    def animate_jump_on(self, surface):
        if self.jump_start - self.MAX_JUMP < self.pos.y and self.jump_direction > 0:
            self.pos.y -= 1
        elif not self.on_platform and self.jump_direction < 0:
            self.pos.y += 1
        else:
            self.jump_direction = -1

        if self.on_platform:
            self.jumping = False
            self.jump_direction = 0
        self.draw_on(surface)
        self.prev = self.pos.copy()

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_direction = 1
            self.jump_start = self.pos.y

player = Player(140, 180, base)

player.draw_on(background)

screen.blit(background, (0,0))
pygame.display.flip()


mod = 0
LEFT = -1
RIGHT = 1
JUMP = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            raise SystemExit(0)
        elif event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_LEFT:
                player.moving = -1
            elif event.key == pygame.locals.K_RIGHT:
                player.moving = 1
            elif event.key == pygame.locals.K_UP:
                player.jump()
        elif event.type == pygame.locals.KEYUP:
            player.moving = 0

    if player.moving == LEFT:
        player.move_left_on(background)
    elif player.moving == RIGHT:
        player.move_right_on(background)
    if player.jumping:
        player.animate_jump_on(background)

    if player.moving or player.jumping:
        screen.blit(background, (0,0))
        pygame.display.flip()
    clock.tick(60)
