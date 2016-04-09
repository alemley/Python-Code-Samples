__author__ = 'Andrew'

import time
import sys
#import queue
from random import randint
from threading import Thread
from threading import Lock
from threading import Event

event = Event()#creates a new object to access the set, wait, and clear methods
lock = Lock()#creates a new object to access the acquire and release methods

#First attempt to create thread-derived Customer class
'''class Customer(Thread):
    def __init__(self, name):
        self.name = name'''


#Just a constructor to set the customers' names
class Customer():
    def __init__(self, name):
        self.name = name
     
#First attempt to create threade-derived Barber class
'''class Barber(Thread):
    def __init__(self):'''


class Barber:
    #lock = Lock()
    event = Event()

	#Handles the process of "cutting" the current customer's "hair"
    def HairCut(self, customer):
            print('>> %s is now ready for a hair cut.' % customer.name)
            print('>> %s moved from the waiting room to the barber chair.' % customer.name)
            self.event.clear()#.clear signifies that the barber thread is now active, preventing another customer thread from simultaneously using HairCut
            cut_duration = randint(5, 20)#Randomly generates a time between 5 and 20 seconds for the haircut duration
            print('>> It should only take Mr. Barber %d seconds to cut'
                  ' %s\'s hair. He\'s very good at his job.' % (cut_duration, customer.name))
            time.sleep(cut_duration)#Puts the current process to sleep for the duration of the haircut, while customers continue to arrive in the background
            print('>> %s\'s haircut is done.' % customer.name)
            print('>> %s left the barber shop.' % customer.name)
	
    def Sleep(self):
        self.event.wait()#Causes the barber thread to sleep until event.set is called

    def WakeUp(self):
        self.event.set()#Reactivates the barber thread


class Shop:
    customer_queue = []#Holds all of the possible customer objects, in this case, statically sized at 20 after the for loop appends names to it

    def __init__(self, barber, seats, Closing):
        self.barber = barber
        self.seats = seats
        self.closing = Closing#Determines whether the barber will close his shop yet or just go to sleep
        print('>> Welcome to Mr. Barber\'s barber shop! Now with a %d-seat waiting room!' % seats)

    def openUpShop(self):
        print('>> Mr. Barber\'s shop is open for business!')
        thread = Thread(target=self.startBarber)#Initializes the main working-thread for the barber
        thread.start()#Starts the working-thread for the barber

    def closeUpShop(self):
        print('>> All potential customers have been served.')
        print('>> Mr. Barber is closing his shop for the day.')
        sys.exit()#Exits the python interpreter gracefully if there are no more possible customers that can enter the shop

    def startBarber(self):
        while 1:
            lock.acquire()#Places a block on the barber thread so the barber cannot cut multiple customers' hair at once

            if len(self.customer_queue) != 0:
                next_customer = self.customer_queue[0]#Fetch next customer in the array

                lock.release()#Remove block on barber thread
                del self.customer_queue[0]
                self.barber.HairCut(next_customer)
            else:
                print('>> No customers in the barber shop. Mr. Barber is going to sleep...')
                lock.release()
                if len(customers) == 0 and len(Shop.customer_queue) == 0:
                    Shop.closeUpShop(self)

                barber.Sleep()
                print('>> Mr. Barber heard the door jingle and woke up!')

    def takeNewCustomer(self, customer):
        lock.acquire()#Places a block on the customer thread
        print('>> %s entered the barber shop and is looking for an available seat.' % customer.name)

        if len(self.customer_queue) == self.seats:
            print('>> All seats are taken, %s unfortunately left the barber shop.' % customer.name)
            lock.release()#Removes the block on the customer thread
        else:
            available_seats = self.seats - len(self.customer_queue)#check how many seats are already occupied, subtract it from waiting room sized
            print('>> Available Seats: %d.' % available_seats)
            print('>> %s sat down in one of the available seats.' % customer.name)
            self.customer_queue.append(new_customer)#Move customer from customer array to waiting room array
            available_seats = self.seats - len(self.customer_queue)
            print('>> Available Seats: %d.' % available_seats)
            lock.release()#Remove block on customer thread
            barber.WakeUp()

if __name__ == '__main__':
    customers = []
    names = ['Jon Snow', 'Arya', 'Sansa', 'Ned Stark', 'Samwell', 'Tyrion', 'Jeoffrey', 'The Mountain',
             'Littlefinger', 'Stannis', 'Daenerys', 'The Hound', 'Prince Oberyn', 'Lady Margaery',
             'Cersei', 'Jaime', 'Bran', 'Hodor', 'Ghost', 'Varys']

    for i in range(0, 20):
        customers.append(Customer(names[i]))#Static size of 20 names, append and increment

    barber = Barber()
    seats = randint(1, 5)
    Closing = False
    barberShop = Shop(barber, seats, Closing)
    barberShop.openUpShop()

    while len(customers) != 0:#as long as the customer queue isn't empty, new customers will continue to enter the shop
        arrival_frequency = randint(5, 12)
        new_customer = customers.pop()
        barberShop.takeNewCustomer(new_customer)
        time.sleep(arrival_frequency)