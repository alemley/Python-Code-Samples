#Python Programming Samples:

*See Operating Systems and Programming Languages for more complex projects
or Algorithms for routine, daily problem solutions*

##Contents:
1. Algorithms:
..* Lab001:
...Python implementation of classic hangman. This version reads in a list of
...countries and capitols, strips out extra punctuation and special characters,
...then gives the user three opportunities to guess incorrectly before losing 
...the game. The user's past guesses are stored in a list data structure to
...ensure they cannot guess the same character twice. When the user fills up
...the blank word, the answer is checked against the solution and a win/lose
...condition is then returned.
..* Lab002:
This lab compares the performance of some of Python's common data structures
using the timeit library. Lists and maps are written to and read from in order
to compare the runtime needed to process a large list of integers. I chose lists
and maps because they are two extremely versatile data structures that can be
applied to most, if not all programs.
..* Lab005:
This lab generates a user-specified number of points in a 2D space, then runs
a closest-pair analysis on the points using their relative positions to one-another.
The program switches out a global closest-pair for a local closest-pair any time the
current pair is closer together than the global value.
..* Lab006:
An implementation of a source-removal topological sort on adjacency matrices. The 
algorithm identifies an index as a source, then deletes the node while changing
all of its dependent nodes to sources themselves. The algorithm repeats until there
are no sources left. Each time a source is found, it is appended to a list in order
to demonstrate the order in which the adjacency matrix nodes are popped.
- Lab010:
A classic implementation of a Quicksort algorithm which uses lomuto partitioning
to pre-sort the data. A lomuto partition places a pivot value in the middle of a 
list of integers such that everything preceding the pivot is smaller than the pivot,
and everything following the pivot is larger than the pivot(though unordered).
Quicksort then sorts the left half of the list, then the right side of the list, then
re-partitions and recurses until each side of the list is one digit. At this point,
the numbers will be in ascending numerical order.
- Lab011:
This lab was used to demonstrate which kinds of cases made presorting more efficient
than linear sorting. Using a brute force linear search to find a pattern in a set of
data is relatively slow on large data sets, but can actually be faster than presorting
when used on smaller data sets. Pre-sorting the list of data by turning in into a heap,
then popping the smallest value from the heap into a new list will place it into ascending
order, which can make it easier to search. It takes longer, however, to pre-sort data than
to brute force search it unless we are dealing with thousands of values.
- Lab012:
Maze pathfinding. This algorithm uses decrease and conquer methodologies to determine if 
a path exists from the starting point to the ending point of a maze. It uses recursion to 
constantly reduce the size of the problem to just the next available move that has not
already been traversed and is not blocked. Using decrease and conquer, the algorithm can
also return multiple valid paths and determine the most optimal, or shortest path.
- Lab013:
Input-Enhancement algorithm. This algorithm employs a time-space tradeoff methodology in
order to increase runtime and efficiency while finding for a string within a given block
of text, while sacrificing space, or memory used to store a character by character shift
table. Traditionally, the last character in the pattern that is trying to be found would
be compared to n + number of identical characters where n is the length of the block of
text. This method is not very efficient, but the input enhancement allows many comparisons
to be completely skipped based on the structure of the string itself, increasing efficiency
by a very large amount.
- Lab016:
This algorithm utilizes a time-space tradeoff(dynamic programming)to find the best order
to choose from a line of objects of varying value in which an opponent and the player can
only take an item from the very beginning or end of the line. The first reaction is to take
the highest value object available from one of the two ends, but this could often unblock 
an item of even higher value for the opponent to take. This algorithm stores possible options
in memory and compares them against all other possibilities by looking ahead in the line to 
see what the future turns would entail, then determines which item to pick in each turn in
order to guarantee the highest overall value is in posession.
- Project 1:
A larger scale, more in-depth version of lab012 which utilizes more efficient mechanisms to
increase execution efficiency.

- Operating Systems:
- Barber Shop:
This project uses threads and mutexes to synchronize multiple processes and coordinate appropriate
output. The problem states that a barber goes to sleep if his shop is empty, but if someone comes
into his shop, they wake him up and ask for a hair cut. Additional patrons come in and sit in the
waiting area if the barber is busy. Once all available customers have been served, the barber shuts
down his shop. This project exposed me to the concept of multi-threading and allowed me to get some
practice with synchronization.
- Banker's Algorithm:
This program focuses on resource allocation. It takes requests from customers, checks the current
available resources, then makes loans if it can without deficiting resources. When a customer is 
done with the resources, the banker gets them back and can loan them to a different customer. The 
banker is the main process, and each new customer is a separate thread, which all compete for the 
same pool of resources.
- Final Project - San Diego Zoo:
This is a larger-scale multi-threading project which utilizes concepts from both the barber shop 
and banker's algorithm to organize queues of patrons, distribute resources, and protect attributes
accessed by multiple threads. The program ehibits all of the important pieces of operating system
resource distribution and process synchronization.

- Programming Languages:
- Scheme Interpreter:
My professor wrote a scheme interpreter in C++, which we had to translate to any language we chose
while retaining complete functionality. The finished python program consists of Scanning, parsing,
tokenizing, and executing scheme/lisp input and returning the result. Each part of the finished product
was constructed as a standalone program before being integrated into one piece. Each portion of the 
program passes its output to the next portion. The program is written in an object-oriented, C++ clone
manner, and is the largest Python project I have written to date.