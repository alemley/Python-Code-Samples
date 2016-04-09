import heapq
import os                       # needed to scan subdirectory for available files
import time                     # needed for measuring how long alg takes to run.
import math


def heuristic(current_x, current_y, goal_x, goal_y):
    manhattan_distance = ((math.sqrt((goal_x - current_x)**2))+(math.sqrt((goal_y - current_y)**2)))
    return manhattan_distance


#  Performs Best-First-Search to find whether a path exists through a maze stored in a 2D
# list of lists.  Returns True or False accordingly.
def bfs(maze):

    # compute number of rows and columns in maze.
    rows = len(maze)
    cols = len(maze[0])

    # Create a 2D list, the same size as the maze, indicating which cells have been
    # visited already.  All cells are initialized to False, indicating they haven't
    # been visited.
    visited = [[False]*cols for i in range(rows)]

    # Find the row and column coordinates of the start and end of the maze.
    start_r, start_c = find(maze, 's')
    end_r, end_c = find(maze, 'e')

    # Create queue of nodes to explore.  Initially place the starting node onto the queue.
	# Tuples have the format (score, row, col) where score is always zero.  It is a placeholder
	# ready to be replaced when the algorithm is converted to Best First Search
    toExpand = []
    manhattan_distance = heuristic(start_r, start_c, end_r, end_c)
    test_tuple = (manhattan_distance, start_r, start_c)
    test_list = []
    test_list.append(test_tuple)
    heapq.heappush(toExpand, test_list)


    ### Main BFS Execution Loop ###
    # While there are still nodes left on the queue to explore, process them one at a time.
    while len(toExpand) > 0:

        # pull the next node off the queue and break it into its component parts.
        cur = heapq.heappop(toExpand)
        print(cur)
        score, cur_r, cur_c = cur[0][0], cur[0][1], cur[0][2]

        # mark that the current cell has now been visited.
        visited[cur_r][cur_c] = True

        # Test whether you've reached the end of the maze.
        if maze[cur_r][cur_c] == 'e':
            return True

        # If current cell is not a wall, then check the neighbouring cells that can be reached
        # from the current cell (up, left, down, right) -- if neighbouring cell has not been
        # visited then it is appended to the queue of nodes to expand.
        # Since the outside of the maze is surrounded by walls, no need to worry about going
        # off the edge of the map.
        if maze[cur_r][cur_c] != '*':
            if not visited[cur_r-1][cur_c]:  # up
                manhattan_distance = heuristic(cur_r-1, cur_c, end_r, end_c)
                heapq.heappush(toExpand, [(manhattan_distance,cur_r-1,cur_c)])
            if not visited[cur_r][cur_c-1]:  # left
                manhattan_distance = heuristic(cur_r, cur_c-1, end_r, end_c)
                heapq.heappush(toExpand, [(manhattan_distance,cur_r,cur_c-1)])
            if not visited[cur_r+1][cur_c]:  # down
                manhattan_distance = heuristic(cur_r+1, cur_c, end_r, end_c)
                heapq.heappush(toExpand, [(manhattan_distance,cur_r+1,cur_c)])
            if not visited[cur_r][cur_c+1]:  # right
                manhattan_distance = heuristic(cur_r, cur_c+1, end_r, end_c)
                heapq.heappush(toExpand, [(manhattan_distance,cur_r,cur_c+1)])

    # If main loop ends without returning, then we never found a path to the end node.
    return False


# returns row and column coordinate of first instance of "letter" in the 2D list of lists
# storing the maze called "array"
# used by BFS to find the start 's' and end 'e' positions in the maze.
def find(array, letter):
    for row in range(len(array)):
        for col in range(len(array[row])):
            if array[row][col] == letter:
                return row, col


def runMaze(filename):
    # read maze in as a list of strings -- each string represents one row of maze
    file = open(filename)
    data = file.readlines()
    file.close()

    # split each string from previous list into a sub-list, creating a 2D list of lists
    for index in range(len(data)):
        data[index] = list(data[index][:-1])

    # start the timer then call BFS to find the shortest path
    start = time.time()
    pathExists = bfs(data)
    end = time.time()

    # display result and time taken for algorithm to find solution
    if pathExists:
        print("A path exists through the maze.")
    else:
        print("No path exists through the maze.")
    print("Algorithm took %f msecs to solve %s\n" % ((end-start) * 1000, filename))


def main():
    # find all the available mazes
    files = os.listdir("./mazes")
    userChoice = 0

    # while hasn't selected to quit
    while userChoice <= len(files):

        # print a menu with all of the mazes numbered
        count = 1
        for file in files:
            print("%d.\t%s" % (count,file))
            count += 1
        print("%d\tExit" % count)  # append an exit option to menu

        userChoice = int(input("Enter maze you wish to use: "))
        # if selected a maze (not exit) then run BFS on maze
        if userChoice <= len(files):
            runMaze("./mazes/"+files[userChoice-1])


if __name__ == "__main__":
    main()


# My heuristic algorithm adds together the horizontal and vertical steps needed
# to get from the current node to the end node. It ensures the distance will
# always be positive by taking the square root of the difference between
# the two points, squared. After the distance is acquired, I load it into
# the score parameter of the tuples, which is then appended to a list, and
# eventually to a heap. The nodes are organized by lowest score first.
