import pygame
import sys
import os

from scripts.utils import load_images, Button
from data.images import tiles
from scripts.tilemap import Tilemap
from scripts.assets import Assets
from scripts.user_interface import UI

import tkinter as tk
from tkinter import filedialog


#class Tilemap:
 #   def __init


class Editor:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        #Sets window name
        pygame.display.set_caption('Rusty Editor')

        #sets window res and editor res
        self.screen_res = (1280,960)
        self.display_res = (320, 240)
        self.editor_upscale_res = (1280,960)

        #applies the set resolutions
        self.screen = pygame.display.set_mode(self.screen_res)
        self.display = pygame.Surface(self.display_res)
        self.grid_overlay = pygame.Surface(self.display_res, pygame.SRCALPHA)

        #Enables frame rates
        self.clock = pygame.time.Clock()

        self.assets = Assets()
        
        #Sets the 4 directional movement to False(To be checked later)
        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load('map.json')
            print('loaded')
        except FileNotFoundError:
            pass
        

        #these are variables that retain to the layer properties
        self.current_layer = 0
        self.active_layers = []
        self.layer_text = pygame.font.SysFont('Tiny Islanders', 20)
        self.layer_text_opacity = 225

        #The screen location, used for camera movement
        self.scroll = [0, 0]
        #This is the world origin
        self.world_origin = (0,0)
        self.grid_opacity = 8
        self.origin_opacity = 125
        self.show_grid = True
        self.show_origin = True

        self.tile_list = list(self.assets.assets)
        self.tile_group = 0
        self.tile_variant = 2

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        #the checker to see if the user is hovering over a UI element or not.
        #This will make it so that the user will not accidentally place things if they click an UI elemnt
        self.is_hovering = False

        #Draws button UI and stores them in an array
        self.ui = UI(self)
        self.buttons = []
        #self.ui.load_tile_ui(self.grid_overlay)
        
        

    def draw_grid(self):
        tile_size = self.tilemap.tile_size

        #Renders the grid overlay
        # Calculate the number of vertical and horizontal lines to draw
        cols = self.display_res[0] // tile_size + 2  # +2 to cover edge cases
        rows = self.display_res[1] // tile_size + 2

        # Calculate where to start drawing grid lines based on world position
        start_x = -self.scroll[0] % tile_size
        start_y = -self.scroll[1] % tile_size

        #Tile Grid
        if self.show_grid:
            for col in range(cols):
                x = start_x + col * tile_size
                pygame.draw.line(self.grid_overlay, (255,255,255,min(self.grid_opacity, 255)), (x,0), (x, self.display_res[1]))
            
            for row in range(rows):
                y = start_y + row * tile_size
                pygame.draw.line(self.grid_overlay, (255,255,255,min(self.grid_opacity, 255)), (0,y), (self.display_res[0], y))
        
        #renders the world origin
        #X origin(horizontal)
        if self.show_origin:
            x_orig = pygame.draw.line(self.grid_overlay, (0,0,255,min(self.origin_opacity, 255)),
                            (self.world_origin[0], self.world_origin[1] - self.scroll[1]),
                            (self.display.width, -self.scroll[1]))
            #Y origin(vertical)
            y_orig = pygame.draw.line(self.grid_overlay, (255,0,0,min(self.origin_opacity, 255)),
                            (-self.scroll[0], self.world_origin[1]),
                            (-self.scroll[0], self.display.height))

    def run(self):
        while True:
            #refreshes the screen with a black background
            self.display.fill((20,20,25))
            self.grid_overlay.fill((0,0,0,0))

            self.is_hovering = False

            #Updates the screen position based on movement
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            #Stores it in an easier to access tuple
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            #gets mouse position
            mpos = pygame.mouse.get_pos()
            #Scales mouse position to the lower display resolution
            mpos = (mpos[0] / (self.screen_res[0] / self.display_res[0]), mpos[1] / (self.screen_res[1] / self.display_res[1]))
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            self.tilemap.render(self.display, offset=render_scroll)

            #Draws the grid
            self.draw_grid()
            for button in self.buttons:
                button.draw(self.grid_overlay, mpos)
            

            text_surface = self.layer_text.render('Layer ' + str(self.current_layer), False, (255,255,255)).convert()
            text_surface.set_alpha(self.layer_text_opacity)
            self.grid_overlay.blit(text_surface,
                            (self.grid_overlay.width - text_surface.width - 5,
                            self.grid_overlay.height - text_surface.height))        

            #Sets the preview tile image of the selected tile
            current_tile_img = self.assets.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            

            #Shows the preview tile of the selected tile image and where it is going to go
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)
            
            #If the user is clicking, and the tile grid is toggled on, then this will place the tile in
            #its designated spot
            #Checks to see if user is hovering over UI
            if self.clicking and self.ongrid and not self.is_hovering:
                if self.current_layer not in self.active_layers:
                    self.active_layers.append(self.current_layer)
                    self.tilemap.active_layers.append(self.current_layer)
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1]) + ';' + str(self.current_layer)] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos, 'layer': self.current_layer}
            #Deletes tile at mouse position
            #Checks to see if player is hovering over UI
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1]) + ';' + str(self.current_layer)
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos) and tile['layer'] == self.current_layer:
                        self.tilemap.offgrid_tiles.remove(tile)

            #Shows preview tile image in top left of screen
            self.display.blit(current_tile_img, (5,5))

            for event in pygame.event.get():
                #Closes application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #LMB
                    if event.button == 1:
                        for button in self.buttons:
                            button.handle_event(event, mpos)
                        self.clicking = True
                        if not self.ongrid and not self.is_hovering:
                            if self.current_layer not in self.active_layers:
                                self.active_layers.append(self.current_layer)
                                self.tilemap.active_layers.append(self.current_layer)
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1]), 'layer': self.current_layer})
                    #RMB
                    if event.button == 3:
                        self.right_clicking = True

                    #Changes the tile selection
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    #LMB
                    if event.button == 1:
                        self.clicking = False
                    #RMB
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    #Camera Movement
                    #a
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    #d              
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    #w        
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    #s            
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    
                    #g(toggles on/off grid)
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_1:
                        self.show_grid = not self.show_grid
                    if event.key == pygame.K_2:
                        self.show_origin = not self.show_origin
                    #pulls up file selection for saving maps
                    if event.key == pygame.K_o:
                        try:
                            self.tilemap.save(self.save_file_dialog())
                        except FileNotFoundError:
                            pass
                    #Pulls up file selection for loading maps
                    if event.key == pygame.K_p:
                        try:
                            self.tilemap.load(self.load_file_dialog())
                        except FileNotFoundError:
                            pass
                    if event.key == pygame.K_DELETE:
                        self.tilemap.clear_map()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_PERIOD:
                        self.current_layer += 1
                    if event.key == pygame.K_COMMA:
                        self.current_layer -= 1
                if event.type == pygame.KEYUP:
                    #Cancel Camera Movement
                    #a
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    #d              
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    #w        
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    #s            
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                
            self.display.blit(self.grid_overlay, (0, 0))
            self.screen.blit(pygame.transform.scale(self.display, self.editor_upscale_res), (self.screen_res[0] - self.editor_upscale_res[0],0))
            pygame.display.update()
            self.clock.tick(60)

    def save_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(defaultextension='.json')
        root.destroy()
        return file_path

    def load_file_dialog(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(defaultextension='.json')
        root.destroy()
        return file_path

Editor().run()
