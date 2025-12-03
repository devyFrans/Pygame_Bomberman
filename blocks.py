#This is blocks.py - defines block classes for the Bomberman game
import pygame
import gamesetting as gs

class Blocks(pygame.sprite.Sprite):
  def __init__(self,game,images,group,row_number,col_number):
    super().__init__(group)
    self.GAME = game
    self.y_offset = gs.Y_OFFSET
    # self.passable = False #this one is temporary. Will be used for collision detection later.


    # BLOCK POSITION
    self.row = row_number
    self.col = col_number
    #self.x = col_number * gs.SIZE
    #self.y = row_number * gs.SIZE

    # Cell size
    self.size = gs.SIZE

    # Coordinates of block
    self.x = self.col * self.size
    self.y = (self.row * self.size) + self.y_offset

    # Atrributes
    self.passable = False   #False ang default nito!


    # BLOCK DISPLAY
    self.image_list = images
    self.image_index = 0
    self.image = self.image_list[self.image_index]
    self.rect = self.image.get_rect(topleft=(self.x, self.y))

  def update(self):
    pass

  def draw(self, window, offset=0):
    # Draw block shifted by horizontal camera offset
    window.blit(self.image, (self.x - offset, self.y))

  def __repr__(self):
    return "'#'"
  

class Hard_block(Blocks):
  def __init__ (self, game, images, group, row_number, col_number):
    super().__init__(game, images, group, row_number, col_number)



class Soft_Block(Blocks):
  def __init__ (self,game,images,group,row_num, col_num):
        super().__init__(game, images, group, row_num, col_num)

  def __repr__(self):
    return "'@'"