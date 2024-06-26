from MVC.EventManager import *
from Scene.UI_1 import *
import pygame
from pygame.locals import *
import pygame.freetype
import cv2
from Components.Button.Button import button
from Components.Sprite_Engine.Sprite import sprite_engine

class UI_View(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        self.model = model

    def initialize(self):
        """
        Initialize the UI.
        """
        pygame.init()
        pygame.font.init()
        pygame.freetype.init()

        pygame.display.set_caption('Test_Project')

        # flags = FULLSCREEN | DOUBLEBUF
        flags = DOUBLEBUF

        if (pygame.display.get_num_displays() >= 2):
            screen_no = 1
        else:
            screen_no = 0

        self.model.screen = pygame.display.set_mode((1280, 720), flags, 16, display = screen_no, vsync=1)

        self.clock = pygame.time.Clock()

        # speedup a little bit
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    def quit_pygame(self):
        # shut down the pygame graphics
        self.isinitialized = False
        pygame.quit()

    def init_page(self):
        self.model.start_button = button((100, 150), self.model.start_button_path, self.model, 2)
        
        #self.model.bun_sprite = sprite_engine(0.6, (100, 400), 6, self.model)

    def render(self):
        # Display FPS
        self.model.FPS_class.display_FPS()

            
        """
        Draw things on pygame
        """
        empty_color = pygame.Color(0, 0, 0, 0)
        self.model.screen.fill(empty_color)

        # Convert into RGB
        self.model.img_RGB = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)

        # Convert the image into a format pygame can display
        self.model.img_surface = pygame.image.frombuffer(self.model.img_RGB.tostring(), self.model.img.shape[1::-1], "RGB")

        # blit the image onto the screen
        self.model.screen.blit(self.model.img_surface, (0, 0))
        
        # Draw button
        self.model.start_button.draw(self.model.screen)

        # Draw sprite
        #self.model.bun_sprite.draw(self.model.bun_sprite_time)

        # Update the screen
        pygame.display.flip()

        # limit the redraw speed to 30 frames per second
        self.clock.tick(60)