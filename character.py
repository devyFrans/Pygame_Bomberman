#This is character.py - defines the Character class for the Bomberman game
import pygame
import gamesetting as gs

class Character(pygame.sprite.Sprite):
    def __init__(self, game,image_dict, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game

        # Level matrix position
        self.row_num = row_num
        self.col_num = col_num
        self.size = size



        # CHARACTER POSITION
        self.x = self.col_num * self.size 
        self.y = (self.row_num * self.size) + gs.Y_OFFSET

        # CHARACTER ATTRIBUTES 
        self.alive = True
        self.speed = 3          #default is 3

        # CHARACTER ACTION
        self.action = "walk_left"

        # CHARACTER DISPLAY
        self.index = 0
        self.anim_time = 50
        self.anim_time_set = pygame.time.get_ticks()
        self.image_dict = image_dict
        self.image = self.image_dict[self.action][self.index]

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.inflate_ip(-20,-20)

    def input(self):
        for event in pygame.event.get():
            # CHECK IF RED CROSS IS CLICKED
            if event.type == pygame.QUIT:
                self.GAME.MAIN.running = False  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.GAME.MAIN.running = False

        keys_pressed = pygame.key.get_pressed() 
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.move("walk_right")
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move("walk_left")

        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.move("walk_up")

        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.move("walk_down")


        # UPDATE THE CHARACTER POSITION
        #self.rect.topleft = (self.x, self.y)          

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(window, gs.RED, self.rect, 1)

    def animate(self,action):
        """Switches between images in order to animate movement"""
        if pygame.time.get_ticks() - self.anim_time_set > self.anim_time:
            self.index += 1
            if self.index == len(self.image_dict[action]):
                self.index = 0

            #self.index = self.index % len(self.image_dict[action])
            self.image = self.image_dict[action][self.index]
            self.anim_time_set = pygame.time.get_ticks()

    def move(self,action):
       
        if not self.alive:
            return
        
        if action != self.action:
            self.action = action
            self.index = 0

        old_x = self.x
        old_y = self.y

        direction = {
            "walk_left": -self.speed, 
            "walk_right": self.speed, 
            "walk_up": -self.speed, 
            "walk_down": self.speed
        }

        if action in ["walk_left", "walk_right"]:
            self.x += direction[action]
        elif action in ["walk_up", "walk_down"]:
            self.y += direction[action]        

        offset = 10
        self.rect.topleft = (self.x + offset, self.y + offset)

        hit_hard = pygame.sprite.spritecollideany(self, self.GAME.groups["hard_block"])
        hit_soft = pygame.sprite.spritecollideany(self, self.GAME.groups["soft_block"])   

        if hit_hard or hit_soft:
            self.x = old_x
            self.y = old_y
            self.rect.topleft = (self.x + offset,  self.y + offset) # Reset rect to old safe spot

        self.animate(action)   

                    
        """ SNAP THE PLAYER TO GRID COORDINATES MAKING NAVIGATOR EASIER"""
        self.snap_to_grid(action)

        # Check if x, y posotion is within game area
        self.play_area_restriction(64,(gs.COLS - 1 ) * 64, gs.Y_OFFSET + 64, ((gs.ROWS -1 ) * 64) + gs.Y_OFFSET )   
        

    def snap_to_grid(self,action):
        """ SNAP THE PLAYER TO GRID COORDINATES MAKING NAVIGATOR EASIER"""
        x_pos = self.x % gs.SIZE
        y_post = (self.y - gs.Y_OFFSET) % gs.SIZE

        if action in ["walk_up","walk_down"]:
            if x_pos <= 12:
                self.x = self.x - x_pos
            if x_pos >= 52:
                self.x = self.x + (gs.SIZE - x_pos)
        elif action in ["walk_left", "walk_right"]:
            if y_post <= 12:
                self.y = self.y - y_post
            if y_post >= 52:
                self.y = self.y + (gs.SIZE - y_post)

    def play_area_restriction(self, left_x, right_x, top_y, bottom_y):
        """ Check player coords to ensure remains within play area """
        if self.x  < left_x:
            self.x = left_x
        elif self.x > right_x:
            self.x = right_x
        elif self.y < top_y:
            self.y = top_y
        elif self.y > bottom_y:
            self.y = bottom_y                    
