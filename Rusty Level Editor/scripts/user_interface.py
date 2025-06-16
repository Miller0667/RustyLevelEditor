import pygame
import os

from scripts.utils import load_image, load_images, Button
from scripts.assets import Assets

class UI:
    def __init__(self, game):
        self.game = game
        self.assets = self.game.assets.assets
    
    def load_tile_ui(self, surf):
        #Grabs each asset upon loading. and displays them in a grid format
        pos=(0,20)
        for cat, list in self.assets.items():
            print(cat + str(pos))
            for image in range(len(list)):
                button = Button(self.game, pos, {'type': cat, 'variant': image}, self.assets[cat][image].copy())
                self.game.buttons.append(button)
                pos = (pos[0] + 16, 20)

                
