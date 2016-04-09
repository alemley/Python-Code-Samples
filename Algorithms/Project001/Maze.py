import os
import timeit

PATH = os.getcwd()
original_x = 0
original_y = 0
basic_operations = 0


def find_start(_maze):
    maze_start = _maze
    for i in range(len(maze_start)):
        for j in range(len(maze_start[0])):
            if maze[i][j] == 's':
                return i, j


def find_path(_x, _y, _maze):
    # recursively find path based on current position in the maze
    global basic_operations
    l = _x
    m = _y
    local_maze = _maze
    if l < 0 or m < 0 or l > (len(local_maze)-1) or m > (len(local_maze[0])-1):
        basic_operations += 1
        return False  # Out of bounds
    if local_maze[l][m] == '*' or local_maze[l][m] == 'o':
        basic_operations += 1
        return False  # Space taken
    if local_maze[l][m] == 'e':
        basic_operations += 1
        return True  # Goal located

    # draw current solution approximation
    local_maze[l][m] = 'o'

    # Check North
    if find_path(l, m-1, local_maze):
        basic_operations += 1
        return True
    # Check East
    if find_path(l+1, m, local_maze):
        basic_operations += 1
        return True
    # Check South
    if find_path(l, m+1, local_maze):
        basic_operations += 1
        return True
    # Check West
    if find_path(l-1, m, local_maze):
        basic_operations += 1
        return True

    # begin backtracking over dead-ends
    local_maze[l][m] = 'x'
    print('Number of comparisons:', basic_operations)
    # If the search has returned to the original starting point, there is no path
    if l == original_x and m == original_y:
        print('All traversable routes exhausted. Maze not solvable.')
    return False


def print_maze(_maze):
    printable_maze = _maze
    for i in range(len(printable_maze)):
        for j in range(len(printable_maze[0])):
            print(printable_maze[i][j], end=''),
            if j == (len(printable_maze[0])-1):
                print('\n')

if __name__ == '__main__':
    replay = True
    while replay is True:
        options = []
        dirs = os.listdir(PATH)
        for file in dirs:
            if file.endswith(".txt"):
                options.append(file)
        print(options)
        io_control = 0
        maze = ''
        print("Enter the position in which the desired file is located, or any letter to quit.")
        try:
            entry = int(input())
            choice = options[entry]
            print(choice)
            maze = [list(line.rstrip('\n')) for line in open(choice)]
        except ValueError:
            print('Exiting program')
            exit()
        except IndexError:
            print('Invalid file number')
            exit()
        except TypeError:
            print('Invalid file number')
            exit()
        x, y = find_start(maze)
        original_x = x
        original_y = y
        start = (x, y)
        print('Starting point:', start)
        print('Unsolved maze:')
        print_maze(maze)

        # start at designated starting point
        start = timeit.default_timer()
        find_path(x, y, maze)
        stop = timeit.default_timer()
        # reset initial x, y coordinate to start = to 's' for visualization
        maze[x][y] = 's'
        print('\n\n\nTraversed maze:')
        print_maze(maze)
        print('Runtime:', (stop - start)*1000, 'milliseconds.')
