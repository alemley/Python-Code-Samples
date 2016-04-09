from threading import Thread
from threading import Lock
from threading import Event
import random

lock = Lock()
done = Event()
is_done = 0


# Stores a copy of the input file's data
class Arguments:
    # visitors, cars, pumps, time interval
    def __init__(self, m_visitors, n_cars, k_pumps, t_time, _done):
        self.m_visitors = m_visitors
        self.n_cars = n_cars
        self.k_pumps = k_pumps
        self.t_time = t_time
        self.done = _done


# holds information for the cars, and is used to initialize carthread
class Car:
    def __init__(self, rides, time, in_service, in_queue):
        self.rides = rides
        self.time = time
        self.in_service = in_service
        self.in_queue = in_queue


# holds information for the pumps, and is used to initialize the pump thread
class Pump:
    def __init__(self, in_use, car_num, time):
        self.in_use = in_use
        self.car_num = car_num
        self.time = time


# controls the pump_line, the cars waiting to refuel
class PumpQueue:
    def __init__(self, max_size):
        self.pQueue = [None] * max_size
        self.max_size = max_size
        self.front = 0
        self.back = 0
        self.size = 0


# the visitor thread
def visitor_thread(_visitor):
    global is_done
    visitor = _visitor

    v = visitor.m_visitors
    c = visitor.n_cars

    n = 0
    while n < v:
        for j in range(0, c):
            lock.acquire()
            if cars[j].in_service is False and cars[j].rides < 5:  # maximum of five rides
                print('\nVisitor %d boarded car %d' % (n+1, j+1))
                print("Car %d Fuel: %d%%" % (j+1, (100 - (20 * cars[j].rides))))
                cars[j].in_service = True
                n += 1
                print('\n%d customers are waiting for a ride.' % (v - n))
                lock.release()
                break
            lock.release()
    lock.acquire()
    is_done += 1
    lock.release()


# the car thread
def car_thread(_car):
    global is_done
    carthread = _car
    cars_done = 0

    c = carthread.n_cars
    t = carthread.t_time

    while cars_done == 0:
        cars_in_service = 0
        for k in range(0, c):
            lock.acquire()
            if cars[k].in_service is True and cars[k].rides < 5:  # car can keep going
                cars[k].time += 1
            if cars[k].time == t:
                cars[k].in_service = False
                cars[k].rides += 1
                cars[k].time = 0
            if cars[k].rides == 5 and cars[k].in_queue is False:  # car must refuel
                push(k)  # push into the queue of cars
                cars[k].in_queue = True
            if cars[k].in_service is False:
                cars_in_service += 1
            lock.release()
        if cars_in_service == c and is_done >= 1:
            cars_done = 1
    lock.acquire()
    is_done += 1
    lock.release()


# the gas station thread
def gas_station_thread(_gas_station):
    global is_done
    refill_early = 0  # random integer to function as conrol for non-empty pump station refuelling
    gas_station = _gas_station

    truck = False
    cars_filled = 0
    p = gas_station.k_pumps

    gas_done = 0
    pumps_in_service = 0

    while gas_done == 0:
        for j in range(0, p):
            lock.acquire()
            if pumps[j].in_use is True:
                pumps[j].time += 1
            if pumps[j].time == 3:  # three units of time to refuel
                print("\nCar %d has been refueled by pump %d" % (pumps[j].car_num + 1, j + 1))
                cars[pumps[j].car_num].in_service = False
                cars[pumps[j].car_num].rides = 0
                cars[pumps[j].car_num].time = 0
                cars[pumps[j].car_num].in_queue = False
                pumps[j].time = 0
                pumps[j].in_use = False
                cars_filled += 1
                print('Gas station fuel: %d%%' % (10 * (10 - cars_filled)))
                pumps_in_service -= 1
            if truck is True and pumps[j].in_use is False:
                truck = False
                print('Fuel Truck is currently filling up the gas station.')
                for q in range(0, 15):  # simulating 15 units of time to refuel
                    pumps[j].time += 1
                    if pumps[j].time == 15:
                        print('The Gas Station has been refilled')
            elif pumps[j].in_use is False and pump_line.size > 0:
                pumps_in_service += 1
                pumps[j].in_use = True
                pumps[j].car_num = pump_line.front
                print('Car %d is getting fuel from pump %d' % (pumps[j].car_num + 1, j + 1))
                pumps[j].time = 0
                pop()  # remove car from the queue
            lock.release()

            if cars_filled > 5:  # begin randomly trying to fill if it is half empty
                gasStationThread.refill_early = random.randint(0, 1)
            if cars_filled > 10 or refill_early == 1:
                print('The Fuel Truck is currently on its way')
                truck = True
                cars_filled = 0
            if pumps_in_service == 0 and is_done == 2:
                gas_done = True
    lock.acquire()
    is_done += 1
    lock.release()


# removes a car from the queue
def pop():
    fr = pump_line.front
    f = pump_line.pQueue[fr]
    pump_line.size -= 1
    if pump_line.size == 1:
        print("\n%d car is waiting for a gas pump" % pump_line.size)
    else:
        print("\n%d cars are waiting for a gas pump" % pump_line.size)
    if fr < (pump_line.max_size - 1):
        pump_line.front += 1
    else:
        pump_line.front = 0

    return f


# adds a car to the waiting queue for a pump
def push(_c):
    c = _c
    b = pump_line.back
    pump_line.pQueue[b] = c
    pump_line.size += 1
    if pump_line.size == 1:
        print("\n%d car is waiting for a gas pump" % pump_line.size)
    else:
        print("\n%d cars are waiting for a gas pump" % pump_line.size)
    if b < (pump_line.max_size - 1):
        pump_line.back += 1
    else:
        pump_line.back = 0

if __name__ == "__main__":
    # initialize arguments and main obj
    arguments = Arguments(0, 0, 0, 0, False)
    main = Arguments(0, 0, 0, 0, False)
    thread = []
    round_number = 0
    io_control = 0
    input_file = []
    number_of_threads = 3

    print("Enter the name of the text file to use as input, including the .txt:")
    while io_control == 0:
        try:
            filename = input()
            input_file = open(filename)
            io_control = 1
        except IOError:
            print("Specified file does not exist, enter a different text file:")

    file_lines = []
    num_lines = 0
    for line in input_file:
        line = line.split(",")
        num_lines += 1
        if line:
            line = [int(i) for i in line]
            file_lines.append(line)

        main.m_visitors = int(file_lines[round_number][0])
        main.n_cars = int(file_lines[round_number][1])
        main.k_pumps = int(file_lines[round_number][2])
        main.t_time = int(file_lines[round_number][3])

    while main.done is False and round_number < num_lines:
        skip = False
        print("\n\n\n\n\nRound Number: %d" % (round_number + 1))

        if main.n_cars == 0:  # handles a line of all zeros in the input
            print('No data to read in this round, continuing to next round:')
            skip = True
        if skip is False:
            print("Number of Visitors: %d" % main.m_visitors)
            print("Number of Cars: %d" % main.n_cars)
            print("Number of Pumps: %d" % main.k_pumps)
            print("Units of Time: %d" % main.t_time)

            M = main.m_visitors
            N = main.n_cars
            K = main.k_pumps
            T = main.t_time

            thread_info = []
            cars = []
            pumps = []

            # initialize arguments
            for i in range(0, 3):
                temp = Arguments(M, N, K, T, False)
                thread_info.append(temp)
            # initialize cars
            for i in range(0, N):
                temp = Car(0, 0, False, False)
                cars.append(temp)
            # initialize pumps
            for i in range(0, K):
                temp = Pump(False, 0, 0)
                pumps.append(temp)
            # initialize pump line
            pump_line = PumpQueue(N)

            # create the threads
            visitorThread = Thread(target=visitor_thread, args=(thread_info[0],))
            thread.append(visitorThread)

            carsThread = Thread(target=car_thread, args=(thread_info[1],))
            thread.append(carsThread)

            gasStationThread = Thread(target=gas_station_thread, args=(thread_info[2],))
            thread.append(gasStationThread)

            # start the threads
            visitorThread.start()
            carsThread.start()
            gasStationThread.start()

            # tell threads to wait for one another before finishing
            visitorThread.join()
            carsThread.join()
            gasStationThread.join()

            print('All visitors have taken a tour, searching for a new round...')

        round_number += 1
        is_done = 0

        try:
            main.m_visitors = int(file_lines[round_number][0])
            main.n_cars = int(file_lines[round_number][1])
            main.k_pumps = int(file_lines[round_number][2])
            main.t_time = int(file_lines[round_number][3])
        except IndexError:
            break

print("\nNo lines remaining in input file, terminating program.")
