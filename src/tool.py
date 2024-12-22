import pygame

def event_loop(self):
        self.events = pg.event.get()

        for event in self.events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                self.state.get_event(event)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.get_event(event)
                

def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)
                
def image_to_map_string(image_surface, color_map, one_line = False):
  result = ""
  result += str(image_surface.get_width()) + " "

  if not one_line:
    result += "\n"

  result += str(image_surface.get_height()) + " "

  if not one_line:
    result += "\n"

  for j in range(image_surface.get_height()):
    for i in range(image_surface.get_width()):
      current_color = image_surface.get_at((i,j))

      found = False

      for item in color_map:
        if item[0] == current_color:
          found = True
          result += str(item[1]) + " " + str(item[2]) + " "
          break

      if not found:
        result += "N 0 "

    if not one_line:
      result += "\n"


  return result

img = pygame.image.load("resources/tile_city.png")
c_map = [
          (pygame.Color(0,255,0),0,0),
          (pygame.Color(0,128,0),0,1),
          (pygame.Color(0,64,0),0,2),
          (pygame.Color(0,32,0),0,3),
          (pygame.Color(255,0,0),2,0),
          (pygame.Color(128,0,0),2,1),
          (pygame.Color(64,0,0),2,2),
          (pygame.Color(32,0,0),2,3),
          (pygame.Color(255,255,255),3,0),
          (pygame.Color(128,128,128),3,1),
          (pygame.Color(64,64,64),3,2),
          (pygame.Color(32,32,32),3,3),
          (pygame.Color(0,255,255),4,0),
          (pygame.Color(0,128,128),4,1),
          (pygame.Color(0,64,64),4,2),
          (pygame.Color(0,32,32),4,3),
          (pygame.Color(0,0,255),1,0),
          (pygame.Color(128,64,0),2,0)
        ]

print(image_to_map_string(img,c_map))

def main(self):
        """Main loop for entire program"""
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)

def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)
  
def get_image(x, y, width, height, sprite_sheet):
    """Extracts image from sprite sheet"""
    image = pg.Surface([width, height])
    rect = image.get_rect()

    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(c.BLACK)

    return image