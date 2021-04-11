# import board
# import neopixel
from animations import twoDAnimations, lightAnimations
from rx import of, subject, operators
from rx.scheduler import ThreadPoolScheduler
from threading import current_thread
import time
import multiprocessing
import random

shouldIContinueSubject = subject.BehaviorSubject(True)

def intense_calculation(value):
    # sleep for a random short duration between 0.5 to 2.0 seconds to simulate a long-running calculation
    time.sleep(random.randint(5, 20) * 0.1)
    return value


# calculate number of CPUs, then create a ThreadPoolScheduler with that number of threads
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
print("OPTIMAL THREADS: ", optimal_thread_count)

# Create Process 1
shouldIContinueSubject.pipe(
    operators.map(lambda s: intense_calculation(s))
).subscribe(
    on_next=lambda s: print("PROCESS 1: {0} {1}".format(current_thread().name, s)),
    on_error=lambda e: print(e),
    on_completed=lambda: print("PROCESS 1 done!"),
    scheduler=operators.subscribe_on(pool_scheduler)
)

# Create Process 2
shouldIContinueSubject.pipe(
    operators.map(lambda s: intense_calculation(s))
).subscribe(
    on_next=lambda i: print("PROCESS 2: {0} {1}".format(current_thread().name, i)),
    on_error=lambda e: print(e),
    on_completed=lambda: print("PROCESS 2 done!"),
    scheduler=operators.subscribe_on(pool_scheduler)
)



# def change(shouldIContinue2):
#     print("Subscriber #1: ", shouldIContinue2)
#     time.sleep(5)
#     print("Subscriber 1 finished waiting")
#     # global shouldIContinue
#     shouldIContinue = shouldIContinue2

# def change2(idk):
#     print("subscriber #2: ", idk)

# shouldIContinueSubject.subscribe(change)
# shouldIContinueSubject.subscribe(change2)
for i in range(10000000):
    if(i == 8000):
        shouldIContinueSubject.on_next(False)
    if(i == 8001):
        shouldIContinueSubject.on_next(True)

print("finished for loop")

while True:
    something = 7
# # while True:
# #     translate2DPointTo1DPosition(pixels, 4, 3, (30,0,0))
# #     translate2DPointTo1DPosition(pixels, 9, 4, (0,30,0))

# while True:
#     twoDAnimations.scanningStripe(pixels, 10, 5, 0, (155,255,89))


# from rx import of, subject

# hello = of(1,2,3,'hello')
# doot = subject.Subject()


# listener1 = doot.subscribe( lambda value : print("listening to subject: ", value))

# doot.on_next('yo')
# terrible = 'terrible'

# hello.subscribe( lambda value : print(value, terrible))

# Make all of state a behavior subject

# Create a new subject every time a new animation starts so that way you could publish a stop command to the function

# Create a universal way to stop animations