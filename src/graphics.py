## \file graphics.py
#
#  This file contains classes working with graphics.

import os
import pygame as pg
import pytmx
import pygame
import general
import time
import kek
import math
import random
import time


class TileImageLoader:
      
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def get_tile_image(tile_type):
      if not (tile_type.identifier in TileImageLoader.tile_images):  # lazy image loading
       TileImageLoader.tile_images[tile_type.identifier] = TileImageContainer(os.path.join(general.RESOURCE_PATH,"tile_" + tile_type.name + ".png"))

      return TileImageLoader.tile_images[tile_type.identifier]

class TileImageContainer:
  def init(self):
    self.main_tile = [None,None,None,None] # main tile variations or alternatively animation frames
    self.corner_UL_00 = None
    self.corner_UL_01 = None
    self.corner_UL_10 = None
    self.corner_UL_11 = None

  def load_from_file(self,filename):
    image = pygame.image.load(filename)
    image = image.convert_alpha()

    self.main_tile[0] = image.subsurface(general.TILE_WIDTH * 2,0,general.TILE_WIDTH,general.TILE_HEIGHT)
    self.main_tile[1] = image.subsurface(general.TILE_WIDTH * 3,0,general.TILE_WIDTH,general.TILE_HEIGHT)
    self.main_tile[2] = image.subsurface(general.TILE_WIDTH * 2,general.TILE_HEIGHT,general.TILE_WIDTH,general.TILE_HEIGHT)
    self.main_tile[3] = image.subsurface(general.TILE_WIDTH * 3,general.TILE_HEIGHT,general.TILE_WIDTH,general.TILE_HEIGHT)

  def make_character_image(self, race, gender, head_number, animation_type, animation_frame):

    animation_string = ""
    direction_string = ""
    race_string = ""
    gender_string = ""

    head_coordinates = (0,0)

    if race == general.RACE_HUMAN:
      race_string = "human"

    if animation_type == general.ANIMATION_IDLE_UP:
      animation_string = "idle"
      direction_string = "up"
      head_coordinates = (4,0)
    elif animation_type == general.ANIMATION_IDLE_RIGHT:
      animation_string = "idle"
      direction_string = "right"
      head_coordinates = (6,0)
    elif animation_type == general.ANIMATION_IDLE_DOWN:
      animation_string = "idle"
      direction_string = "down"
      head_coordinates = (4,0)
    else:                         # idle left
      animation_string = "idle"
      direction_string = "left"
      head_coordinates = (3,0)

    image_head = pygame.image.load(os.path.join(RESOURCE_PATH,"character_" + race_string + "_" + str(head_number) + "_" + direction_string + ".png"))

    if animation_type in (general.ANIMATION_IDLE_RIGHT,general.ANIMATION_IDLE_LEFT):
      image1 = pygame.image.load(os.path.join(general.RESOURCE_PATH,"character_" + race_string + "_" + gender_string + "_body_" + animation_string + "_" + direction_string + "_layer1.png"))
  
      image1.blit(image2,(0,0))
      image1.blit(image_head,head_coordinates)

    return image1


  def __tile_priority(self, tile_type):
    try:
      return tile_type.priority
    except Exception:
      return 0


  def __make_tile_priority_list(self, terrain_array):
    result = []

    for j in range(terrain_array.height):
      for i in range(terrain_array.width):
        tile_type = terrain_array.get_tile_type(i,j)

        if tile_type != None and tile_type.animated:    # this maked animated tiles not render, they are drawn differently (the cannot be prerendered because they are changing constantly)
         
          return sorted(result)


  def make_terrain_image(self, terrain_array):
    result_image = pygame.Surface((terrain_array.width * general.TILE_WIDTH, terrain_array.height * general.TILE_HEIGHT),flags = pygame.SRCALPHA)
    result_image.fill((255,255,255,0))

    for current_priority in self.__make_tile_priority_list(terrain_array):      # draw the terrain in layers
      for j in range(terrain_array.height):
        for i in range(terrain_array.width):
          tile_type = terrain_array.get_tile_type(i,j)

          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j - 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j - 1)) and \
             tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j)):
           result_image.blit(tile_picture.corner_DR_00,(i * general.TILE_WIDTH - general.SUBTILE_WIDTH,j * general.TILE_HEIGHT - general.SUBTILE_HEIGHT))

          if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i,j - 1)):
            if tile_priority > self.__tile_priority(terrain_array.get_tile_type(i - 1,j - 1)):  # left
              helper_image = tile_picture.corner_DL_01
            else:
              helper_image = tile_picture.corner_DL_11

            result_image.blit(helper_image,(i * general.TILE_WIDTH,j * general.TILE_HEIGHT - general.SUBTILE_HEIGHT))

    return result_image


class kekRenderer:

  ## view width in pixels
  VIEW_WIDTH = 800

  ## view height in pixels
  VIEW_HEIGHT = 480

  ## view width in pixels
  VIEW_WIDTH_TILES = math.ceil(VIEW_WIDTH / general.TILE_WIDTH)

  ## view height in pixels
  VIEW_HEIGHT_TILES = math.ceil(VIEW_HEIGHT / general.TILE_HEIGHT)

  TILE_PADDING = 15

  ## active area width in tiles

  ACTIVE_AREA_WIDTH = VIEW_WIDTH_TILES + 2 * TILE_PADDING

  ## active area height in tiles

  ACTIVE_AREA_HEIGHT = VIEW_HEIGHT_TILES + 2 * TILE_PADDING
  
  def kekRenderer(self, surface):
    
      tw = self.tmx_data.tilewidth
      th = self.tmx_data.tileheight
      gt = self.tmx_data.getTileImageByGid

      if self.tmx_data.background_color:
          surface.fill(self.tmx_data.background_color)

      for layer in self.tmx_data.visibleLayers:
            if isinstance(layer, pytmx.TiledLayer):
                for x, y, gid in layer:
                    tile = gt(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

  def _view_top_left_tiles(self):
       return (math.floor(self._view_top_left[0] / general.TILE_WIDTH),math.floor(self._view_top_left[1] / general.TILE_HEIGHT))()

  if ((self.kek.active_area[0] > 0 and in_tiles[0] <= self.kek.active_area[0]) or
        (self.kek.active_area[1] > 0 and in_tiles[1] <= self.kek.active_area[1]) or
        (self.kek.active_area[0] + self.kek.active_area[2] < self.kek.width and in_tiles[0] + kekRenderer.VIEW_WIDTH_TILES >= self.kek.active_area[0] + self.kek.active_area[2]) or
        (self.kek.active_area[1] + self.kek.active_area[3] < self.kek.height and in_tiles[1] + kekRenderer.VIEW_HEIGHT_TILES >= self.kek.active_area[1] + self.kek.active_area[3])):
      print("changing active area")
      print(self.kek.get_active_area_props())

      self.__change_active_area()

  def __init_attributes(self):
    self.terrain_image = None
    self._view_top_left = (0,0)
    self.canvas = pygame.Surface((kekRenderer.VIEW_WIDTH,kekRenderer.VIEW_HEIGHT))
    self.kek = None
    
  def view_top_left_relative(self):
    return (self.view_top_left[0] - self.kek.active_area[0] * general.TILE_WIDTH,self.view_top_left[1] - self.kek.active_area[1] * general.TILE_HEIGHT)

  def view_top_left_relative_tiles(self):
    pixel_coordinates = self.view_top_left_relative()
    x = math.floor(pixel_coordinates[0] / general.TILE_WIDTH)
    y = math.floor(pixel_coordinates[1] / general.TILE_HEIGHT)
    return (x,y,pixel_coordinates[0] - x * general.TILE_WIDTH,pixel_coordinates[1] - y * general.TILE_HEIGHT)

  def __init__(self,kek):
    self.__init_attributes()
    self.kek = kek
    self.__change_active_area()
    
  def __change_active_area(self):
    image_compositor = ImageCompositor()
    view_tile_coordinates = self._view_top_left_tiles()

    new_area = (general.saturate(view_tile_coordinates[0] - kekRenderer.TILE_PADDING,0,self.kek.width - kekRenderer.ACTIVE_AREA_WIDTH),
                general.saturate(view_tile_coordinates[1] - kekRenderer.TILE_PADDING,0,self.kek.height - kekRenderer.ACTIVE_AREA_HEIGHT),
                kekRenderer.ACTIVE_AREA_WIDTH,
                kekRenderer.ACTIVE_AREA_HEIGHT)

    self.kek.active_area = new_area
    self.terrain_image = image_compositor.make_terrain_image(self.kek.kek_area)


  def render(self):
    self.canvas.fill((255,0,0,0))

    view_top_left_tile = self.view_top_left_relative_tiles()

    # prepass, get objects in view to be rendered plus render animated files
    y = -view_top_left_tile[3]
    for j in range(view_top_left_tile[1],view_top_left_tile[1] + kekRenderer.ACTIVE_AREA_HEIGHT):
      x = -view_top_left_tile[2]
      for i in range(view_top_left_tile[0],view_top_left_tile[0] + kekRenderer.ACTIVE_AREA_WIDTH):
        tile_type = self.kek.kek_area.get_tile_type(i,j)
        if tile_type.animated:
          self.canvas.blit(TileImageLoader.get_tile_image(tile_type).main_tile[int(time.time()) % 4],(x,y))
        x += general.TILE_WIDTH
      y += general.TILE_HEIGHT

    view_relative = self.view_top_left_relative()
    self.canvas.blit(self.terrain_image,(-1 * view_relative[0],-1 * view_relative[1]))
    return self.canvas
  
  def make_2x_map(self):
        temp_surface = pg.Surface(self.size)
        self.render(temp_surface)
        temp_surface = pg.transform.scale2x(temp_surface)
        return temp_surface

