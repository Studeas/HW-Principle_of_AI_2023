# Escape Tower of the Sorcerer: Search Algorithms Application

This project presents a maze-solving game where a player (warrior) must escape from a tower filled with obstacles (walls) and monsters. The player aims to find the shortest path to escape while minimizing health loss from monsters. Shields are scattered throughout the map, helping the player mitigate damage from encounters.

<img src="./display/display window.png" style="zoom:50%;" />

## Design & Solution

### Maze Generation

A random map generation function (Gene_RandomMap) is used to create different maze layouts with varying obstacle density. `Gene_RandomMap` generates a random maze with configurable obstacle ratio and seed for reproducibility. `Is_Valid_Move1` validates if a move is possible (i.e., no crossing walls or going out of bounds). `Get_Possible_Moves1` provides possible moves from a given point.

### Path Searching Algorithm

A modified **Breadth-First Search (BFS)** is employed to calculate the shortest path, ensuring the warrior avoids walls and minimizes health loss from monsters. The solution considers various possible paths and picks the one with the least damage based on shield availability. 

### Optimization

All permutations of possible paths through the shields are evaluated to find the shortest path with the least cost (damage and distance).

## Files

- `surface.py`: Contains the core logic of the maze game, including map generation, pathfinding, and health calculation.
- `./img`: Folder containing image assets for the game elements such as the player, monsters, shields, walls, and background.