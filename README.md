Hello!

This is a personal project of mine to help me get more familiar with python and pygame

I dont expect this level editor to be used by anyone but myself. Therfore, it will only have tools that i would personally use in my level editing needs, then maybe some extra cause its fun to make this kind of stuff

about this program:
The window size is 1280x960
The display is 320x240

keybinds:
W,A,S,D - Camera Movement
1 - Disable/enable Grid
2 - Disable/enable World origin
G - Turn on/off grid snapping
O - Save project
DEL - Clear map
Mouse Scroll up/down - change tile group
Shift+scroll up/down - change tile variant
. - Layer up
, - Layer down

The best use case for this version of the editor is to use 16x16 pixel art assets.
This might be changed in future updates to where it can be modified to any size, but as of right now, this is the size i want

camera movement:
camera is at a set speed

Save/Load:
the file spaces are hard set in code right now, but there will be a UI update soon that fixes that issue

Clear map:
Deletes the entire tilemap. Will not save unless you press the save key

Tile group vs Tile variant:
Tile group refers to the folder that holds the tiles(decor, wood, stone, small decor, etc.)
The tile variant refers to each individual image within the tile group

Layers:
I very quickly made a layer system. Right now, it mainly works with the offgrid tiles, which is the main reason i needed the layer system anyways.
with the way it renders tiles, offgrid tiles will always be behind on grid tiles within the same layer. If the
offgrid tiles are 1 layer above the on grid tiles, then they will be placed in front of the on grid tiles
P.S. Do not worry if you space layers out more than 1 or 2 between eahc layer. The way it renders, it only renders layers with actual tiles on them.
There is not a system that checks for tiles, only if you place a tile on the layer that has not been used, it will initiate that layer. If you delete all tiles off of a
layer, it will still be active. This will be changed in the future

how to add more tile assets:
You can not add any assets through the editor as of yet, you need to go into the code and manually drag and drop your tile folder into the data/images/tiles section. It will read it from there

autotile:
There is no autotile function as of yet. there is skeleton code for it, but i plan on adding auto tile UI to the editor

Flood fill:
I do have plans to add flood fill to the editor in the near future, but i want to work on basic UI first before i get to that part

Planned updates:
near future- 
Save UI
Load UI
Tile collision
Alt. window for tiles
Layer tile delete

further out-
Flood Fill
Autotile
TileMaps(will be released with autotile)
Drag and drop files
game testing in engine

even further out-
tiles with code(being able to link code to a specific tile in engine, rather than through code)

If anyone actually decided to give this editor a go, please give me feedback in any way possible.

Here is my discord if you have any questions or feedback: hentur06




