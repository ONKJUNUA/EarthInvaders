import pygame, sys, os, subprocess
from random import choice, randint
from boss import Boss
import obstacles
from perks import Bullet, Damage, Heart, Shield, Speed
from player import Player
from alien import Alien, Extra, FakeAlien
from laser import BossLaser, ChildLaser, Laser

class Game:
    def __init__(self):
        player_sprite = Player((screen_width/2, screen_height - 10), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.killable = False
        self.level = 0
        self.lives = 0
        self.dmg = 0
        self.speed_charge = 5
        self.bullet_charge = 5
        self.damage_charge = 5
        self.live_icon = pygame.image.load('graphics/player.png').convert_alpha()
        self.score = 0
        self.font = pygame.font.Font('font/pixel.ttf', 25)
        self.level_font = pygame.font.Font('font/pixel.ttf', 35)
        self.title_font = pygame.font.Font('font/pixel.ttf', 50)
        
        self.alien_cooldown = 800
        self.boss_cooldown = 600
        self.shape = obstacles.shape
        self.block_size = 3
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num *(screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 12, y_start = 770)

        self.aliens = pygame.sprite.Group()
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        self.fake_aliens = pygame.sprite.Group()
        self.fake_alien_direction = 1

        self.extra = pygame.sprite.Group()
        self.extra_spawn_time = randint (1500, 1500)

        self.heart = pygame.sprite.Group()
        self.shield = pygame.sprite.Group()
        self.laser_speed = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.damage = pygame.sprite.Group()

    def death(self):
        lose()

    def create_obstacle(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacles.Block(self.block_size,(120,120,120),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance = 85, y_distance = 80, x_offset = 27, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                if self.level != 11:
                    if row_index <= 1: alien_sprite = Alien(str(2+self.level), x, y)
                    elif 2 <= row_index <= 3: alien_sprite = Alien(str(1+self.level), x, y)
                    else: alien_sprite = Alien(str(0+self.level), x, y)
                    self.aliens.add(alien_sprite)

    def one_alien(self, x = 450, y = 947):
        if self.level <= 11:
            alien_sprite = Alien(str(0+self.level), x, y)
            self.aliens.add(alien_sprite)

    def earth(self, x = 450, y = -200):
        alien_sprite = FakeAlien('earth', x, y)
        self.aliens.add(alien_sprite)

    def fake_alien(self, rows, cols, x_distance = 85, y_distance = 80, x_offset = 27, y_offset = 500):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = FakeAlien('12', x, y)
                self.fake_aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width - 10:
                self.alien_direction = -1
                self.alien_move_down(1)
            elif alien.rect.left <= 10:
                self.alien_direction = 1
                self.alien_move_down(1)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shot(self):
        if self.aliens.sprites():
            global power
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, self.level + power, screen_height)
            self.alien_lasers.add(laser_sprite)
        
    def boss_shot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = BossLaser(random_alien.rect.center, self.level - 3, screen_height)
            self.alien_lasers.add(laser_sprite)

    def child_shot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = ChildLaser(random_alien.rect.center, self.level +10, screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']), screen_width))
            self.extra_spawn_time = randint (1000,2000)

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit_check = pygame.sprite.spritecollide(laser, self.aliens, False)
                if aliens_hit_check:
                    for alien in aliens_hit_check:
                        if alien.enemy_lives <= self.dmg:
                            self.killable = True
                        else:
                            self.killable = False
                            alien.enemy_lives -= self.dmg

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, self.killable)
                if aliens_hit:
                    for alien in aliens_hit:
                        if self.killable == True:
                            self.score += alien.value
                    laser.kill()

                fake_aliens_hit_check = pygame.sprite.spritecollide(laser, self.fake_aliens, False)
                if fake_aliens_hit_check:
                    for fake_alien in fake_aliens_hit_check:
                        if fake_alien.enemy_lives <= self.dmg:
                            self.killable = True
                        else:
                            self.killable = False
                            fake_alien.enemy_lives -= self.dmg

                fake_aliens_hit = pygame.sprite.spritecollide(laser, self.fake_aliens, self.killable)
                if fake_aliens_hit:
                    for fake_alien in aliens_hit:
                        if self.killable == True:
                            pass
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 100
                    if self.level >= 6:
                        self.choice = randint(1,4)
                        if self.choice == 1:
                            self.drop_shield()
                        else: self.drop_heart()
                    else: self.drop_heart()
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.death()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.death()

        if self.fake_aliens:
            for fake_alien in self.fake_aliens:
                pygame.sprite.spritecollide(fake_alien, self.blocks, True)

        if self.player:
            for player in self.player:
                if pygame.sprite.spritecollide(player, self.heart, True):
                    self.lives += 1
                if pygame.sprite.spritecollide(player, self.shield, True):
                    self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 12, y_start = 770)
                if pygame.sprite.spritecollide(player, self.laser_speed, True):
                    player.laser_cooldown -= 100
                    player.speed += 1
                    self.speed_charge -= 1
                if pygame.sprite.spritecollide(player, self.bullet, True):
                    player.laser_bullet += 1
                    self.bullet_charge -= 1
                if pygame.sprite.spritecollide(player, self.damage, True):
                    self.dmg += 1
                    self.damage_charge -= 1
                if pygame.sprite.spritecollide(player,self.fake_aliens,True):
                    self.lives -= 1
                    if self.lives <= 0:
                        self.death()

    def display_lives(self):
            lives_surf = self.font.render(f'{self.lives - 1}x', False, 'white')
            screen.blit(lives_surf,(565,25))
            screen.blit(self.live_icon,(625,10))

    def display_level(self):
        if self.level <= 11:
            if self.level <= 10: level_surf = self.font.render(f'Level {self.level}', False, 'white')
            else: level_surf = self.font.render(f'Boss', False, 'white')
            level_rect = level_surf.get_rect(topleft = (350,25))
            screen.blit(level_surf, level_rect)

    def display_score(self):
        score_surf = self.font.render(f'Score:{self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (25,25))
        screen.blit(score_surf, score_rect)

    def drop_heart(self):
        heart_sprite = Heart((screen_width/2, 100), 4, screen_height)
        self.heart.add(heart_sprite)

    def drop_shield(self):
        shield_sprite = Shield((screen_width/2, 100), 4, screen_height)
        self.shield.add(shield_sprite)

    def drop_perks(self):
        if self.speed_charge >= 1:
            speed_sprite = Speed((screen_width/2 + screen_width/4 ,200), 6, screen_height)
            self.laser_speed.add(speed_sprite)
        else: pass
        if self.bullet_charge >= 1:
            bullet_sprite = Bullet((screen_width/4, 200), 6, screen_height)
            self.bullet.add(bullet_sprite)
        else: pass
        if self.damage_charge >= 1:
            damage_sprite = Damage((screen_width/2, 200), 6, screen_height)
            self.damage.add(damage_sprite)
        else: pass

    def boss_setup(self):
        boss_sprite = Boss(screen_width/2,screen_height/3)
        self.aliens.add(boss_sprite)

    def boss_attack(self):
        attack_type = randint(1,4)
        if attack_type == 1:
            pygame.time.set_timer(BOSSLASER, self.boss_cooldown, loops = 10)
        if attack_type == 2:
            self.fake_alien(rows = 2, cols = 8)
        if attack_type == 3:
            pygame.time.set_timer(CHILDLASER, self.boss_cooldown, loops = 5)
        if attack_type == 4:
            self.fake_alien(rows = 1, cols = 8)

    def next_level(self):
        if self.aliens.sprites():
            if self.level == 0:
                pass

        if not self.aliens.sprites():
            if self.level == 0:
                self.level += 1
                self.one_alien()
                pygame.time.set_timer(ALIENSET,1700,loops = 1)
            elif self.level <= 10:
                self.level += 1
                self.drop_perks()
                self.one_alien()
                pygame.time.set_timer(ALIENSET,1700,loops = 1)
            else: win()
            
    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()
        self.heart.update()
        self.shield.update()
        self.laser_speed.update()
        self.bullet.update()
        self.damage.update()

        self.aliens.update(self.alien_direction)
        self.fake_aliens.update(self.fake_alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.fake_aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.heart.draw(screen)
        self.shield.draw(screen)
        self.laser_speed.draw(screen)
        self.bullet.draw(screen)
        self.damage.draw(screen)

        self.display_lives()
        self.display_level()
        self.display_score()
        self.next_level()

class Game2:
    def __init__(self):
        player_sprite = Player((screen_width/2, screen_height - 10), screen_width)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.killable = False
        self.level = 0
        self.lives = 6
        self.dmg = 2
        self.speed_charge = 5
        self.bullet_charge = 5
        self.live_icon = pygame.image.load('graphics/player.png').convert_alpha()
        self.score = 0
        self.font = pygame.font.Font('font/pixel.ttf', 25)
        self.level_font = pygame.font.Font('font/pixel.ttf', 35)
        self.title_font = pygame.font.Font('font/pixel.ttf', 50)
        
        self.alien_cooldown = 1000
        self.shape = obstacles.shape
        self.block_size = 3
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num *(screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 12, y_start = 770)

        self.aliens = pygame.sprite.Group()
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        self.extra = pygame.sprite.Group()
        self.extra_spawn_time = randint (1500, 1500)

        self.heart = pygame.sprite.Group()
        self.shield = pygame.sprite.Group()
        self.laser_speed = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.damage = pygame.sprite.Group()

    def death(self):
        lose2()

    def create_obstacle(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacles.Block(self.block_size,(120,120,120),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance = 85, y_distance = 80, x_offset = 27, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if self.level <= 4:                
                    if row_index <= 1: alien_sprite = Alien(str(randint(5,6)), x, y)
                    elif 2 <= row_index <= 3: alien_sprite = Alien(str(randint(3,4)), x, y)
                    else: alien_sprite = Alien(str(randint(1,2)), x, y)
                    self.aliens.add(alien_sprite)
                elif 5 <= self.level <= 8:                
                    if row_index <= 1: alien_sprite = Alien(str(randint(7,9)), x, y)
                    elif 2 <= row_index <= 3: alien_sprite = Alien(str(randint(4,6)), x, y)
                    else: alien_sprite = Alien(str(randint(1,3)), x, y)
                    self.aliens.add(alien_sprite)
                elif 9 <= self.level <= 10:                
                    if row_index <= 1: alien_sprite = Alien(str(randint(7,12)), x, y)
                    elif 2 <= row_index <= 3: alien_sprite = Alien(str(randint(4,8)), x, y)
                    else: alien_sprite = Alien(str(randint(1,5)), x, y)
                    self.aliens.add(alien_sprite)
                elif 11 <= self.level <= 12:                
                    if row_index <= 1: alien_sprite = Alien(str(randint(7,12)), x, y)
                    elif 2 <= row_index <= 3: alien_sprite = Alien(str(randint(4,10)), x, y)
                    else: alien_sprite = Alien(str(randint(1,8)), x, y)
                    self.aliens.add(alien_sprite)
                else:
                    if row_index <= 1: alien_sprite = Alien(str(randint(10,12)), x, y)
                    elif 2 <= row_index <= 3: alien_sprite = Alien(str(randint(6,12)), x, y)
                    else: alien_sprite = Alien(str(randint(1,12)), x, y)
                    self.aliens.add(alien_sprite)

    def one_alien(self, x = 450, y = 947):
        alien_sprite = Alien(str(1), x, y)
        self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width - 10:
                self.alien_direction = -1
                self.alien_move_down(1)
            elif alien.rect.left <= 10:
                self.alien_direction = 1
                self.alien_move_down(1)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shot(self):
        if self.aliens.sprites():
            global power
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, self.level + power, screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']), screen_width))
            self.extra_spawn_time = randint (1000,2000)

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                aliens_hit_check = pygame.sprite.spritecollide(laser, self.aliens, False)
                if aliens_hit_check:
                    for alien in aliens_hit_check:
                        if alien.enemy_lives <= self.dmg:
                            self.killable = True
                        else:
                            self.killable = False
                            alien.enemy_lives -= self.dmg

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, self.killable)
                if aliens_hit:
                    for alien in aliens_hit:
                        if self.killable == True:
                            self.score += alien.value
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 100
                    if self.level >= 6:
                        self.choice = randint(1,4)
                        if self.choice == 1:
                            self.drop_shield()
                        else: self.drop_heart()
                    else: self.drop_heart()
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.death()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.death()

        if self.player:
            for player in self.player:
                if pygame.sprite.spritecollide(player, self.heart, True):
                    self.lives += 1
                if pygame.sprite.spritecollide(player, self.shield, True):
                    self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 12, y_start = 770)
                if pygame.sprite.spritecollide(player, self.laser_speed, True):
                    player.laser_cooldown -= 100
                    player.speed += 1
                    self.speed_charge -= 1
                if pygame.sprite.spritecollide(player, self.bullet, True):
                    player.laser_bullet += 1
                    self.bullet_charge -= 1
                if pygame.sprite.spritecollide(player, self.damage, True):
                    self.dmg += 1

    def display_lives(self):
            lives_surf = self.font.render(f'{self.lives - 1}x', False, 'white')
            screen.blit(lives_surf,(565,25))
            screen.blit(self.live_icon,(625,10))

    def display_level(self):
        level_surf = self.font.render('Endless', False, 'white')
        level_rect = level_surf.get_rect(topleft = (350,25))
        screen.blit(level_surf, level_rect)

    def display_score(self):
        score_surf = self.font.render(f'Score:{self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (25,25))
        screen.blit(score_surf, score_rect)

    def drop_heart(self):
        heart_sprite = Heart((screen_width/2, 100), 4, screen_height)
        self.heart.add(heart_sprite)

    def drop_shield(self):
        shield_sprite = Shield((screen_width/2, 100), 4, screen_height)
        self.shield.add(shield_sprite)

    def drop_perks(self):
        if self.speed_charge >= 1:
            speed_sprite = Speed((screen_width/2 + screen_width/4 ,200), 6, screen_height)
            self.laser_speed.add(speed_sprite)
        else: pass
        if self.bullet_charge >= 1:
            bullet_sprite = Bullet((screen_width/4, 200), 6, screen_height)
            self.bullet.add(bullet_sprite)
        else: pass
        damage_sprite = Damage((screen_width/2, 200), 6, screen_height)
        self.damage.add(damage_sprite)

    def next_level(self):

        if not self.aliens.sprites():
            if self.level == 0:
                self.level += 1
                self.one_alien()
                pygame.time.set_timer(ALIENSET,1700,loops = 1)
            else:
                self.level += 1
                self.drop_perks()
                self.one_alien()
                pygame.time.set_timer(ALIENSET,1700,loops = 1)
            
    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()
        self.heart.update()
        self.shield.update()
        self.laser_speed.update()
        self.bullet.update()
        self.damage.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.heart.draw(screen)
        self.shield.draw(screen)
        self.laser_speed.draw(screen)
        self.bullet.draw(screen)
        self.damage.draw(screen)

        self.display_lives()
        self.display_level()
        self.display_score()
        self.next_level()

class Button:
    def __init__(self,text,width,height,pos):
        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (255,255,255)
        self.text_surf = game_font.render(text,True,(30,30,30))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        global credit, option, start, rul, power
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (120,120,120)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    if button_1.pressed:
                        menu()                 
                    elif button_2.pressed:
                        options()                   
                    elif button_3.pressed:
                        credits()
                    self.pressed = False               
        else:
            self.top_color = (255,255,255)

class ButtonGame:
    def __init__(self,text,width,height,pos):
        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (255,255,255)
        self.text_surf = game_font.render(text,True,(30,30,30))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        global credit, option, start, rul, power
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (120,120,120)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    if button_6.pressed:
                        game2.level = 0
                        game2.lives = 6
                        game2.dmg = 2
                        power = 3
                        gameplay2()
                    if button_10.pressed:
                        game.level = 0
                        game.lives = 2
                        game.dmg = 1
                        power = 10
                        gameplay()
                    if button_11.pressed:
                        game.level = 0
                        game.lives = 4
                        game.dmg = 2
                        power = 5
                        gameplay()
                    if button_12.pressed:
                        game.level = 0
                        game.lives = 6
                        game.dmg = 3
                        power = 3
                        gameplay()
                    self.pressed = False
        else:
            self.top_color = (255,255,255)

class ButtonRul:
    def __init__(self,text,width,height,pos):
        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (255,255,255)
        self.text_surf = game_font.render(text,True,(30,30,30))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        global credit, option, start, rul, power
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (120,120,120)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    rules()
                    self.pressed = False
        else:
            self.top_color = (255,255,255)

class ButtonBack:
    def __init__(self,text,width,height,pos):
        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (255,255,255)
        self.text_surf = game_font.render(text,True,(30,30,30))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        global credit, option, start, rul, power
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (120,120,120)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    credit = False
                    option = False
                    start = False
                    self.pressed = False
        else:
            self.top_color = (255,255,255)

class ButtonBack2:
    def __init__(self,text,width,height,pos):
        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (255,255,255)
        self.text_surf = game_font.render(text,True,(30,30,30))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        global credit, option, start, rul, power
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (120,120,120)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    rul = False
                    self.pressed = False
        else:
            self.top_color = (255,255,255)

class ButtonRestart:
    def __init__(self,text,width,height,pos):
        self.pressed = False

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (255,255,255)
        self.text_surf = game_font.render(text,True,(30,30,30))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect)
        screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        global credit, option, start, rul, power
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (120,120,120)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    pygame.quit()
                    sys.stdout.flush()
                    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
                    self.pressed = False
                    sys.exit()
        else:
            self.top_color = (255,255,255)

def gameplay():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == ALIENLASER:
                if game.level <= 10: game.alien_shot()
            if event.type == BOSSLASER: game.boss_shot()
            if event.type == CHILDLASER: game.child_shot()
            if event.type == ALIENSET:
                if game.level <= 10: game.alien_setup(rows = 7, cols = 7)
                elif game.level == 11: 
                    game.boss_setup()
                    pygame.time.set_timer(BOSS, 3000)
                else: pass
            if event.type == BOSS:
                game.boss_attack()

        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)

def gameplay2():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == ALIENLASER:
                game2.alien_shot()
            if event.type == ALIENSET:
                game2.alien_setup(rows = 7, cols = 7)
        screen.fill((30, 30, 30))
        game2.run()
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    while True:
        screen.fill((30,30,30))

        title_text = str('Earth Invaders')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(100)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)
        
        n = -20
        a = pygame.image.load('graphics/10.png').convert_alpha()
        a_rect = a.get_rect(center = (150,250+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/8.png').convert_alpha()
        a_rect = a.get_rect(center = (250,250+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/11.png').convert_alpha()
        a_rect = a.get_rect(center = (350,250+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/4.png').convert_alpha()
        a_rect = a.get_rect(center = (450,250+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/9.png').convert_alpha()
        a_rect = a.get_rect(center = (550,250+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/5.png').convert_alpha()
        a_rect = a.get_rect(center = (250,350+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/3.png').convert_alpha()
        a_rect = a.get_rect(center = (350,350+n))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/6.png').convert_alpha()
        a_rect = a.get_rect(center = (450,350+n))
        screen.blit(a,a_rect)

        a = pygame.image.load('graphics/earth.png').convert_alpha()
        a_rect = a.get_rect(center = (700,450))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/earth.png').convert_alpha()
        a_rect = a.get_rect(center = (0,750))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/boss.png').convert_alpha()
        a_rect = a.get_rect(center = (700,750))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/boss.png').convert_alpha()
        a_rect = a.get_rect(center = (0,450))
        screen.blit(a,a_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        button_1.draw()
        button_2.draw()
        button_3.draw()

        pygame.display.update()
        clock.tick(60)

def credits():
    global credit
    credit = True
    while credit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    credit = False

        screen.fill((30,30,30))

        title_text = str('Earth Invaders')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(100)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        game_text = str('Made by XiR000')
        game_surface = game_font.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(300)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('Music:')
        game_surface = game_font.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(450)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('My Own Bit LOL')
        game_surface = game_font.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(500)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('Thanks for playing!')
        game_surface = game_font.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(650)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        button_4.draw()

        pygame.display.flip()
        clock.tick(60)

def options():
    global option
    option = True
    while option:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    option = False

        screen.fill((30,30,30))

        title_text = str('Earth Invaders')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(100)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        a = pygame.image.load('graphics/earth.png').convert_alpha()
        a_rect = a.get_rect(center = (700,700))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/earth.png').convert_alpha()
        a_rect = a.get_rect(center = (0,350))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/boss.png').convert_alpha()
        a_rect = a.get_rect(center = (700,350))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/boss.png').convert_alpha()
        a_rect = a.get_rect(center = (0,700))
        screen.blit(a,a_rect)

        button_9.draw()
        button_7.draw()
        button_5.draw()
        button_4.draw()

        pygame.display.flip()
        clock.tick(60)

def menu():
    global start
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start = False

        screen.fill((30,30,30))

        title_text = str('Earth Invaders')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(100)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        a = pygame.image.load('graphics/earth.png').convert_alpha()
        a_rect = a.get_rect(center = (700,700))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/earth.png').convert_alpha()
        a_rect = a.get_rect(center = (0,350))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/boss.png').convert_alpha()
        a_rect = a.get_rect(center = (700,350))
        screen.blit(a,a_rect)
        a = pygame.image.load('graphics/boss.png').convert_alpha()
        a_rect = a.get_rect(center = (0,700))
        screen.blit(a,a_rect)

        button_12.draw()
        button_11.draw()
        button_10.draw()
        button_6.draw()
        button_4.draw()

        pygame.display.flip()
        clock.tick(60)

def rules():
    global rul
    rul = True
    while rul:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rul = False

        screen.fill((30,30,30))

        title_text = str('Earth Invaders')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(100)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        game_text = str('1.Kill Aliens Using Spacebar')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(200)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('2.Move Your Ship Using Arrows')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(250)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('3.Survive By Collecting Perks')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(300)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('4.Watch Out For Your Life')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(350)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('5.Hide Behind Shields')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(400)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('6.Boss Have Multiple Moves')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(450)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('7.Take Down Extra Alien For Health')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(500)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('8.Get The Best Score')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(550)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('9.Try Every Mode')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(600)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        game_text = str('10.And Remember: Always Have Fun!')
        game_surface = game_font2.render(game_text,True,(255,255,255))
        game_x = int(screen_width/2)
        game_y = int(650)
        game_rect = game_surface.get_rect(center = (game_x,game_y))
        screen.blit(game_surface,game_rect)

        button_0.draw()

        pygame.display.flip()
        clock.tick(60)

def pause():
    global rul
    rul = True
    while rul:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rul = False

        pygame.draw.rect(screen, (30,30,30), pygame.Rect(0, 100, 700, 650))

        title_text = str('PAUSE')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/2)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        button_13.draw()

        pygame.display.flip()
        clock.tick(60)

def win():
    rul = True
    while rul:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        screen.fill((30, 30, 30))

        e = pygame.image.load('graphics/player.png').convert_alpha()
        e_rect = e.get_rect(center = (screen_width/2,screen_height - 50))
        screen.blit(e,e_rect)

        e = pygame.image.load('graphics/earth.png').convert_alpha()
        e_rect = e.get_rect(center = (screen_width/2,screen_height/3))
        screen.blit(e,e_rect)

        title_text = str('You Win!!!')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/10)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        title_text = str(f'Your Score: {game.score}')
        title_surface = game_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/2 + screen_height/20)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        button_13.draw()

        pygame.display.flip()
        clock.tick(60)

def lose():
    rul = True
    while rul:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((30, 30, 30))

        title_text = str('You Lose...')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/3)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        title_text = str(f'Your Score: {game.score}')
        title_surface = game_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/2)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        button_13.draw()

        pygame.display.flip()
        clock.tick(60)

def lose2():
    rul = True
    while rul:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill((30, 30, 30))

        title_text = str('You Die...')
        title_surface = title_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/3)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        title_text = str(f'Your Score: {game2.score}')
        title_surface = game_font.render(title_text,True,(255,255,255))
        title_x = int(screen_width/2)
        title_y = int(screen_height/2)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        screen.blit(title_surface,title_rect)

        button_13.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    screen_width = 700
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('graphics/icon.png').convert_alpha()
    pygame.display.set_caption('Earth Invaders')
    pygame.display.set_icon(icon)
    game = Game()
    game2 = Game2()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, game.alien_cooldown)
    ALIENSET = pygame.USEREVENT + 2
    BOSSLASER = pygame.USEREVENT + 3
    CHILDLASER = pygame.USEREVENT + 4
    BOSS = pygame.USEREVENT + 5

    game_font2 = pygame.font.Font('font/pixel.ttf',20)
    game_font = pygame.font.Font('font/pixel.ttf',30)
    title_font = pygame.font.Font('font/pixel.ttf',45)

    button_1 = Button('Start Game',screen_width/2,100,(screen_width/4,450))
    button_2 = Button('Options',screen_width/2,100,(screen_width/4,600))
    button_3 = Button('Credits',screen_width/2,100,(screen_width/4,750))

    button_4 = ButtonBack('Back',screen_width/2,100,(screen_width/4,750))

    button_5 = ButtonRul('Colors',screen_width/2,100,(screen_width/4,550))
    button_7 = ButtonRul('Sound:ON',screen_width/2,100,(screen_width/4,400))
    button_8 = ButtonRul('Sound:OFF',screen_width/2,100,(screen_width/4,400))
    button_9 = ButtonRul('Rules',screen_width/2,100,(screen_width/4,250))

    button_0 = ButtonBack2('Back',screen_width/2,100,(screen_width/4,750))

    button_6 = ButtonGame('Endless',screen_width/2,100,(screen_width/4,575))
    button_10 = ButtonGame('Impossible',screen_width/2,100,(screen_width/4,450))
    button_11 = ButtonGame('Hard',screen_width/2,100,(screen_width/4,325))
    button_12 = ButtonGame('Normal',screen_width/2,100,(screen_width/4,200))

    button_13 = ButtonRestart('Restart',screen_width/2,100,(screen_width/4,550))

    main_menu()