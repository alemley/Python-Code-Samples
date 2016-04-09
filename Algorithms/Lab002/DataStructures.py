from random import randint
import timeit

input_file = []
io_control = 0
data = []
filename = ''
print("Enter the name of the text file to use as input, including the .txt:")
while io_control == 0:
    try:
        filename = input()
        input_file = open(filename)
        io_control = 1
    except IOError:
        print("Specified file does not exist, enter a different text file:")

print("List data structure:")
start = timeit.default_timer()
file_lines = []
num_lines = 0
for line in input_file:
    line = line.split()
    num_lines += 1
    if line:
        line = [i for i in line]
        file_lines.append(line)
for i in range(0, num_lines):
    data.append(file_lines[i][0])
    data.append(file_lines[i][1])

for k in range(0, 100):
    num = randint(0, (num_lines/2))
    print(data[(num*2)], end='')
    print(' ', data[(num*2) + 1])
stop = timeit.default_timer()
print("List data structure runtime:", (stop - start), "seconds.")
####################################################################
print("Dictionary data structure:")
d = {}
length = 0
start = timeit.default_timer()
with open(filename) as f:
    for line in f:
        (key, val) = line.split()
        d[int(key)] = val
        length += 1
for q in range(0, 100):
    number = randint(0, (length/2))
    for key, value in d.items():
        if key == number:
            print(key, value)
stop = timeit.default_timer()
print("Dictionary data structure runtime:", (stop - start), "seconds.")




