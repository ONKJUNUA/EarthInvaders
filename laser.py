import pygame, shelve

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4,20))
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image.fill((255,255,255))
        elif p == 2: self.image.fill((88,199,171))
        elif p == 3: self.image.fill((174,110,230))
        elif p == 4: self.image.fill((224,152,63))
        self.rect = self.image.get_rect(midtop = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Laser2(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4,20))
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image.fill((255,255,255))
        elif p == 2: self.image.fill((88,199,171))
        elif p == 3: self.image.fill((174,110,230))
        elif p == 4: self.image.fill((224,152,63))
        self.rect = self.image.get_rect(midleft = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class Laser3(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4,20))
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image.fill((255,255,255))
        elif p == 2: self.image.fill((88,199,171))
        elif p == 3: self.image.fill((174,110,230))
        elif p == 4: self.image.fill((224,152,63))
        self.rect = self.image.get_rect(midright = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class BossLaser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((100,5))
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: self.image.fill((255,255,255))
        elif p == 2: self.image.fill((88,199,171))
        elif p == 3: self.image.fill((174,110,230))
        elif p == 4: self.image.fill((224,152,63))
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()

class ChildLaser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        color_o = shelve.open('doc/color.txt')
        p = color_o['color']
        color_o.close()
        if p == 1: file_path = 'graphics/childboss.png'
        elif p == 2: file_path = 'graphics/childboss_m.png'
        elif p == 3: file_path = 'graphics/childboss_v.png'
        elif p == 4: file_path = 'graphics/childboss_o.png'
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