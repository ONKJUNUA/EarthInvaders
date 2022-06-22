import pygame

class Perks(pygame.sprite.Sprite):
    def __init__(self,symbol,pos,speed,screen_height):
        super().__init__()
        file_path = 'graphics/' + symbol + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

        if symbol == 'p_heart': 
            pass
        elif symbol == 'p_time': 
            pass
        elif symbol == 'p_bullet': 
            pass
        elif symbol == 'p_aim': 
            pass

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()