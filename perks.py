import pygame, shelve

class Shield(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image = pygame.image.load('graphics/p_shield.png').convert_alpha()
        elif p == 2: self.image = pygame.image.load('graphics/p_shield_m.png').convert_alpha()
        elif p == 3: self.image = pygame.image.load('graphics/p_shield_v.png').convert_alpha()
        elif p == 4: self.image = pygame.image.load('graphics/p_shield_o.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image = pygame.image.load('graphics/p_heart.png').convert_alpha()
        elif p == 2: self.image = pygame.image.load('graphics/p_heart_m.png').convert_alpha()
        elif p == 3: self.image = pygame.image.load('graphics/p_heart_v.png').convert_alpha()
        elif p == 4: self.image = pygame.image.load('graphics/p_heart_o.png').convert_alpha()
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
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image = pygame.image.load('graphics/p_time.png').convert_alpha()
        elif p == 2: self.image = pygame.image.load('graphics/p_time_m.png').convert_alpha()
        elif p == 3: self.image = pygame.image.load('graphics/p_time_v.png').convert_alpha()
        elif p == 4: self.image = pygame.image.load('graphics/p_time_o.png').convert_alpha()
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
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image = pygame.image.load('graphics/p_bullet.png').convert_alpha()
        elif p == 2: self.image = pygame.image.load('graphics/p_bullet_m.png').convert_alpha()
        elif p == 3: self.image = pygame.image.load('graphics/p_bullet_v.png').convert_alpha()
        elif p == 4: self.image = pygame.image.load('graphics/p_bullet_o.png').convert_alpha()
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
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image = pygame.image.load('graphics/p_aim.png').convert_alpha()
        elif p == 2: self.image = pygame.image.load('graphics/p_aim_m.png').convert_alpha()
        elif p == 3: self.image = pygame.image.load('graphics/p_aim_v.png').convert_alpha()
        elif p == 4: self.image = pygame.image.load('graphics/p_aim_o.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()