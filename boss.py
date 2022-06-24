import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        file_path = 'graphics/boss.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center =(x,y))
        self.value = 10000
        self.enemy_lives = 5000

    def update(self, direction):
        self.rect.x += direction