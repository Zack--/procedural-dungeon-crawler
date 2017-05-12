# Procedural Dungeon Crawler

This is a fun little project where I recreate [Jamis Buck's Dungeon Generator](https://www.myth-weavers.com/generate_dungeon.php) in Python

Algorithm: [Random Dungeon Design by Jamis Buck](http://www.brainycode.com/downloads/RandomDungeonGenerator.pdf)

## Maze

Create a maze instance and connect the cells to have a perfect maze

```python
width = 10
height = 10
maze = Maze(width, height)
maze.create(randomness=0.6)
```

![Perfect maze](assets/1.basic.png)

Make it sparse by removing some deadends (if you remove all deadends you will end up with no connected cells since it's a perfect maze)

```python
maze.make_sparse(sparseness_ratio=0.4)
```

![Sparse maze](assets/2.sparse.png)

Close the remaining deadends to allow loops and have something that ressembles dungeon corridors better

```python
maze.close_deadends(randomness=0.6)
```

![No dead ends](assets/3.closed.png)

Double its size to make more space to place rooms and have more elongated corridors.

```python
maze.double()
```

![Doubled](assets/4.doubled.png)

To have a visual of the maze use `_ascii` or `_draw`

`_ascii` will return a ASCII representation of the maze

`draw` will draw the maze in a PIL image and either show it or save depending on if you pass a filename or not


Try it out yourself:

```shell
$ python example.py 10 10 0.6 0.4
```


## Rooms


![Doubled](assets/5.rooms.png)

### TO DO:

- Control room elongation

- Automatically find best room width/height ratios

- Connect rooms together

- Create better connections between corridors and room

## Weapons & Consumables

todo
