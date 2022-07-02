import pygame, shelve

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image = pygame.image.load('graphics/boss.png').convert_alpha()
        elif p == 2: self.image = pygame.image.load('graphics/boss_m.png').convert_alpha()
        elif p == 3: self.image = pygame.image.load('graphics/boss_v.png').convert_alpha()
        elif p == 4: self.image = pygame.image.load('graphics/boss_o.png').convert_alpha()
        self.rect = self.image.get_rect(center =(x,y))
        self.value = 5000
        self.enemy_lives = 10000

    def update(self, direction):
        self.rect.x += direction