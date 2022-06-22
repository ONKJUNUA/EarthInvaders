import pygame

class Perks(pygame.sprite.Sprite):
    def __init__(self,symbol,x,y,):
        super().__init__()
        file_path = 'graphics/' + symbol + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft =(x,y))

        if symbol == 'p_heart': 
            pass
        elif symbol == 'p_time': 
            pass
        elif symbol == 'p_bullet': 
            pass
        elif symbol == 'p_aim': 
            pass

    def update(self,direction):
        self.rect.y += direction