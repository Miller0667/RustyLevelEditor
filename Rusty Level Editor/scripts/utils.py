import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(path)):
        images.append(load_image(path + '/' + img_name))
    return images

def update_tile(tile):
    pass


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]

class Button:
    def __init__(self, game, pos, tile_info, img, action=None):
        self.game = game
        self.action = action
        self.img = img
        self.pos = pos
        self.tile_info = tile_info

        print('variant - ' + str(self.tile_info['variant']))

        self.update_rect()
    
    def update_rect(self):
        self.img_rect = self.img.get_rect()
        self.img_rect.x = self.pos[0]
        self.img_rect.y = self.pos[1]

    
    def draw(self, surf, mouse_pos):
        surf.blit(self.img,(self.pos[0], self.pos[1]))
        self.update_rect()

        if self.img_rect.collidepoint(mouse_pos):
            self.game.is_hovering = True
    
    def handle_event(self, event, mouse_position):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.img_rect.collidepoint(mouse_position):
                self.game.tile_group = self.tile_info['type']
                self.game.tile_variant = self.tile_info['variant']

        