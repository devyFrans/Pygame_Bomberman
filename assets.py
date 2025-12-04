#This is assets.py - handles loading and managing game assets for Bomberman

import pygame
import gamesetting as gs

class Assets:
    def __init__(self):
        # DO NOT SCALE the sprite sheet if it's already the correct size (325x257)
        # Assuming "owncreation.png" is the 325x257 image
        self.sprite_sheet = self.load_sprite_sheet("images", "owncreation.png") # Removed hardcoded size | THIS IS FOR CHARACTER
        #self.sprite_sheet = self.load_sprite_sheet("images","BombermanNES2-tiles.png")
        self.player_char = self.load_sprite_range(
            gs.PLAYER, 
            self.sprite_sheet, 
            row=gs.SPRITE_HEIGHT, # Use new constants
            col=gs.SPRITE_WIDTH, 
            width=gs.SPRITE_WIDTH, 
            height=gs.SPRITE_HEIGHT,
            resize=True # Added resize to scale it up to a visible game size, e.g., 32x32
        )

        #self.sprite_sheet = self.load_sprite_sheet("images", "BombermanPCE-tiles.png") # Removed hardcoded size
        self.sprite_sheet = self.load_sprite_sheet("images", "sprite_sheet (1).png") # Removed hardcoded size | THIS IS FOR BLOCKS
        self.hard_block = self.load_sprite_range(
            gs.HARD_BLOCK, 
            self.sprite_sheet, 
            row=gs.TILE_HEIGHT, 
            col=gs.TILE_WIDTH, 
            width=gs.TILE_WIDTH - 1,
            height=gs.TILE_HEIGHT,
            resize=True            
        )

        self.soft_block = self.load_sprite_range(
            gs.SOFT_BLOCK, # Use the coordinates defined in gamesetting
            self.sprite_sheet, # Use the same sprite sheet
            row=gs.TILE_HEIGHT, 
            col=gs.TILE_WIDTH, 
            width=gs.TILE_WIDTH - 1,
            height=gs.TILE_HEIGHT,
            resize=True            
        )

        self.sprite_sheet = self.load_sprite_sheet("images", "bomb.png")# THIS IS FOR BOMB
        self.bomb = self.load_sprite_range(
            gs.BOMB, # Use the coordinates defined in gamesetting
            self.sprite_sheet, # Use the same sprite sheet
            row=gs.TILE_HEIGHT, 
            col=gs.TILE_WIDTH, 
            width=gs.TILE_WIDTH - 1,
            height=gs.TILE_HEIGHT,
            resize=True            
        )

        #This is from gemini as a test
        # --- ADD THIS CODE BELOW ---
        # Create a Green Background Block manually
        bg_surface = pygame.Surface((gs.SIZE, gs.SIZE))
        bg_surface.fill(gs.PITCH_RED) # Fills the square with Green color
        
        # Save it so game.py can find it
        self.background = {"background": [bg_surface]}

    def load_sprite_sheet(self, path, file_name): # Removed width, height arguments
        """Load a sprite sheet.""" 
        image = pygame.image.load(f"{path}/{file_name}").convert_alpha()
        # image = pygame.transform.scale(image, (width, height)) # REMOVED SCALING
        return image
    
    def load_sprites(self, spritesheet, xcoord, ycoord, width, height):
        """Load individual sprites from a sprite sheet."""
        # CREATE AN EMPTY SURFACE
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill the surface with a off color
        #image.fill((0, 0, 1))
        # BLIT THE SPRITE SHEET ONTO THE NEW SURFACE
        image.blit(spritesheet, (0, 0), (xcoord, ycoord, width, height))
        # CONVERT BLACK COLOURS ON THE NEW IMAGE TO TRANSPARENT 
        #image.set_colorkey(gs.BLACK)
        return image
    
    def load_sprite_range(self, image_dict, spritesheet, row, col, width, height, resize=False): # Changed defaults
        """Return a dictionary containing list of images for the animation."""
        animation_images = {}
        for animation in image_dict.keys():
            animation_images[animation] = []
            for coord in image_dict[animation]:
                # NOTE: The coordinates here are (ROW, COL) * (SPRITE_HEIGHT, SPRITE_WIDTH)
                # You were using coord[1] * col (COL * WIDTH) for x and coord[0] * row (ROW * HEIGHT) for y
                # This is correct for (ROW, COL) mapping if row/col are pixel sizes
                image = self.load_sprites(
                    spritesheet, 
                    coord[1] * col, # X-coordinate: Column index * Sprite Width
                    coord[0] * row, # Y-coordinate: Row index * Sprite Height
                    width, 
                    height
                )
                if resize:
                    # Scale to a more suitable game size, like 32x64 or 64x64
                    image = pygame.transform.scale(image, (gs.SIZE, gs.SIZE)) # Example scale
                animation_images[animation].append(image)
        return animation_images