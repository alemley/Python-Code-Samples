import sys


class Customer:

    def __init__(self, _allocation_matrix, _request_matrix, _number_of_resource_types, _finished):
                self.request_matrix = _request_matrix
                self.allocation_matrix = _allocation_matrix
                self.number_of_resource_types = _number_of_resource_types
                self.finished = _finished
                                

class Banker:

        def __init__(self, _available_resources, _customers):

                self.available_resources = _available_resources # holds the available resources matrix
                self.customers = _customers # holds a list of Character type objects

        def run(self):
            completed_processes = 0 # will be used to compare completions against total processes
            total_processes = len(customers) # the length of the Customer obj. list will serve as the total
            attempts = 0 # will be used as an arbitrary counter to detect infinite looping
            first = 1 # will be used to detect if the system is on its first pass through the processes or not
            order = [] # will be appended to as processes complete for later output
            while completed_processes < total_processes: # keep going as long as all processes aren't complete
                for n in range(len(customers)):
                    current_customer = customers[n] # iterate through each obj. in the customers list
                    # if the process isn't already finished and has enough available to complete, go through these steps
                    if (current_customer.request_matrix <= self.available_resources) and (current_customer.finished == 0):
                        print("Request matrix for process %d:" % n)
                        print(current_customer.request_matrix)
                        print("Available resources for process %d:" % n)
                        print(self.available_resources)
                        print("Attempting to complete process %d..." % n)
                        print("Process %d successfully satisfied." % n)
                        print("%d resources freed." % current_customer.allocation_matrix)
                        self.available_resources += current_customer.allocation_matrix # update freed resources
                        print("New available resources matrix:", self.available_resources)
                        # increment the completed processes and infinite loop detection variable
                        completed_processes += 1
                        attempts += 1
                        current_customer.finished = 1 # set current process to finished
                        order.append(n) # append completed processes to a list for printing
                        # check for safe or unsafe states
                        self.check_state(completed_processes, total_processes, attempts, order)
                    elif current_customer.finished == 1:
                        # just move along if its already been processed. Popping from the list was also an option
                        # here, but was causing problems since my loop depends on len(customers)
                        n += 1
                    else:
                        if first == 1:
                            # print the following information only once
                            print("Request matrix for process %d:" % n)
                            print(current_customer.request_matrix)
                            print("Resources currently available:")
                            print(self.available_resources)
                            print("Not enough resources to complete process %d at this time. Attempting to finish other processes first." % n)
                        attempts += 1
                        # if the infinite loop detection variable is going haywire, deadlock is happening
                        if first == 0 and attempts > 10000:
                            print("Retried process %d with maximum possible available resources." % n)
                            print("Deadlock detected. Process %d cannot complete using the allocated and available resources." % n)
                            self.check_state(completed_processes, total_processes, attempts, order)
                        first = 0

        def check_state(self, _completed_processes, _total_processes, _attempts, _order):
            completed_processes = _completed_processes
            total_processes = _total_processes
            attempts = _attempts
            order = _order

            if completed_processes == total_processes: # everything finished okay
                print("No deadlock detected; the system is in a safe state.")
                print("Order of process completion:")
                print(order)
                return 1
            elif(attempts > 10000) and (completed_processes != total_processes):
                print("System is in an unsafe state. Press Enter to end simulation.")
                input() # wait for an ENTER
                exit()

if __name__ == "__main__":
        go_again = 'y'

        while go_again == 'y':
            customers = []
            IOcontrol = 0
            input_file = []
            print("Enter the name of the text file to use as input, including the .txt:")
            while IOcontrol == 0:
                try:
                    filename = input()
                    input_file = open(filename)
                    IOcontrol = 1
                except IOError:
                    print("Specified file does not exist, enter a different text file:")

            # parse file into lines, separating by endlines
            file_lines = [line.rstrip('\n') for line in input_file]

            # assign corresponding lines to matrices
            number_of_processes = int(file_lines[0])
            number_of_resource_types = int(file_lines[1])
            available_resource_matrix = list(str(file_lines[2]))
            available_resource_integer = []
            finished = False

            for i in range(number_of_resource_types):
                    # convert string matrices into integers of M digits in length
                    # couldn't figure out why, but this ignores zeros unless they are after a non-zero integer
                    # had to edit my input so that no matrices started with zero
                    available_resource_integer = int(''.join(str(i) for i in available_resource_matrix))

            print("Number of processes: %d" % number_of_processes)
            print("Number of resource types: %d" % number_of_resource_types)
            print("Available instances of each resource: %s" % available_resource_matrix)

            # populate customer objects with matrices
            for i in range(number_of_processes):
                    request_matrix_integer = []
                    allocation_matrix_integer = []

                    # print("Allocation matrix for process %d:" % i)
                    allocation_matrix = list(str(file_lines[i + 3]))
                    # print(allocation_matrix)
                    allocation_matrix_integer = int(''.join(map(str, allocation_matrix)))
                    # print("Allocation matrix as an integer:", allocation_matrix_integer)

                    # print("Request matrix for process %d:" % i)
                    request_matrix = list(str(file_lines[i + number_of_processes + 3]))
                    # print(request_matrix)
                    request_matrix_integer = int(''.join(map(str, request_matrix)))
                    # print("Request matrix as an integer:", request_matrix_integer)

                    temp_customer = Customer(allocation_matrix_integer, request_matrix_integer, number_of_resource_types, finished)
                    customers.append(temp_customer)

            # create banker object
            banker = Banker(available_resource_integer, customers)
            banker.run()
            print("Would you like to test a new input file? y/n")
            go_again = input()