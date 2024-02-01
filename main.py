import pygame
import sys
import random

SCREEN_WIDTH = 768
SCREEN_HEIGHT = 816

class Game:
    def __init__(self)->None:
        self.running  = True
        self.display = pygame.display.get_surface()
        self.screen  = pygame.Surface((256,256))
        self.map = Map()
        self.level = 0

        self.bullets = []
        self.max_shoot_cooldown = 250
        self.shoot_cooldown = 0

        self.enemies = []
        self.spawner= []
        self.max_spawn_cooldown = 1000
        self.spawn_cooldown = 0

        self.walls = []
        
        self.clock = pygame.time.Clock()

        self.info_screen = None

        self.init_game()


    def init_game(self)->None:
        #intializes the game
        self.character = Character(pygame.Vector2(128, 128))
        self.level += 1
        self.next_level(self.level, False)
        delta_time = self.clock.tick(60)
        while self.running:
            self.handle_input()
            if self.info_screen == None: 
                self.time_tick(delta_time)
            self.display_update()
            delta_time = self.clock.tick(60)
            

    def stop_running(self)->None:
        pygame.quit()
        sys.exit()

    def time_tick(self, delta_time: int)->None:

        # level end
        if self.spawner == [] and self.enemies == []:
            self.level += 1
            self.next_level(self.level, False)
            return
            
        # enemy spawn
        self.spawn_cooldown -= delta_time
        if self.spawn_cooldown <= 0:
            if self.spawner != []:
                spawn_index = random.randint(0, len(self.spawner) - 1)
                self.enemies.append(self.spawner.pop(spawn_index))
                self.spawn_cooldown = random.randint(0, self.max_spawn_cooldown)

        # shooting
        self.shoot_cooldown -= delta_time
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = -1

        for enemy in self.enemies[:]:
            enemy.move(self.character,self.walls,self.enemies)
        for bullet in self.bullets[:]:
            if not bullet.move(256, 256, self.walls, self.enemies):
                self.bullets.remove(bullet)
        
        if self.character.get_health() <= 0:
            self.next_level(self.level, True)
        
    def next_level(self, level_number:int, fail:bool)->None:
        #starts next level
        #kaybedince farklı info ekranı çıkıcaksa diye fail_or_next level tuttum  
        #1 next level 0 fail level tekrarını gösteriyor
        self.spawner = []
        self.enemies = []
        self.bullets = []
        if level_number==1:
            for i in range(15):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(EasyEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(EasyEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
        elif level_number==2:
            for i in range (10):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(EasyEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(EasyEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
            for i in range (7):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(MediumEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(MediumEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(MediumEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(MediumEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
        elif level_number==3:
            for i in range (12):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(EasyEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(EasyEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
            for i in range (7):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(MediumEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(MediumEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(MediumEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(MediumEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
            for i in range (8):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(HardEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(HardEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(HardEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(HardEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
        elif level_number==4:
            for i in range (8):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(EasyEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(EasyEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(EasyEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
            for i in range (5):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(MediumEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(MediumEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(MediumEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(MediumEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
            for i in range (12):
                side = random.randint(0, 3)
                if side == 0:
                    self.spawner.append(HardEnemy(pygame.Vector2(-16, random.randint(7 * 16, 9 * 16))))
                elif side == 1:
                    self.spawner.append(HardEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), -16)))
                elif side == 2:
                    self.spawner.append(HardEnemy(pygame.Vector2(256, random.randint(7 * 16, 9 * 16))))
                elif side == 3:
                    self.spawner.append(HardEnemy(pygame.Vector2(random.randint(7 * 16, 9 * 16), 256)))
        if level_number != 5:
            self.walls = self.map.set_map(level_number)
            self.character.set_pos(pygame.Vector2(128, 128))
        self.character.set_health(3)
        self.info_screen = Info(level_number, fail)

    def handle_input(self)->None:
        key_list = pygame.key.get_pressed()  
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                self.stop_running()
            #info screen
            if self.level != 5 and event.type == pygame.KEYDOWN and self.info_screen != None:
                if event.key == pygame.K_SPACE:
                    self.info_screen = None

        if self.info_screen != None:
            return
        
        # movement
        move_direction = pygame.Vector2(0, 0)
        if key_list[pygame.K_w]:
            move_direction += pygame.Vector2(0, -1)     
        if key_list[pygame.K_a]:
            move_direction += pygame.Vector2(-1, 0)
        if key_list[pygame.K_s]:
            move_direction += pygame.Vector2(0, 1)
        if key_list[pygame.K_d]:
            move_direction += pygame.Vector2(1, 0)
        if move_direction.length() != 0:
            self.character.move(move_direction.normalize(),256,256,self.walls)

        # shooting
        if self.shoot_cooldown == -1:
            shoot_direction = pygame.Vector2(0, 0)
            if key_list[pygame.K_UP]:
                shoot_direction += pygame.Vector2(0, -1)
            if key_list[pygame.K_DOWN]:
                shoot_direction += pygame.Vector2(0, 1)
            if key_list[pygame.K_LEFT]:
                shoot_direction += pygame.Vector2(-1, 0)
            if key_list[pygame.K_RIGHT]:
                shoot_direction += pygame.Vector2(1, 0)
            if shoot_direction.length() != 0:
                self.bullets.append(self.character.shoot(shoot_direction.normalize()))
                self.shoot_cooldown = self.max_shoot_cooldown
    
    def display_update(self)->None:
        pygame.draw.rect(self.screen, pygame.Color(242,188,82),(0,0,256,256))
        self.map.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.character.draw(self.screen)

        scaled_screen = pygame.Surface((768, 768))
        pygame.transform.scale(self.screen, (768, 768), scaled_screen)
        self.display.blit(scaled_screen, (0, 0))

        # Drawing Hearts bottom
        pygame.draw.rect(self.display, pygame.Color(242,188,82), (0,SCREEN_WIDTH,SCREEN_WIDTH,64))
        scaled_heart = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.transform.scale(images["heart"], (48, 48), scaled_heart)
        for i in range(self.character.get_health()):
            self.display.blit(scaled_heart, (i * 48, 768))

        if self.info_screen != None:
            self.info_screen.draw(self.display)
        pygame.display.flip()

class Entity:
    def __init__(self,pos:pygame.Vector2)->None:
        self.image=None
        self.pos=pos
        self.rect=pygame.Rect(0,0,0,0)
        self.speed = 0

    def draw(self,surface:pygame.Surface)->None:
        surface.blit(self.image,self.rect)
        
    def move(self,direction:pygame.Vector2,screen_width:int,screen_height:int,walls:list)->None:
        direction = direction * (self.speed / 100)
        new_x = self.pos.x + direction.x
        new_y = self.pos.y + direction.y
        for wall in walls:
            l = wall.stop_entity(self.rect, direction)
            if l[0]:
                new_x = self.pos.x
            if l[1]:
                new_y = self.pos.y
        if 0 < new_x < screen_width - self.rect.width:
            self.pos.x = new_x
        if 0 < new_y < screen_height - self.rect.height:
            self.pos.y = new_y
        self.rect = pygame.Rect(self.pos, (self.rect.width, self.rect.height))

    def get_rect(self)->pygame.Rect:
        return self.rect

    def get_pos(self)->pygame.Vector2:
        return self.pos
        
    def set_pos(self,pos:pygame.Vector2)->None:
        self.pos=pos
        self.rect = pygame.Rect(self.pos, (self.rect.width, self.rect.height))

class Bullet(Entity):
    def __init__(self, pos:pygame.Vector2, direction:pygame.Vector2) -> None:
        super().__init__(pos)
        self.image = images["bullet"]
        self.pos = pos
        self.rect = pygame.Rect(self.pos,(4,4))
        self.direction = direction 
        self.speed=200
        
    def move(self,screen_width:int,screen_height:int,walls:list, enemies:list)->None:
        super().move(self.direction, screen_width, screen_height, walls)
        if self.screen_collide(screen_width, screen_height):
            return False
        if self.hit_wall(walls):
            return False
        if self.hit_enemy(enemies):
            return False
        return True
        
    def screen_collide(self,screen_width:int,screen_height:int)->bool:
        if self.rect.x<3 or self.rect.x+self.rect.width>screen_width-3 or self.rect.y<3 or self.rect.y+self.rect.height>screen_height-3:
            return True

    def hit_enemy(self, enemies:list) -> bool:
        for enemy in enemies[:]:  # Iterate over a copy of the list to safely modify it
            enemy_rect = enemy.get_rect()
            if self.check_collision(enemy_rect):  # Check for collision using entity rects
                if enemy.decrease_health():  # Remove the enemy from the list
                    enemies.remove(enemy)
                return True
    
    def check_collision(self, entity_rect:pygame.Rect) -> bool:
        # Check for collision between the bullet and an entity rectangle
        return self.rect.colliderect(entity_rect)
    
    def draw(self,surface:pygame.Surface)->None:
        surface.blit(self.image, self.rect)

    def hit_wall(self,walls:list)->bool:
        for wall in walls:
            if wall.collide(self.rect):
                return True
        return False

class Character(Entity):
    def __init__(self, pos) -> None:
        super().__init__(pos)
        self.image = images["character"]
        self.pos = pos
        self.rect = pygame.Rect(self.pos, (16, 16))
        self.speed = 100
        self.health = 3

    def draw(self,surface: pygame.Surface)->None:
        surface.blit(self.image, self.rect)

    def shoot(self,direction:pygame.Vector2)->Bullet:
        bullet = Bullet(self.pos.copy() + pygame.Vector2(self.rect.width / 2, self.rect.height / 2), direction)
        return bullet

    def decrease_health(self)->None:
        self.health -= 1

    def die(self)->None:
        self.health = 0

    def get_health(self)->int:
        return self.health

    def set_health(self, health:int)->None:
        self.health = health
class Enemy(Entity):
    def __init__(self, pos:pygame.Vector2) -> None:
        super().__init__(pos)
        self.image=pygame.Surface((16,16))
        self.pos = pos
        self.rect=pygame.Rect(pos,(16,16))
        self.speed = 100
        self.health = 1
        
    def move(self, character:Character, walls:list, enemies:list)->None:
        character_pos = character.get_pos()
        direction = self.determine_direction(character_pos) * (self.speed / 100)
        for enemy in enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                avoid_direction = pygame.Vector2(self.pos - enemy.pos).normalize()
                # Attempts to move in the new avoid direction
                direction = direction + avoid_direction * (self.speed / 100)
        for wall in walls:
            l = wall.stop_entity(self.rect, direction)
            if l[0]:
                direction.x = 0
            if l[1]:
                direction.y = 0
        if direction.length() != 0:
            direction = direction.normalize() * (self.speed / 100)
        self.pos += direction
        self.rect = pygame.Rect(self.pos, (self.rect.width, self.rect.height))
        
    def determine_direction(self, character_pos:pygame.Vector2)->pygame.Vector2:
        direction = (character_pos - self.pos).copy()
        direction.normalize_ip()
        return direction
    
    def hit_player(self, character_rect:pygame.Rect)->bool:
        return self.rect.colliderect(character_rect)

    def draw(self, surface:pygame.Surface)->None:
        surface.blit(self.image, self.rect)
        
    def decrease_health(self) -> bool:
        self.health -= 1
        return self.health <= 0
        
    def get_rect(self)->pygame.Rect:
        return self.rect
class EasyEnemy(Enemy):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pos)
        self.image = images["enemy1"]
        self.speed = 80

    def move(self, character:Character, walls:list, enemies:list) -> None:
        super().move(character, walls, enemies)
        if self.hit_player(character.get_rect()):
            character.decrease_health()
            enemies.remove(self)
            
        
class MediumEnemy(Enemy):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pos)
        self.image = images["enemy2"]
        self.speed = 75
        self.health = 2

    def move(self, character:Character, walls:list, enemies:list) -> None:
        super().move(character, walls, enemies)
        if self.hit_player(character.get_rect()):
            character.decrease_health()
            enemies.remove(self)

class HardEnemy(Enemy):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pos)
        self.image = images["enemy3"]
        self.speed = 100

    def move(self, character:Character, walls:list, enemies:list) -> None:
        super().move(character, walls, enemies)
        if self.hit_player(character.get_rect()):
            character.die()
            enemies.remove(self)
           

class Tile:
    def __init__(self, pos:pygame.Vector2) -> None:
        self.image = None
        self.rect = pygame.Rect((pos), (16, 16))
    def draw(self,surface:pygame.Surface)->None:
        surface.blit(self.image, self.rect)
class Wall(Tile):
    def __init__(self, pos:pygame.Vector2) -> None:
        super().__init__(pos)
        self.image = images["wall"]

    def stop_entity(self, entity_rect:pygame.Rect,direction:pygame.Vector2)->list:
        stop_x=False
        stop_y=False
        if self.rect.y-entity_rect.height<entity_rect.y<self.rect.y+self.rect.height:
            if direction.x > 0 and entity_rect.x < self.rect.x and entity_rect.x + direction.x + entity_rect.width > self.rect.x:
                stop_x=True
            if direction.x < 0 and entity_rect.x > self.rect.x and entity_rect.x + direction.x < self.rect.x + self.rect.width:
                stop_x=True
        if self.rect.x-entity_rect.width<entity_rect.x<self.rect.x+self.rect.width:
            if direction.y > 0 and entity_rect.y < self.rect.y and entity_rect.y + direction.y + entity_rect.height > self.rect.y:
                stop_y=True
            if direction.y < 0 and entity_rect.y > self.rect.y and entity_rect.y + direction.y < self.rect.y + self.rect.height:
                stop_y=True
        return [stop_x,stop_y]
    
    def collide(self, entity_rect:pygame.Rect)->bool:
        return self.rect.inflate(4,4).colliderect(entity_rect)
    
class Ground(Tile):
    def __init__(self, pos:pygame.Vector2) -> None:
        super().__init__(pos)
        self.image = images["ground"]

class Info:
    def __init__(self,  level_number: int, fail: bool) -> None:
        self.image = None
        self.rect = (0, 0, 16, 16)
        self.fail = fail
        self.level_number = level_number

    def draw(self,surface:pygame.Surface)->None:
        if not self.fail:
            if self.level_number == 1:
                self.image=images["welcome"]
            elif self.level_number == 2:
                self.image=images["level2"]
            elif self.level_number == 3:
                self.image=images["level3"]
            elif self.level_number == 4:
                self.image=images["level4"]
        else:
            self.image=images["fail"]
        if self.level_number==5:
            self.image=images["finish"]
        scaled_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT), scaled_image)
        surface.blit(scaled_image, self.rect)

class Map:
    def __init__(self) -> None:
        self.tile_list = [[Ground((i * 16, j * 16)) for i in range(16)] for j in range(16)]
    def draw(self,surface:pygame.Surface)->None:
        for i in range(16):
            for j in range(16):
                self.tile_list[i][j].draw(surface)

    def set_map(self,level_number:int)->list:
 
        level_str = self.level_strings(level_number)
        level_matrix = self.making_level_matrix(level_str)
        walls = []
        for i in range(16):
            for j in range(16):
                if level_matrix[i][j] == 1:
                    new_wall = Wall((j*16,i*16))
                    self.tile_list[i][j] = new_wall
                    walls.append(new_wall)
                else :
                    self.tile_list[i][j] = Ground((j*16,i*16))
        return walls 
    
    def making_level_matrix(self,level:str)->list:
        rows = level.strip().split("\n") 
        matrix = []
        for row in rows:
            values = list(map(int, row.split(',')))
            matrix.append(values)
        return matrix
    
    def level_strings(self,level_number:int)->str:
        level_1 = """
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
"""
        level_2 ="""
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
"""
        level_3 ="""
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
"""
        level_4 = """
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1
1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1
1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1
1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1
1,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1
1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1
"""
        if level_number == 1:
            return level_1
        elif level_number == 2:
            return level_2
        elif level_number == 3:
            return level_3
        elif level_number == 4:
            return level_4

#images
pygame.init()
pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("images/icon2.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("GROUP-14-Project")
images=dict()
images["ground"] = pygame.image.load("images/tile0.png").convert_alpha()
images["wall"] = pygame.image.load("images/tile6.png").convert_alpha()
images["bullet"] = pygame.image.load("images/bullet.png").convert_alpha()
images["character"] = pygame.image.load("images/player5.png").convert_alpha()
images["enemy1"] = pygame.image.load("images/enemy1_0.png").convert_alpha()
images["enemy2"] = pygame.image.load("images/enemy2_0.png").convert_alpha()
images["enemy3"] = pygame.image.load("images/enemy3_0.png").convert_alpha()
images["level2"] = pygame.image.load("images/level2.png").convert_alpha()
images["level3"] = pygame.image.load("images/level3.png").convert_alpha()
images["level4"] = pygame.image.load("images/level4.png").convert_alpha()
images["welcome"] = pygame.image.load("images/welcome.png").convert_alpha()
images["fail"] = pygame.image.load("images/fail.png").convert_alpha()
images["finish"] = pygame.image.load("images/finish.png").convert_alpha()
images["heart"]=pygame.image.load("images/heart.png").convert_alpha()

game = Game()