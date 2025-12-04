# ============================================================================
# FILE: character.py - PLAYER CHARACTER CLASS
# ============================================================================
# PURPOSE:
#   Defines the Character class representing the player in the game.
#   Handles:
#   - Character movement (WASD / Arrow keys) with collision detection
#   - Animation frame switching based on movement direction
#   - Camera follow system
#   - Input processing
#
# DEPENDENCIES:
#   - pygame: Sprite and rendering
#   - gamesetting: Game configuration and tile sizes
# ============================================================================

#This is character.py - defines the Character class for the Bomberman game
import pygame
import gamesetting as gs

# ============================================================================
# CLASS: Character - Player sprite with movement, animation, and collision
# ============================================================================
class Character(pygame.sprite.Sprite):
    def __init__(self, game, image_dict, group, row_num, col_num, size):
        """
        CONSTRUCTOR - Initialize the player character
        
        PARAMETERS:
        - game: Game object reference for camera updates and collision checks
        - image_dict: Dictionary of animation frames indexed by direction (walk_left, walk_right, etc.)
        - group: Pygame sprite group for rendering
        - row_num: Starting grid row position
        - col_num: Starting grid column position
        - size: Tile size in pixels (64px)
        
        INITIALIZATION STEPS:
        1. Call parent Sprite constructor to add to sprite group
        2. Store references to game and grid position
        3. Calculate pixel position from grid position
        4. Initialize animation state and frame tracking
        5. Create hitbox (collision rectangle) smaller than visual sprite
        """
        super().__init__(group)
        self.GAME = game

        # Level matrix position (in grid tiles)
        self.row_num = row_num
        self.col_num = col_num
        self.size = size

        # CHARACTER WORLD POSITION (in pixels, with Y offset for visual alignment)
        self.x = self.col_num * self.size 
        self.y = (self.row_num * self.size) + gs.Y_OFFSET

        # CHARACTER ATTRIBUTES
        self.alive = True
        self.speed = 3  # Pixels per frame when moving
        self.bomb_limit = 1


        # CHARACTER ACTION/ANIMATION STATE
        self.action = "walk_left"  # Current animation direction

        # Bomb Planted
        self.bomb_planted = 0


        # ANIMATION FRAME TRACKING
        self.index = 0  # Current frame in animation sequence
        self.anim_time = 50  # Milliseconds between frame updates
        self.anim_time_set = pygame.time.get_ticks()  # Last frame switch time
        self.image_dict = image_dict  # Dictionary of all animation sequences
        self.image = self.image_dict[self.action][self.index]

        # HITBOX SETUP for collision detection
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.inflate_ip(-20, -20)  # Shrink hitbox by 20px (10 on each side)
        self.offset = 10  # Offset to keep the hitbox centered inside the image

    def input(self, events):
        """
        INPUT HANDLER - Process keyboard input for player movement
        
        HANDLES:
        - Event loop for QUIT and ESCAPE events (passed from main)
        - Continuous key polling for smooth movement (WASD / Arrow keys)
        
        MOVEMENT CONTROLS:
        - W / UP ARROW: Move up (walk_up animation)
        - A / LEFT ARROW: Move left (walk_left animation)
        - S / DOWN ARROW: Move down (walk_down animation)
        - D / RIGHT ARROW: Move right (walk_right animation)
        
        NOTES:
        - Events are passed from Bomberman.input() via Game.input()
        - Continuous polling with pygame.key.get_pressed() ensures smooth movement
        - Each movement calls self.move() which handles collision detection
        """
        # Process events passed from main (QUIT/ESCAPE)
        for event in events:
            if event.type == pygame.QUIT:
                self.GAME.MAIN.running = False  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.GAME.MAIN.running = False
                elif event.key == pygame.K_SPACE:
                    row, col, = ((self.rect.centery - gs.Y_OFFSET)//gs.SIZE, self.rect.centerx // gs.SIZE)
                    if self.GAME.level_matrix[row][col] == "_" and self.bomb_planted < self.bomb_limit:
                        Bomb(self.GAME, self.GAME.ASSETS.bomb["bomb"], self.GAME.groups["bomb"], row, col, gs.SIZE)  
                        print(self.bomb_planted)

        # Continuous key polling for smooth movement
        keys_pressed = pygame.key.get_pressed() 
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.move("walk_right")
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.move("walk_left")
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.move("walk_up")
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.move("walk_down")

    def update(self):
        """
        UPDATE - Update sprite state each frame (currently empty as movement is
        handled in move() and animation in animate())
        """
        pass

    def draw(self, window, x_offset=0, y_offset=0):
        """
        DRAW - Render the character sprite to screen with camera offset applied
        
        PARAMETERS:
        - window: pygame.Surface to draw on (the game screen)
        - x_offset: Horizontal camera offset (subtracts from x coordinate)
        - y_offset: Vertical camera offset (subtracts from y coordinate)
        
        NOTES:
        - Camera offsets shift the character position, creating the camera follow effect
        - Commented debug code shows how to draw the hitbox for debugging
        """
        window.blit(self.image, (self.x - x_offset, self.y - y_offset))
        #pygame.draw.rect(window, gs.RED, self.rect, 1)

        # Optional: Uncomment to see the red hitbox for debugging
        # debug_rect = self.rect.copy()
        # debug_rect.x -= offset
        # pygame.draw.rect(window, gs.RED, debug_rect, 1)

    def animate(self, action):
        """
        ANIMATE - Switch animation frame based on elapsed time
        
        PARAMETERS:
        - action: Current movement direction (walk_left, walk_right, walk_up, walk_down)
        
        LOGIC:
        1. Check if enough time (anim_time ms) has passed since last frame switch
        2. If yes: advance to next frame in the animation sequence
        3. Loop back to frame 0 when reaching the end of the sequence
        4. Update the current image and reset the timer
        
        NOTES:
        - Different directions have different animation sequences (defined in gamesetting.PLAYER)
        - Each direction typically has 3 frames for walking animation
        - This creates smooth sprite animation during movement
        """
        if pygame.time.get_ticks() - self.anim_time_set > self.anim_time:
            self.index += 1
            if self.index == len(self.image_dict[action]):
                self.index = 0

            #self.index = self.index % len(self.image_dict[action])
            self.image = self.image_dict[action][self.index]
            self.anim_time_set = pygame.time.get_ticks()

    def check_collision(self):
        """
        CHECK_COLLISION - Detect collisions with blocks in the game world
        
        RETURNS:
        - True: Character is colliding with a solid (non-passable) block
        - False: No collision detected
        
        COLLISION LOGIC:
        1. Get all hard blocks the character's hitbox is touching
        2. Get all soft blocks the character's hitbox is touching
        3. Combine both lists
        4. Check each block's 'passable' attribute
        5. Return True if any block has passable=False (solid wall)
        
        NOTES:
        - Uses pygame.sprite.spritecollide() for efficient collision detection
        - Hitbox is smaller than the visual sprite (inflated -20px) for better gameplay feel
        - Used in move() to prevent character from walking through walls
        """
        # 1. Get a list of all blocks we are touching
        hard_hits = pygame.sprite.spritecollide(self, self.GAME.groups["hard_block"], False)
        soft_hits = pygame.sprite.spritecollide(self, self.GAME.groups["soft_block"], False)
        all_hits = hard_hits + soft_hits

        # 2. Check each block to see if it is passable
        for block in all_hits:
            if hasattr(block, 'passable') and block.passable == False:
                return True  # We hit a solid wall!
            
        return False  # No solid collisions found


    def move(self, action):
        """
        MOVE - Handle character movement with collision detection
        
        PARAMETERS:
        - action: Direction to move (walk_left, walk_right, walk_up, walk_down)
        
        MOVEMENT LOGIC (Two-phase collision detection):
        1. PHASE 1 - Move horizontally (X axis)
           - Apply horizontal velocity (dx) based on action direction
           - Update hitbox x position
           - Check for collisions; undo movement if collision detected
        
        2. PHASE 2 - Move vertically (Y axis)
           - Apply vertical velocity (dy) based on action direction
           - Update hitbox y position
           - Check for collisions; undo movement if collision detected
        
        3. FINAL UPDATES
           - Animate the sprite based on the current action
           - Update camera position to follow the character
        
        WHY TWO PHASES?
        - Allows player to slide along walls (move diagonally if one axis is blocked)
        - More forgiving gameplay feel compared to complete rejection on collision
        
        NOTES:
        - self.speed = 3 pixels per frame
        - self.offset = 10 pixels to center the hitbox inside the sprite
        - Camera follows smoothly with interpolation (lerp) defined in Game
        """
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
        
        # Update camera based on the center of the player (x and y)
        self.GAME.update_camera(self.rect.centerx, self.rect.centery)

class Bomb(pygame.sprite.Sprite):
    def __init__(self,game, image_list, group, row_num, col_num, size):
        super().__init__(group)
        self.GAME = game


        # Level matrix position (in grid tiles)
        self.row = row_num
        self.col = col_num

        # Coordinates
        self.size = size
        self.x = self.col * self.size
        self.y = (self.row * self.size) + gs.Y_OFFSET

        # Bomb Attributes
        self.bomb_counter = 1
        self.bomb_timer = 12    
        self.passable = True  # Bombs are passable until they explode

        # Image
        self.index = 0
        self.image_list = image_list
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Animation Settings
        self.anim_length = len(self.image_list)
        self.anim_frame_time = 200  # milliseconds per frame
        self.anim_timer = pygame.time.get_ticks()

        # Insert into level matrix
        self.insert_bomb_into_grid()

    def update(self):
        # Keep the collision rect in sync with the bomb's fixed world position.
        # Do NOT change self.x/self.y here; bombs are stationary after placement.
        self.animation()
        self.planted_bomb_player_collision()
        if self.bomb_counter == self.bomb_timer:
            self.explode()



        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, window, x_offset=0, y_offset=0):
        """
        DRAW - Render the bomb with camera offsets applied.

        PARAMETERS:
        - window: pygame.Surface
        - x_offset: horizontal camera offset
        - y_offset: vertical camera offset

        NOTES:
        - Use the bomb's stored world coordinates (self.x/self.y) so the bomb
          remains fixed in the world even if the player moves or the camera scrolls.
        - Keep rect synced in update(); draw only uses self.x/self.y for rendering.
        """
        window.blit(self.image, (int(self.x) - int(x_offset), int(self.y) - int(y_offset)))
    def insert_bomb_into_grid(self):
        """Add the bomb object to the level matrix"""
        self.GAME.level_matrix[self.row][self.col] = self
        self.GAME.PLAYER.bomb_planted += 1
        

    def animation(self):
        if pygame.time.get_ticks() - self.anim_timer >= self.anim_frame_time:
            self.index += 1
            self.index = self.index % self.anim_length
            self.image = self.image_list[self.index]
            self.anim_timer = pygame.time.get_ticks()
            self.bomb_counter += 1

    def remove_bomb_from_grid(self):
        """Remove the bomb object from the level matrix"""
        self.GAME.level_matrix[self.row][self.col] = "_"
        self.GAME.PLAYER.bomb_planted += 1

    def explode(self):
        """Destroy the bomb and remove from the level matrix"""    
        self.kill()
        self.remove_bomb_from_grid()

    def planted_bomb_player_collision(self):
        if not self.passable:
            return
        if not self.rect.colliderect(self.GAME.PLAYER):
            self.passable = False


    def __repr__(self):
        return "'!'"         
            