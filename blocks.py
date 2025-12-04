# ============================================================================
# FILE: blocks.py - BLOCK/TILE SPRITE CLASSES
# ============================================================================
# PURPOSE:
#   Defines block/tile classes for the Bomberman game:
#   - Blocks: Base class for all block types (handles position, rendering)
#   - Hard_block: Indestructible barriers that form the maze
#   - Soft_Block: Destructible blocks that can be destroyed by bombs
#
# DEPENDENCIES:
#   - pygame: Sprite rendering and collision detection
#   - gamesetting: Game configuration (tile sizes, offsets)
# ============================================================================

#This is blocks.py - defines block classes for the Bomberman game
import pygame
import gamesetting as gs

# ============================================================================
# CLASS: Blocks - Base class for all block types
# ============================================================================
class Blocks(pygame.sprite.Sprite):
  def __init__(self, game, images, group, row_number, col_number):
    """
    CONSTRUCTOR - Initialize a block at the specified grid position
    
    PARAMETERS:
    - game: Game object reference for accessing game state
    - images: List of sprite images for this block type
    - group: Pygame sprite group to add this block to
    - row_number: Grid row position (0-indexed)
    - col_number: Grid column position (0-indexed)
    
    INITIALIZATION:
    1. Call parent Sprite constructor to add to sprite group
    2. Calculate world pixel position from grid coordinates
    3. Create visual sprite and hitbox (collision rectangle)
    4. Set passable attribute (whether player can walk through)
    """
    super().__init__(group)
    self.GAME = game
    self.y_offset = gs.Y_OFFSET  # Vertical offset for visual alignment
    
    # Block position in grid coordinates
    self.row = row_number
    self.col = col_number
    self.size = gs.SIZE  # Tile size in pixels (64px)

    # Block position in world pixels
    self.x = self.col * self.size
    self.y = (self.row * self.size) + self.y_offset

    # Block attributes - passable=False means solid wall (blocks all movement)
    self.passable = True

    # Block display/sprite
    self.image_list = images  # List of animation frames (if any)
    self.image_index = 0      # Current frame index
    self.image = self.image_list[self.image_index]
    self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Hitbox for collision

  def update(self):
    """UPDATE - Currently empty (blocks don't animate or move)"""
    pass

  def draw(self, window, x_offset=0, y_offset=0):
    """
    DRAW - Render the block sprite with camera offset applied
    
    PARAMETERS:
    - window: pygame.Surface to draw on
    - x_offset: Horizontal camera offset (subtracts from x position)
    - y_offset: Vertical camera offset (subtracts from y position)
    
    NOTES:
    - Camera offsets create the camera follow effect
    - Block is drawn at world position minus camera offset
    """
    window.blit(self.image, (self.x - x_offset, self.y - y_offset))

  def __repr__(self):
    """String representation for debugging"""
    return "'#'"
  

class Hard_block(Blocks):
  """
  HARD_BLOCK - Indestructible barriers that form the game maze
  
  PROPERTIES:
  - passable = False (solid, cannot pass through)
  - Static (never moves or changes)
  - Placed in a grid pattern to create maze structure
  
  PLACEMENT PATTERN:
  - Borders: All edges of the map
  - Interior: Every other row/column (creates checkerboard pattern)
  - Purpose: Creates maze layout for gameplay
  """
  def __init__(self, game, images, group, row_number, col_number):
    super().__init__(game, images, group, row_number, col_number)
    # Hard blocks are always solid walls
    self.passable = False



class Soft_Block(Blocks):
  """
  SOFT_BLOCK - Destructible blocks that can be blown up by bombs
  
  PROPERTIES:
  - passable = False (solid, cannot pass through until destroyed)
  - Can be destroyed by bomb explosions
  - Randomly placed throughout the map (except near player start)
  
  PLACEMENT STRATEGY:
  - Randomly placed in open areas
  - Avoids player starting zone (rows 2-4, cols 1-3)
  - Ensures gameplay progression and exploration
  
  FUTURE FEATURES:
  - Drop power-ups when destroyed
  - Contribute to bomb explosion propagation
  """
  def __init__ (self,game,images,group,row_num, col_num):
        super().__init__(game, images, group, row_num, col_num)

  def __repr__(self):
    return "'@'"