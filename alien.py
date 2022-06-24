import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, number, x, y):
        super().__init__()
        file_path = 'graphics/' + number + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft =(x, y))

        if number == '1': 
            self.value = 10
            self.enemy_lives = 1
        elif number == '2': 
            self.value = 20
            self.enemy_lives = 2
        elif number == '3': 
            self.value = 30
            self.enemy_lives = 3
        elif number == '4': 
            self.value = 40
            self.enemy_lives = 4
        elif number == '5': 
            self.value = 50
            self.enemy_lives = 5
        elif number == '6': 
            self.value = 60
            self.enemy_lives = 6
        elif number == '7': 
            self.value = 70
            self.enemy_lives = 7
        elif number == '8': 
            self.value = 80
            self.enemy_lives = 8
        elif number == '9': 
            self.value = 90
            self.enemy_lives = 9
        elif number == '10': 
            self.value = 100
            self.enemy_lives = 10
        elif number == '11': 
            self.value = 110
            self.enemy_lives = 11
        elif number == '12': 
            self.value = 120
            self.enemy_lives = 12

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('graphics/extra.png').convert_alpha()
        if side == 'right':
            x = screen_width + 50
            self.speed = - 3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (x,100))

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= 750:
            self.kill()

    def update(self):
        self.rect.x += self.speed
        self.destroy()