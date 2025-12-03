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
        # --- HITBOX SETUP ---
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.inflate_ip(-20,-20)
        # Offset to keep the hitbox centered inside the image
        # Bagong Add ito. 
        self.offset = 10

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

    def draw(self, window, offset=0):
        # `offset` is optional to keep compatibility with other objects
        # that are drawn without camera offset. Default is 0 (no offset).
        window.blit(self.image, (self.x - offset, self.y - offset))
        #pygame.draw.rect(window, gs.RED, self.rect, 1)

        # Optional: Uncomment to see the red hitbox for debugging
        # debug_rect = self.rect.copy()
        # debug_rect.x -= offset
        # pygame.draw.rect(window, gs.RED, debug_rect, 1)

    def animate(self,action):
        """Switches between images in order to animate movement"""
        if pygame.time.get_ticks() - self.anim_time_set > self.anim_time:
            self.index += 1
            if self.index == len(self.image_dict[action]):
                self.index = 0

            #self.index = self.index % len(self.image_dict[action])
            self.image = self.image_dict[action][self.index]
            self.anim_time_set = pygame.time.get_ticks()

    def check_collision(self):
        """
        Checks for collisions with Hard and Soft blocks.
        Returns TRUE if we hit a block that is NOT passable.
        """
        # 1. Get a list of all blocks we are touching
        hard_hits = pygame.sprite.spritecollide(self, self.GAME.groups["hard_block"], False)
        soft_hits = pygame.sprite.spritecollide(self, self.GAME.groups["soft_block"], False)
        all_hits = hard_hits + soft_hits

        # 2. Check each block to see if it is passable
        for block in all_hits:
            if hasattr(block, 'passable') and block.passable == False:
                return True # We hit a solid wall!
            
        return False # No solid collisions found


    def move(self, action):
        if not self.alive:
            return
        
        if action != self.action:
            self.action = action
            self.index = 0

        dx = 0
        dy = 0

        if action == "walk_left":
            dx = -self.speed
        elif action == "walk_right":
            dx = self.speed
        elif action == "walk_up":
            dy = -self.speed
        elif action == "walk_down":
            dy = self.speed

        # --- PHASE 1: MOVE X-AXIS ---
        self.x += dx
        self.rect.x = int(self.x + self.offset)
        
        # Check collision using the new passable-aware logic
        if self.check_collision():
            self.x -= dx # Undo X movement
            self.rect.x = int(self.x + self.offset)

        # --- PHASE 2: MOVE Y-AXIS ---
        self.y += dy
        self.rect.y = int(self.y + self.offset)
        
        # Check collision using the new passable-aware logic
        if self.check_collision():
            self.y -= dy # Undo Y movement
            self.rect.y = int(self.y + self.offset)

        # --- FINAL UPDATES ---
        self.animate(action)   
        
        # Update Camera based on the center of the player
        self.GAME.update_x_camera_offset_player_position(self.rect.centerx)                 
