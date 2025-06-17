import sys
import os

from scripts.utils import load_images

class Assets:
    def __init__(self):
        self.assets = {}
        self.tile_list_path = 'data\images/tiles'
        tile_file_list = os.listdir(self.tile_list_path) 
        for file in tile_file_list:
            if file not in self.assets:
                self.assets[file] = load_images(self.tile_list_path + '/' + file)
            else:
                raise FileExistsError
    
    def add_asset(self, file_path):
        self.assets[file_path] = load_images(self.tile_list_path + '/' + file_path)
        print('added ' + str(file_path) + 'to assets!')

    def delete_asset(self, file_path):
        self.assets.pop(file_path)
        print('removed ' + str(file_path) + 'to assets!')

        