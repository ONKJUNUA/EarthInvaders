import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,number,x,y):
        super().__init__()
        file_path = 'graphics/' + number + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft =(x,y))

    def update(self,direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = pygame.image.load('graphics/extra.png').convert_alpha()
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (x,100))

    def update(self):
        self.rect.x += self.speed