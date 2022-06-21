import pygame, sys
from player import Player
import obstacles
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        player_sprite = Player((screen_width/2,screen_height - 10),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        self.level = 1
        self.lives = 3
        self.live_icon = pygame.image.load('graphics/player.png').convert_alpha()
        self.score = 0
        self.font = pygame.font.Font('font/pixel.ttf', 25)
        self.level_font = pygame.font.Font('font/pixel.ttf', 35)
        self.title_font = pygame.font.Font('font/pixel.ttf', 50)
        
        self.shape = obstacles.shape
        self.block_size = 3
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num *(screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 11, y_start = 750)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 7, cols = 7)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint (1500,1500)

    def death(self):
        pygame.quit()
        sys.exit()

    def create_obstacle(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacles.Block(self.block_size,(247, 74, 74),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_distance = 85,y_distance = 80, x_offset = 27, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index <= 1: alien_sprite = Alien('3',x,y)
                elif 2 <= row_index <= 3: alien_sprite = Alien('2',x,y)
                else: alien_sprite = Alien('1',x,y)
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

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']),screen_width))
            self.extra_spawn_time = randint (1000,2000)

    def collision_checks(self):
        global killable
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                aliens_hit_check = pygame.sprite.spritecollide(laser,self.aliens,False)
                if aliens_hit_check:
                    for alien in aliens_hit_check:
                        if alien.enemy_lives == 1:
                            killable = True
                        else:
                            killable = False
                            alien.enemy_lives -= 1
                        print(alien.enemy_lives)
                    laser.kill()

                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,killable)
                if aliens_hit:
                    for alien in aliens_hit:
                        if killable == True:
                            self.score += alien.value
                        print(alien.enemy_lives)
                    laser.kill()


                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 50
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.death()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    self.death()

    def display_lives(self):
            lives_surf = self.font.render(f'{self.lives - 1}x',False,'white')
            screen.blit(lives_surf,(565,25))
            screen.blit(self.live_icon,(625,10))

    def display_level(self):
        level_surf = self.font.render(f'Level {self.level}',False,'white')
        level_rect = level_surf.get_rect(topleft = (325,25))
        screen.blit(level_surf,level_rect)

    def display_score(self):
        score_surf = self.font.render(f'Score:{self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (25,25))
        screen.blit(score_surf,score_rect)

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()

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
        self.display_lives()
        self.display_level()
        self.display_score()

if __name__ == '__main__':
    pygame.init()
    screen_width = 700
    screen_height = 900
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('graphics/icon.png').convert_alpha()
    pygame.display.set_caption('Earth Invaders')
    pygame.display.set_icon(icon)
    killable = False
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shot()

        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)