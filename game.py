import pygame
import pygame.locals

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((300,200))
pygame.display.set_caption('Alien Tower')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((240, 240, 240))

base = background.copy()

tower = pygame.Surface((20, 200))
tower = tower.convert()
tower.fill((255, 0, 0))
towerpos = tower.get_rect()
towerpos.centerx = base.get_rect().centerx

background.blit(tower, towerpos)
base.blit(tower, towerpos)

class Player(object):
    MAX_JUMP = 40
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
        self.jump_at = 0
        self.jump_direction = 0
        self.jumping = False

    def draw_on(self, surface):
        surface.blit(self.blank, self.blank.get_rect())
        surface.blit(self.viz, self.pos)

    def move_left_on(self, surface):
        self.pos.x -= 1
        self.draw_on(surface)
        self.prev = self.pos.copy()

    def move_right_on(self, surface):
        self.pos.x += 1
        self.draw_on(surface)
        self.prev = self.pos.copy()

    def animate_jump_on(self, surface):
        if self.jump_at < self.MAX_JUMP and self.jump_direction > 0:
            self.jump_at += 1
            self.pos.y -= 1
        elif self.jump_at > 0 and self.jump_direction < 0:
            self.jump_at -= 1
            self.pos.y += 1

        if self.jump_at == 0:
            self.jumping = False
            self.jump_direction = 0
        elif self.jump_at == self.MAX_JUMP:
            self.jump_direction = -1
        self.draw_on(surface)
        self.prev = self.pos.copy()

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_direction = 1

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
