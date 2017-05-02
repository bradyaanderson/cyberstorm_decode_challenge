import time
from datetime import timedelta

# saves current time
start_time = time.time()

# total time of timer in seconds
total_time = 5

time_left = True

# prints out formatted time left until time runs out
while time_left:
    current_time_left = total_time - time.time() + start_time
    if current_time_left > 0:
        print str(timedelta(seconds=current_time_left+1))[3:7]
    else:
        print '0:00'
        time_left = False
