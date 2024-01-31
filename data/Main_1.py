# Rahman ve Rahim olan Allahın adı ile

import stft
import numpy as np
import math
from matplotlib import pyplot as plt

stft_object = stft.Stft  # creating the STFT object

data = "fall_demo1.npy"

[t, f, s] = stft_object.stft_1(256, 256, 128, data)  # taking STFT of the data
#[t, f, s] = stft_object.stft(256, 256, 128, data)  # taking STFT of the data

[f_1, f_2] = [70, 100]  # frequency band of the falls to be determined from the experiments!!!

def pbc(t, s):
    PBC = np.zeros(np.shape(t))  # creating the PBC array

    a_1 = np.where((f <= f_2) & (f >= f_1))  # indexes of frequencies in the pos range
    a_2 = np.where((f <= -f_1) & (f >= -f_2))  # indexes of frequencies in the neg range
    a_3 = a_1 + a_2  # combination of both indexes

    for i in range(len(PBC)):
        PBC[i] = np.sum(s[a_3, i])
    return PBC

def image_segmentation_and_noise(s):
    # Display the noise region and its mean and variance
    # plt.imshow(noise_region, cmap='gray')
    # plt.title('Noise region (mean={}, var={})'.format(noise_mean, noise_var))
    filtered_matrix = np.zeros_like(s)
    filtered_matrix[s <= 0.8] = s[s <= 0.8]
    noise_region = s[0:110, 0:55]

    # Extract the values of the noise-only region
    noise_values = noise_region.flatten()

    # Calculate the mean and variance of the noise values
    noise_mean = np.mean(noise_values)
    noise_var = np.var(noise_values)

    threshold = noise_mean + 1.5 * (math.sqrt(noise_var))
    PBC_threshold = noise_mean + 6 * np.sqrt(noise_var)

    binarized_s = (s >= threshold) * 1
    return binarized_s, PBC_threshold

def image_segmentation_and_noise_new(s):
    # Display the noise region and its mean and variance
    # plt.imshow(noise_region, cmap='gray')
    # plt.title('Noise region (mean={}, var={})'.format(noise_mean, noise_var))
    row = int(s.shape[0] * 465 / 1000)
    column = int(s.shape[1] * 1 / 2)
    noise_region = s[0:row, 0: column]

    # Extract the values of the noise-only region
    noise_values = noise_region.flatten()

    # Calculate the mean and variance of the noise values
    noise_mean = np.mean(noise_values)
    noise_var = np.var(noise_values)

    # plt.imshow(noise_region, cmap='gray')

    threshold = noise_mean + 1.5 * (math.sqrt(noise_var))
    PBC_threshold = noise_mean + 6 * np.sqrt(noise_var)

    binarized_s = (s >= threshold) * 1
    return threshold, binarized_s, PBC_threshold

def feature_extraction(t, s):
    rows, cols = np.where(s == 1)

    f_min = f[np.min(rows)]  # minimum negative frequency
    f_max = f[np.max(rows)]  # maximum negative frequency

    F = np.max(np.array([f_max, -f_min]))  # first feature(extreme frequency magnitude)

    f1 = np.abs(f_max/f_min)
    f2 = np.abs(1/f1)

    R = np.max(np.array([f1, f2]))  # second feature(extreme frequency ratio)

    t_min = t[cols[0]]  # time of the minimum frequency
    t_max = t[cols[np.shape(cols)[0]-1]]  # time of the maximum frequency
    t_begin = t[len(t)//2] # starting time of the event

    # if t_min == t_max:
    #     print("As expected")
    # else:
    #     print("Smth might me wrong")

    L = t_max - t_begin  # third feature(length of event)
    Features = [F, R, L]  # all features
    return Features

PBC_max = np.max(pbc(t, s)) # max PBC value expected to occur at fall
fall_index = np.where(pbc(t, s) == PBC_max)[0][0]

# to find how many indexes refer to 2s
bn = math.floor(t[-1])
bn = bn//2
bn = len(t)//bn  # how many indexes refer to 2s

time_window = t[fall_index - bn: fall_index + bn + 1]  # 4s
s_window = s[:, fall_index - bn: fall_index + bn + 1]

binarized_s = image_segmentation_and_noise_new(s_window)[1]  # window data
binarized_s_1 = image_segmentation_and_noise_new(s)[1]   # full data

threshold = image_segmentation_and_noise_new(s_window)[0]
threshold_1 = image_segmentation_and_noise_new(s)[0]
PBC_threshold = image_segmentation_and_noise_new(s_window)[2]

Features = feature_extraction(time_window, binarized_s)

# save('features.npy', Features)
#
#
#Datas = np.zeros(())
print(Features)
# print(PBC_threshold)
# PBC plot
plt.figure()
plt.plot(t, pbc(t, s))
plt.title("PBC of the time window")
plt.ylabel('PBC value')
plt.xlabel('Time [sec]')

plt.figure()
# Image Segmentation plot
plt.title("Otsu Threshold Method: >"+str(threshold))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.pcolormesh(time_window, f, binarized_s, shading='gouraud')
#
# plt.figure()
# # Image Segmentation plot
# plt.title("Otsu Threshold Method: >"+str(threshold_1))
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.pcolormesh(t, f, binarized_s_1, shading='gouraud')
#
plt.figure()
# STFT plot
plt.pcolormesh(t, f, s, vmin=0, vmax=1000, shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()