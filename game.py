#This is game.py - the main game logic for Bomberman
import pygame
from character import Character
from blocks import Hard_block, Soft_Block
from random import choice
import gamesetting as gs

#Hello this is a test comment for github.

class Game:
  def __init__(self, main, assets):
    # LINK WITH MAIN CLASS AND ASSETS
    self.MAIN = main
    self.ASSETS = assets

    # Player Character 
    #self.PLAYER = Character(self,self.ASSETS.player_char)

    # Groups
    # self.hard_blocks = pygame.sprite.Group()
    # self.soft_block = pygame.sprite.Group()
    self.groups = {
      "hard_block": pygame.sprite.Group(),
      "soft_block": pygame.sprite.Group(),
      "player": pygame.sprite.Group()  }
    
    # Player Character 
    self.PLAYER = Character(self,self.ASSETS.player_char, self.groups["player"],3,2,gs.SIZE)
    
    #Level Information
    self.level = 1
    self.level_matrix = self.generate_level_matrix(gs.ROWS,gs.COLS)

  def input(self):
    self.PLAYER.input()

  def update(self):
    # self.hard_blocks.update()
    # self.soft_block.update()
    # self.PLAYER.update()
    for value in self.groups.values():
      for item in value:
        item.update()

  def draw(self,window):
    #Draw the Green Background squares
    # for row_num, row in enumerate(self.level_matrix): 
    #   for col_num, in enumerate(row):
    #     window.blit(self.ASSETS.background["background"][0],
    #                 (col_num * gs.SIZE, (row_num * gs.SIZE) + gs.Y_OFFSET))

    #Fill the background entirely
    window.fill(gs.GREY)
    #This is from gemini as a test

    for row_num, row in enumerate(self.level_matrix): 
      for col_num, cell in enumerate(row): 
      # Now it unpacks correctly: col_num gets the index, 'cell' gets the value ("_" or "@")
       window.blit(self.ASSETS.background["background"][0],
                  (col_num * gs.SIZE, (row_num * gs.SIZE) + gs.Y_OFFSET))                


    # self.hard_blocks.draw(window)
    # self.soft_block.draw(window)
    # self.PLAYER.draw(window)
    for value in self.groups.values():
      for item in value:
        item.draw(window)



  def generate_level_matrix(self,rows,cols):
    """Generate the basic level matrix"""
    matrix = []
    for row in range(rows):
      line = []
      for col in range(cols):
        line.append("_")
      matrix.append(line)
    self.insert_hard_block_into_matrix(matrix)  
    self.insert_soft_block_into_matrix(matrix)
    for row in matrix:
      print(row)
    return matrix
      

  def insert_hard_block_into_matrix(self,matrix):
    """Insert all of the Hard Barrier Block into the level of matrix"""
    LAST_ROW = len(matrix) - 1

    if not matrix or not matrix[0]:
        return
    LAST_COL = len(matrix[0]) - 1       
    
    for row_num, row in enumerate(matrix):
       for col_num, col in enumerate(row):
         
         if row_num == 0 or row_num == LAST_ROW or \
             col_num == 0 or col_num == LAST_COL or \
               (row_num % 2 == 0 and col_num % 2 == 0):
           matrix[row_num][col_num] = Hard_block(self,
                                              self.ASSETS.hard_block["hard_block"],
                                              self.groups["hard_block"],
                                              row_num, col_num)
    return
  
  def insert_soft_block_into_matrix(self,matrix):
    """RANDOMLY INSERT SOFT BLOCKS INTO THE LEVEL MATRIX"""

    for row_num, row in enumerate(matrix):
       for col_num, col in enumerate(row):
         if row_num == 0 or row_num == len(matrix) - 1 or \
            col_num == 0 or col_num == len(row) - 1 or \
            (row_num % 2 == 0 and col_num % 2 == 0):
            continue
         elif row_num in [2,3,4] and col_num in [1,2,3]:
          continue
         else:
           cell = choice(["@","_","_","_"])
           if cell == "@":
             cell = Soft_Block(self,self.ASSETS.soft_block["soft_block"],
                               self.groups["soft_block"],row_num,col_num,)
           matrix[row_num][col_num] = cell
    return     
    # for row_num, row in enumerate(matrix):
    #   for col_num, col in enumerate(row):
    #     if row_num == 0 or row_num == len(matrix)-1 or \
    #         col_num == 0 or col_num == len(row)-1 or \
    #           (row_num % 2 == 0 and col_num % 2 == 0):
    #      matrix[row_num][col_num] = Hard_block(self, # Pass the Game instance
    #                                   self.ASSETS.hard_block["hard_block"], 
    #                                   self.hard_blocks,
    #                                   row_num, col_num)
    # return           