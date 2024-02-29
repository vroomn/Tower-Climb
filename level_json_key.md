# The levels.json holds all the levels players will have to accend to reach the end of the game
## l(x)
The level itself, be it l1: Level 1, l2: Level 2, etc.
## idx
The index of the cell definition being read
## ts
All the textures
### l(x)
What layer the texture is on, per se: l1: Layer 1 ("The foreground"), l2: Layer 2 ("The backround"). The intent is to have the ability to layer multiple different textures to reduce workload
## cS
What type of shape is the collider going to be: rectangle (size of the cell), angled (some triangle in the cell), half (half of the cell, be that vertical or horizontal), [more to come]  
If null the object has no collider
## mf
Modifiers: [none at current time]