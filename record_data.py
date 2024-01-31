#%%
import time
import numpy as np
import os
import mmap
import socket
from pipe_reader import PlotFromPipe
import sys
#%%
readobj = PlotFromPipe("fifo")
time1 = 10
time_elapsed = 0
readobj.predict_fall(10)
# while(True):
#     readobj.print()
    
    # if (time_elapsed < 2):
    #     time1 = 10
    # else:
    #     time1 = time_elapsed
    # readobj.print()

#%%
