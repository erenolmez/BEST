#%%
import time
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('tkagg')
import matplotlib.animation as animation
import os
import mmap
import fcwt
import socket
       
      

fs = 2000
n = fs*10 #10 seconds
f0 = 1 #lowest frequency
f1 = 1200 #highest frequency
fn = 512 #number of frequencies
abs_val = np.load("ege_fall_backward_arm2.npy")


#... or calculate and plot CWT
freqs, out = fcwt.cwt(abs_val,2560,f0,f1,fn)
# plt.pcolormesh(np.linspace(0,10,25728), freqs, np.abs(out))
f = freqs[350:500]
o = np.abs(out)
o = o[350:500][:]
o = o.sum(0)
plt.pcolormesh(np.linspace(0,10,25728),freqs,np.abs(out),vmax=0.02)

plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
# %%
