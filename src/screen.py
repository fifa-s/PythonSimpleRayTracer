import pygame as pg
import numpy as np


class Screen:

  def __init__(self, screen_size=(360, 480), tick_func=lambda: None):
    self.screen_size = screen_size
    self.tick = tick_func
    self.setup()

  def setup(self):
    self.running = True
    self.max_fps = 10
    self.background_color = (255, 255, 255)
    pg.init()
    self.__screen = pg.display.set_mode(self.screen_size)
    self.screen = pg.Surface(self.__screen.get_size())
    self.clock = pg.time.Clock()

  def mainLoop(self):
    while self.running:
      self.update()
      self.tick()

  def update(self):
    self.events()
    self.__screen.fill(self.background_color)
    self.__screen.blit(self.screen, (0, 0))

    pg.display.flip()
    self.delta = self.clock.tick(self.max_fps)

  def events(self):
    for event in pg.event.get():
      if event.type == pg.QUIT:
        self.running = False

  def setAt(self, color=(0.5, 0.2, 0.8), pos=(200, 200)):
    color = [max(0,min(1,i)) for i in color]
    color = [int(i * 255) for i in color]
    pos = (pos[0], self.screen.get_size()[1] - pos[1])
    self.screen.set_at(pos, color)
