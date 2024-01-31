# Rahman ve Rahim olan Allahın adı ile

import numpy as np
window_frequencies = np.array([-3,-2,-1,1,2,3]) # window frequencies defined here


f_max = np.max(window_frequencies) # maximum positive frequency

f_min = - np.max(-window_frequencies) # minimum negative frequency

F = np.max(np.array([f_max,-f_min])) # first feature(extreme frequency magnitude)

f1 = np.abs(f_max/f_min)

f2 = np.abs(1/f1)

R = np.max(np.array([f1,f2])) # second feature(extreme frequency ratio)

#t_begin = k*T # T is the time step and kth time step is where the PBC passes the threshold

# t_extreme = np.where(np.abs(window_frequencies) == F) I don't know how the extreme frequency is defined.
# print(t_extreme)
