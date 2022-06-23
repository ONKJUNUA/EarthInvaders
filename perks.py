import pygame

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        file_path = 'graphics/p_heart.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Speed(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        file_path = 'graphics/p_time.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        file_path = 'graphics/p_bullet.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Damage(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        file_path = 'graphics/p_aim.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()