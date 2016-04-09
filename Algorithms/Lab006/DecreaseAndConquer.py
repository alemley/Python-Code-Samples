def main():
    io_control = 0
    input_file = ''
    print("Enter the name of the text file to use as input, including the .txt:")
    while io_control == 0:
        try:
            filename = input()
            input_file = [list(line.rstrip('\n')) for line in open(filename)]
            io_control = 1
        except IOError:
            print("Specified file does not exist, enter a different text file:")

    lines = list(input_file)

    rows = (len(lines))
    sources = []
    restart = True
    num_sources = 0
    pop_order = []
    iterator = 0

    while restart is True:
        pop_order = [x for x in sources if x != []]
        for n in range(0, rows):
            lines, source = (find_source(lines, n, rows))
            sources.append(source)
            if sources[n]:  # checks for occupancy
                num_sources += 1
            if len(pop_order) == rows:
                restart = False
            pop_order = [x for x in sources if x != []]
        if iterator == rows and len(pop_order) != rows:
            print('Graph is not acyclic...graph not sortable.')
            break
        iterator += 1
    print('Pop order', pop_order)


def find_source(_lines, _col_num, _rows):
    lines = _lines
    col_num = _col_num
    rows = _rows
    sources = []
    source_comparison = 0
    for i in range(0, rows):
        if lines[i][col_num] == '0':
            source_comparison += 1
            if source_comparison == rows:
                sources.append(col_num)
                for q in range(0, rows):
                    if col_num == q:
                        lines[col_num][q] = '1'
                    else:
                        lines[col_num][q] = '0'
    return lines, sources

if __name__ == "__main__":
    main()
