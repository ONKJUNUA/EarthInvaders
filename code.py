import pygame, sys
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
        self.level = 1
        self.lives = 4
        self.dmg = 1
        self.speed_charge = 3
        self.bullet_charge = 3
        self.damage_charge = 3
        self.live_icon = pygame.image.load('graphics/player.png').convert_alpha()
        self.score = 0
        self.font = pygame.font.Font('font/pixel.ttf', 25)
        self.level_font = pygame.font.Font('font/pixel.ttf', 35)
        self.title_font = pygame.font.Font('font/pixel.ttf', 50)
        
        self.alien_cooldown = 800
        self.boss_cooldown = 1000
        self.shape = obstacles.shape
        self.block_size = 3
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num *(screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 12, y_start = 770)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 7, cols = 7)
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
        pygame.quit()
        sys.exit()

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

    def one_alien(self, x = 450, y = 949):
        if self.level <= 11:
            alien_sprite = Alien(str(0+self.level), x, y)
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
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, self.level + 5, screen_height)
            self.alien_lasers.add(laser_sprite)
        
    def boss_shot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = BossLaser(random_alien.rect.center, self.level - 3, screen_height)
            self.alien_lasers.add(laser_sprite)

    def child_shot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = ChildLaser(random_alien.rect.center, self.level - 3, screen_height)
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
                            self.score += 100
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 100
                    if self.level >= 9:
                        self.choice = randint(1,10)
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
        attack_type = randint(1,5)
        if attack_type == 1:
            pygame.time.set_timer(BOSSLASER, self.boss_cooldown, loops = 5)
        if attack_type == 2:
            self.fake_alien(rows = 2, cols = 8)
        if attack_type == 3:
            pygame.time.set_timer(CHILDLASER, self.boss_cooldown, loops = 1)
        if attack_type == 4:
            pass
        if attack_type == 5:
            if self.dmg == 4:
                self.dmg -= 1
            else: self.dmg += 1

    def next_level(self):
        if not self.aliens.sprites():
            if self.level <= 10:
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

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, game.alien_cooldown)
    ALIENSET = pygame.USEREVENT + 2
    BOSSLASER = pygame.USEREVENT + 3
    CHILDLASER = pygame.USEREVENT + 4
    BOSS = pygame.USEREVENT + 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                if game.level <= 10: game.alien_shot()
            if event.type == BOSSLASER: game.boss_shot()
            if event.type == CHILDLASER: game.child_shot()

            if event.type == ALIENSET:
                if game.level <= 10: game.alien_setup(rows = 7, cols = 7)
                else: 
                    game.boss_setup()
                    pygame.time.set_timer(BOSS, 2000)

            if event.type == BOSS:
                game.boss_attack()

        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)