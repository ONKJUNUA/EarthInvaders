import pygame
from laser import Laser, Laser2, Laser3

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = 3
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.laser_bullet = 1
        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 10:
            self.rect.left = 10
        elif self.rect.right >= self.max_x_constraint - 10:
            self.rect.right = self.max_x_constraint - 10

    def shoot_laser(self):
        if self.laser_bullet == 1:
            self.bullet_speed = -6
            self.lasers.add(Laser(self.rect.center ,self.bullet_speed,self.rect.bottom))
        elif self.laser_bullet == 2:
            self.bullet_speed = -8
            self.lasers.add(Laser2(self.rect.bottomleft,self.bullet_speed,self.rect.bottom))
            self.lasers.add(Laser3(self.rect.bottomright,self.bullet_speed,self.rect.bottom))
        elif self.laser_bullet == 3:
            self.lasers.add(Laser(self.rect.center, self.bullet_speed, self.rect.bottom))
            self.lasers.add(Laser2(self.rect.bottomleft, self.bullet_speed, self.rect.bottom))
            self.lasers.add(Laser3(self.rect.bottomright, self.bullet_speed, self.rect.bottom))
        else:
            self.bullet_speed = -10
            self.lasers.add(Laser(self.rect.center, self.bullet_speed, self.rect.bottom))
            self.lasers.add(Laser2(self.rect.bottomleft, self.bullet_speed, self.rect.bottom))
            self.lasers.add(Laser3(self.rect.bottomright, self.bullet_speed, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()