#!/usr/bin/env python
#
# Naive recursive search for path traversal in a simple maze.
#
# Usage:
#
# $ python maze.py 
#   S # # # # #
#   . . . . . #
#   # . # # # #
#   # . # # # #
#   . . . # . G
#   # # . . . #
#
#   S # # # # #
#   o o . . . #
#   # o # # # #
#   # o # # # #
#   x o o # o G
#   # # o o o #

maze = [['S','#','#','#','#','#'],
        ['.','.','.','.','.','#'],
        ['#','.','#','#','#','#'],
        ['#','.','#','#','#','#'],
        ['.','.','.','#','.','G'],
        ['#','#','.','.','.','#']]

def find_path(x, y):
    """ Finds a path through our character-based maze (stored in a 2D list).
    Uses recursion. See www.cs.bu.edu/teaching/alg/maze for more details.
    """

    if x < 0 or y < 0 or x > 5 or y > 5: return False  # If outside maze.
    if maze[x][y] == 'G': return True  # If found goal.
    if maze[x][y] == '#' or maze[x][y] == 'o': return False  # If position not open.

    maze[x][y] = 'o'  # Mark (x,y) as part of solution path.
    
    if find_path(x, y-1): return True  # Search north.
    if find_path(x+1, y): return True  # Search east.
    if find_path(x, y+1): return True  # Search south.
    if find_path(x-1, y): return True  # Search west.

    maze[x][y] = 'x'  # Unmark (x,y) as part of solution, was a dead-end.

    return False

def print_maze_raw():
    for char in maze:
        print char
    print

def print_maze():
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j]),
        print
    print

if __name__ == '__main__':
    print_maze()  # Before.
    find_path(0,0)  # Starting position is (0,0).
    maze[0][0] = 'S'  # Remark our starting position (got lost during path traversal).
    print_maze()  # After.