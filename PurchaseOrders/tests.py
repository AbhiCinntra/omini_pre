from django.test import TestCase

# Create your tests here.
import threading

def print_numbers():
    temparr= []
    for i in range(5):
        print(f"Thread 1: {i}")
        # temparr.append(i)
    # print("print_numbers", temparr)

def print_letters():
    temparr= []
    for letter in 'ABCDE':
        print(f"Thread 2: {letter}")
        # temparr.append(letter)
    # print("print_letters", temparr)

# Create two threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
# thread1.join()
# thread2.join()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# from multiprocessing import Process

# def print_numbers():
#     for i in range(5):
#         print(f"Process 1: {i}")

# def print_letters():
#     for letter in 'ABCDE':
#         print(f"Process 2: {letter}")

# # Create two processes
# process1 = Process(target=print_numbers)
# process2 = Process(target=print_letters)

# # Start the processes
# process1.start()
# process2.start()

# Wait for both processes to finish
# process1.join()
# process2.join()
