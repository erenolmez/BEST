# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
#import math

data = np.load('fall_backward1.npy')

#print(np.shape(data[0,0]))
print(data[1, :])

plt.figure()
plt.plot(data[:, 2])
plt.title('?')
plt.ylabel('?')
plt.xlabel('?')
plt.show()