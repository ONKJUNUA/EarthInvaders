import pygame

class Block (pygame.sprite.Sprite):
    def __init__(self, size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

shape = [
    'xx            xx',
    'xx     xx     xx',
    ' xx  xxxxxx  xx',
    ' xxxxxxxxxxxxxx',
    '  xxxx    xxxx',
    '   xxxxxxxxxx',
    '   xx      xx',
    '  xxxxxxxxxxxx',
    '  xx        xx',
    ' xxxxxxxxxxxxxx',
    ' xx          xx',
    'xxxxxxxxxxxxxxxx',
    'xxxxxxxxxxxxxxxx',
    'xxxxx  xx  xxxxx',
    'xxx    xx    xxx',
    'x              x']