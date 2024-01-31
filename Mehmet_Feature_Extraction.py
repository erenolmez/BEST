import fcwt
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import math
import scipy
from scipy import signal
import fCWT
import glob
from numpy import save


def last_nonzero(arr):
    # Find indices of non-zero values
    indices = np.where(arr != 0)[0]

    if indices.size > 0:
        last_nonzero_index = np.min(indices)
        return last_nonzero_index
    else:
        return 0

f0 = 1  # lowest frequency
f1 = 1200  # highest frequency
fk = 512  # number of frequencies
fall_data = np.zeros((1, 3))
non_fall_data = np.zeros((1, 3))

for fn in glob.glob(r'C:\Users\HP\PycharmProjects\485_PBC\*.npy'):
    if 'fall' in fn:
        data = np.load(fn, allow_pickle=True)
        freqs, out = fcwt.cwt(data, 2560, f0, f1, fk)

        freqs = freqs[10:-10]

        time_instances = np.linspace(0, 10, 25728)
        time_instances = time_instances[120:-120]

        abs_out = np.abs(out)
        abs_out = abs_out[10:-10:, 120:-120]

        f_index_1 = 296
        f_index_2 = 399

        f = freqs[f_index_1:f_index_2]
        o = abs_out[f_index_1:f_index_2][:]
        o = o.sum(0)
        fall_index = np.argmax(o)
        time_window = time_instances[fall_index - 2573: fall_index + 2573]  # 2s
        o_window = o[fall_index - 2573: fall_index + 2573]  # 2s
        o_energy = np.sum(np.square(o_window))

        abs_out = abs_out * (abs_out > 0.00050)   # Thresholding used here
        maxfreqs = np.zeros(25488)
        motion_detected_freqs = np.zeros(25488)

        for i in range(25488):
            maxval = abs_out[:, i].max()
            maxarg = abs_out[:, i].argmax()

            maxfreq = freqs[maxarg]
            maxfreqs[i] = maxfreq
            detected_mot = last_nonzero(abs_out[:, i])
            detected_mot = freqs[detected_mot]
            motion_detected_freqs[i] = detected_mot

            maxfreqs = maxfreqs * (maxfreqs < 1000)
            motion_detected_freqs = motion_detected_freqs * (motion_detected_freqs < 1000)

        fall_data = np.vstack((fall_data, np.array([o_energy, maxfreqs.max(), motion_detected_freqs.max()])))

    if 'stand' in fn:
        data = np.load(fn, allow_pickle=True)
        freqs, out = fcwt.cwt(data, 2560, f0, f1, fk)

        freqs = freqs[10:-10]

        time_instances = np.linspace(0, 10, 25728)
        time_instances = time_instances[120:-120]

        abs_out = np.abs(out)
        abs_out = abs_out[10:-10:, 120:-120]

        f_index_1 = 296
        f_index_2 = 399

        f = freqs[f_index_1:f_index_2]
        o = abs_out[f_index_1:f_index_2][:]
        o = o.sum(0)
        fall_index = np.argmax(o)
        time_window = time_instances[fall_index - 2573: fall_index + 2573]  # 2s
        o_window = o[fall_index - 2573: fall_index + 2573]  # 2s
        o_energy = np.sum(np.square(o_window))

        abs_out = abs_out * (abs_out > 0.00050)   # Thresholding used here
        maxfreqs = np.zeros(25488)
        motion_detected_freqs = np.zeros(25488)

        for i in range(25488):
            maxval = abs_out[:, i].max()
            maxarg = abs_out[:, i].argmax()
            maxfreq = freqs[maxarg]
            maxfreqs[i] = maxfreq
            detected_mot = last_nonzero(abs_out[:, i])
            detected_mot = freqs[detected_mot]
            motion_detected_freqs[i] = detected_mot

            maxfreqs = maxfreqs * (maxfreqs < 1000)
            motion_detected_freqs = motion_detected_freqs * (motion_detected_freqs < 1000)

        non_fall_data = np.vstack((non_fall_data, np.array([o_energy, motion_detected_freqs.max(), maxfreqs.max()])))

fall_data = fall_data[1:]
non_fall_data = non_fall_data[1:]

save('mehmet_features_dusus', fall_data)
save('mehmet_features_no_dusus', non_fall_data)
