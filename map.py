dungeon = [
    "#########################################",
    "#rrrrrr##############ccccccccccccc#######",
    "#rrrrrr##############c###########c#######",
    "#rrrrrr##############c###########c#######",
    "#rrrrrr##############c###########c#######",
    "#ccccccccccccccccccccccccccccc###c#######",
    "#c#############c#c#c#c#######c###c#######",
    "#c#############rrrrrrrr######c###c#######",
    "#c#############rrrrrrrr######c###c#######",
    "#c#####rrrrrr##rrrrrrrr######ccccccrrrr##",
    "#c#####rrrrrr##rrrrrrrr######c#####rrrr##",
    "#c#####rrrrrr##rrrrrrrr######c#####rrrr##",
    "#c#####rrrrrr##rrrrrrrr######c#####rrrr##",
    "#c#####rrrrrrccccccccccccc###ccccc#######",
    "#c#####rrrrrrc###########c#######c#######",
    "#c###########c###########c#######c#######",
    "#c###########c###########c#######c#######",
    "#ccccccccccccccccc#######ccccccccc#######",
    "#c###c#c#########c#######c#######c#######",
    "#c###rrrr########c#######c#######rrrrrr##",
    "#c###rrrr########c#######c#######rrrrrr##",
    "#c###rrrr########c###ccccc#######rrrrrr##",
    "#c###rrrr########c###c###c#######rrrrrr##",
    "#c###rrrr########c###c###c###############",
    "#c###rrrr########c###c###c###############",
    "#c#####rrrrrrrr##c###c###ccccccccccccc###",
    "#c#####rrrrrrrr##c###c#########c#c###c###",
    "#c#####rrrrrrrr##c###c#########rrrr##c###",
    "#c#####rrrrrrrr##c###c#########rrrr##c###",
    "#c#####rrrrrrrr##c###ccrrrrrrrrrrrr##c###",
    "#c#####rrrrrrrr##c###c#rrrrrrrrrrrr##c###",
    "#c###rrrr########c###ccrrrrrrrrrrrr##c###",
    "#c###rrrr########c###c#rrrrrrrrrrrr##c###",
    "#c###rrrr########c###c#########rrrr##c###",
    "#c###rrrr########c###c#########rrrr##c###",
    "#c###############c###c###############c###",
    "#c###############c###c###############c###",
    "#ccccccccccccccccc###ccccccccccccccccc###",
    "#########################################",
    "#########################################",
    "#########################################"
]

types = {'#': 'wall', 'c': 'corridor', 'r': 'room'}
data = []
for y, row in enumerate(dungeon):
    for x, node in enumerate(row):
        data.append({
            'type': types[node],
            'x': x,
            'y': y
        })
import json
print(json.dumps(data, indent=4))
