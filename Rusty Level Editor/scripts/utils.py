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
    def __init__(self, game, rect, text_color=(255,255,255), font=None, text=None, action=None, color=(255,255,255), hover_color=(255,255,255), img=None):
        self.game = game
        self.rect = rect
        self.text_color = text_color
        self.font = font
        self.text = text
        self.action = action
        self.color= color
        self.img = img
        self.hover_color = hover_color
    
    def draw(self, surface, mouse_pos):
        #Draw the button rectangle
        self.rect = pygame.draw.rect(surface, self.color, self.rect)

        #Checks for mouse hover
        is_hovered = self.rect.collidepoint(mouse_pos[0], mouse_pos[1])
        color = self.hover_color if is_hovered else self.color

        #draw the text centered
        #if self.text:
            #text_surf = self.font.render(self.text, True, self.text_color)
            #text_rect = text_surf.get_rect(center=self.rect.center)
            #surface.blit(text_surf, text_rect)
    
    def handle_event(self, event, mouse_position):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mouse_position):
                if self.action:
                    self.action()
                else:
                    print('Clicked!')

        