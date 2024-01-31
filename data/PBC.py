import stft
import numpy as np
import math
from matplotlib import pyplot as plt

stft_object = stft.Stft  # creating the STFT object

# A = np.load("test1.npy")
# print(np.shape(A))
# print(A)

[t, f, s] = stft_object.stft_1(256, 256, 128, "banyo_ambient_noise.npy")  # taking STFT of the data

t = t[0:500]
s = s[:, 0:500]
[f_1, f_2] = [50, 100]  # frequency band of the falls to be determined from the experiments!!!

PBC = np.zeros(np.shape(t))  # creating the PBC array

a_1 = np.where((f <= f_2) & (f >= f_1))  # indexes of frequencies in the pos range
a_2 = np.where((f <= -f_1) & (f >= -f_2))  # indexes of frequencies in the neg range
a_3 = a_1 + a_2  # combination of both indexes

#PBC code
for i in range(len(PBC)):
    PBC[i] = np.sum(s[a_3, i])

PBC_mean = np.mean(PBC)
PBC_sd = np.std(PBC)

PBC_threshold = PBC_mean + 6 * PBC_sd  # threshold to be determined from the ambient noise!!!



indexes_PBC_passing_threshold = np.where(PBC >= PBC_threshold)

times_PBC_passing_threshold = t[indexes_PBC_passing_threshold]
# PBC code finished

plt.pcolormesh(t, f, s, vmin=0, vmax=1000, shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()