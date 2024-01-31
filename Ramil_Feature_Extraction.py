import glob
import time
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import math
import scipy
#import pywt
from scipy import signal
from numpy import save
# %%
class SignalProcessing:
    # def _init_(self,fft_size,window_sample_num,overlap_window,raw_data,freq=2000):
    #     self.raw_data = np.load(raw_data)
    #     self.fft_size = fft_size
    #     self.window_sample_num = window_sample_num
    #     self.overlap_window = overlap_window
    #     x = window_sample_num
    #     number_of_x = 0
    #     while(len(self.raw_data[0]) >= x):
    #         x += window_sample_num - overlap_window
    #         number_of_x = number_of_x +1
    #     self.x = number_of_x
    #     print(self.x)
    #     self.time_array = np.linspace(0,len(self.raw_data[0])/freq,number_of_x)
    #     self.freq_array = np.linspace(-freq/2,freq/2,fft_size)
    #     self.spectrum = np.zeros((fft_size,number_of_x))
    #     self.spectogram = np.zeros((fft_size,number_of_x))
    def stft(fft_size, window_sample_num, overlap_window, raw_data, freq=2000):
        fft_size = fft_size
        window_sample_num = window_sample_num
        overlap_window = overlap_window
        x = window_sample_num
        number_of_x = 0
        while (raw_data.size >= x):
            x += window_sample_num - overlap_window
            number_of_x = number_of_x + 1
        x = number_of_x
        print(x)
        time_array = np.linspace(0, raw_data.size / freq, number_of_x)
        freq_array = np.linspace(-freq / 2, freq / 2, fft_size)
        spectrum = np.zeros((fft_size, number_of_x))
        spectogram = np.zeros((fft_size, number_of_x))
        # Taking absolute values of raw data
        abs_val_array = raw_data
        abs_mean = np.mean(abs_val_array)
        abs_val_array = abs_val_array - abs_mean
        abs_val_array = abs_val_array * 100000
        print(len(abs_val_array))
        current_window_index = 0
        for i in range(x):
            current_window_index += window_sample_num - overlap_window
            fft_window = abs_val_array[current_window_index:current_window_index + window_sample_num]
            print(len(fft_window))
            while (len(fft_window) != fft_size):
                # zero padding in the case fft size is not equal to window size
                fft_window = np.append(fft_window, 0)
                # Using Hamming function
            hann_win = scipy.signal.hamming(fft_size, sym=True)
            hammed_data = fft_window * hann_win
            scale = 1.0 / ((hann_win).sum() ** 2)
            scale = np.sqrt(scale)
            fft_data = np.fft.fft(hammed_data)
            fft_data = np.abs(fft_data)
            centered_fft = np.zeros(fft_size)
            centered_fft[0:fft_size // 2] = fft_data[fft_size // 2:fft_size]
            centered_fft[fft_size // 2:fft_size] = fft_data[0:fft_size // 2]
            spectrum[:, i] = centered_fft
            spectrum[:, i] *= scale
            spectogram[:, i] = abs(spectrum[:, i]) ** 2
            print(centered_fft[10])
        return time_array, freq_array, spectogram

    def MorletWavelet(data, wavelet_name, sampling_frequency=2000):

        # Currently only supported for Morlet wavelets
        if wavelet_name == 'morl':
            data -= np.mean(data)
            n_orig = data.size
            nv = 10
            ds = 1 / nv
            fs = sampling_frequency
            dt = 1 / fs

            # Pad data symmetrically
            padvalue = n_orig // 2
            x = np.concatenate((np.flipud(data[0:padvalue]), data, np.flipud(data[-padvalue:])))
            n = x.size

            # Define scales
            _, _, wavscales = SignalProcessing.getDefaultScales(wavelet_name, n_orig, ds)
            num_scales = wavscales.size

            # Frequency vector sampling the Fourier transform of the wavelet
            omega = np.arange(1, math.floor(n / 2) + 1, dtype=np.float64)
            omega *= (2 * np.pi) / n
            omega = np.concatenate(
                (np.array([0]), omega, -omega[np.arange(math.floor((n - 1) / 2), 0, -1, dtype=int) - 1]))

            # Compute FFT of the (padded) time series
            f = np.fft.fft(x)

            # Loop through all the scales and compute wavelet Fourier transform
            psift, freq = SignalProcessing.waveft(wavelet_name, omega, wavscales)

            # Inverse transform to obtain the wavelet coefficients.
            cwtcfs = np.fft.ifft(np.kron(np.ones([num_scales, 1]), f) * psift)
            cfs = cwtcfs[:, padvalue:padvalue + n_orig]
            freq = freq * fs

            return cfs, freq
        else:
            raise Exception

    def getDefaultScales(wavelet, n, ds):
        """
        getDefaultScales(wavelet, n, ds)
        Calculate default scales given a wavelet and a signal length.
        Parameters
        ----------
        wavelet : string
            Name of wavelet
        n : int
            Number of samples in a given signal
        ds : float
            Scale resolution (inverse of number of voices in octave)
        Returns
        -------
        s0 : int
            Smallest useful scale
        ds : float
            Scale resolution (inverse of number of voices in octave). Here for legacy reasons; implementing more wavelets
            will need this output.
        scales : array_like
            Array containing default scales.
        """
        wname = wavelet
        nv = 1 / ds

        if wname == 'morl':

            # Smallest useful scale (default 2 for Morlet)
            s0 = 2

            # Determine longest useful scale for wavelet
            max_scale = n // (np.sqrt(2) * s0)
            if max_scale <= 1:
                max_scale = n // 2
            max_scale = np.floor(nv * np.log2(max_scale))
            a0 = 2 ** ds
            scales = s0 * a0 ** np.arange(0, max_scale + 1)
        else:
            raise Exception

        return s0, ds, scales

    def waveft(wavelet, omega, scales):
        """
        waveft(wavelet, omega, scales)
        Computes the Fourier transform of a wavelet at certain scales.
        Parameters
        ----------
        wavelet : string
            Name of wavelet
        omega : array_like
            Array containing frequency values in Hz at which the transform is evaluated.
        scales : array_like
            Vector containing the scales used for the wavelet analysis.
        Returns
        -------
        wft : array_like
            (num_scales x num_freq) Array containing the wavelet Fourier transform
        freq : array_like
            Array containing frequency values
        """
        wname = wavelet
        num_freq = omega.size
        num_scales = scales.size
        wft = np.zeros([num_scales, num_freq])

        if wname == 'morl':
            gC = 6
            mul = 2
            for jj, scale in enumerate(scales):
                expnt = -(scale * omega - gC) ** 2 / 2 * (omega > 0)
                wft[jj,] = mul * np.exp(expnt) * (omega > 0)

            fourier_factor = gC / (2 * np.pi)
            frequencies = fourier_factor / scales

        else:
            raise Exception

        return wft, frequencies

        # self.y2data[0:self.count] = self.y2data[self.count:2*self.count]
        # self.y2data[self.count:2*self.count] = abs_val
        # hammed_data = self.y2data * np.hamming(2*self.count)
        # y1_data = np.fft.fft(hammed_data)
        # y1_data = np.abs(y1_data)
        # centered_y = np.zeros(2*self.count)
        # centered_y[0:self.count] = y1_data[self.count:2*self.count]
        # centered_y[self.count:2*self.count] = y1_data[0:self.count]
        # self.stft = np.vstack((self.stft,centered_y))
        # np.save('abcd.npy', self.stft)


fall_data = np.zeros((1, 3))
non_fall_data = np.zeros((1, 3))




def feature_extraction_ramil(data,sec):
    data_size = data.size
    fs = 2560
    [out, freq] = SignalProcessing.MorletWavelet(data, "morl", fs)

    # First feature o_energy
    f = freq[13:33]  # selected frequencies
    o = np.abs(out[13:33][:])
    o = o.sum(0)
    o_max = np.max(o)  # max PBC value expected to occur at fall

    time_instances = np.linspace(0, sec, data_size)
    fall_index = np.where(o == o_max)[0][0]
    time_window = time_instances[fall_index - 2573: fall_index + 2573]  # 2s
    o_window = o[fall_index - 2573: fall_index + 2573]  # 2s

    o_energy = np.sum(np.square(o_window))

    # Second feature last_detected_frequency
    abs_out = np.abs(out)
    abs_out = abs_out[:, 5:-5]
    abs_out = abs_out * (abs_out >= 0.0008)
    not_purple_index = np.where(abs_out >= 0.0008)
    

    if np.any(not_purple_index) == True:

        a = not_purple_index[0]
        b = not_purple_index[1]

        c = np.argmin(a)
        last_detected_frequency = freq[a[c]]

        # Third feature max_freq
        max_arg = abs_out.argmax(0)
        # max_freq = freq[np.min(max_arg)]
        #max_freq = freq[np.min(max_arg)]

        maxfreqs = freq[max_arg]
        maxfreqs = maxfreqs * (maxfreqs < 1000)
        max_freq = maxfreqs.max()

    else:
        max_freq = 0
        last_detected_frequency = 0

    features = np.array([o_energy, last_detected_frequency, max_freq])
    return features

# for fn in glob.glob(r'C:\Users\HP\PycharmProjects\485_PBC\*.npy'):

#     if 'fall' in fn:
#         data = np.load(fn, allow_pickle=True)
#         fall_data = np.vstack((fall_data, feature_extraction_ramil(data)))

        # fs = 2560
        # [out, freq] = SignalProcessing.MorletWavelet(data, "morl", fs)
        #
        # # First feature o_energy
        # f = freq[13:33]  # selected frequencies
        # o = np.abs(out[13:33][:])
        # o = o.sum(0)
        # o_max = np.max(o)  # max PBC value expected to occur at fall
        #
        # time_instances = np.linspace(0, 10, 25728)
        # fall_index = np.where(o == o_max)[0][0]
        # time_window = time_instances[fall_index - 2573: fall_index + 2573]  # 2s
        # o_window = o[fall_index - 2573: fall_index + 2573]  # 2s
        #
        # o_energy = np.sum(np.square(o_window))
        #
        # # Second feature last_detected_frequency
        # abs_out = np.abs(out)
        # abs_out = abs_out[:, 5:-5]
        # not_purple_index = np.where(abs_out >= 0.0008)
        #
        # a = not_purple_index[0]
        # b = not_purple_index[1]
        #
        # c = np.argmin(a)
        # last_detected_frequency = freq[a[c]]
        #
        # # Third feature max_freq
        # max_arg = abs_out.argmax(0)
        # max_freq = freq[np.min(max_arg)]
        #
        # #maxfreqs = freq[max_arg]
        # #maxfreqs = maxfreqs * (maxfreqs < 1000)
        # #max_freq = maxfreqs.max()
        #
        # fall_data = np.vstack((fall_data, np.array([o_energy, last_detected_frequency, max_freq])))

    # if 'stand' in fn:
    #     data = np.load(fn, allow_pickle=True)
    #     non_fall_data = np.vstack((non_fall_data, feature_extraction_ramil(data)))
        # fs = 2560
        # [out, freq] = SignalProcessing.MorletWavelet(data, "morl", fs)
        #
        # # First feature o_energy
        # f = freq[13:33]  # selected frequencies
        # o = np.abs(out[13:33][:])
        # o = o.sum(0)
        # o_max = np.max(o)  # max PBC value expected to occur at fall
        #
        # time_instances = np.linspace(0, 10, 25728)
        # fall_index = np.where(o == o_max)[0][0]
        # time_window = time_instances[fall_index - 2573: fall_index + 2573]  # 2s
        # o_window = o[fall_index - 2573: fall_index + 2573]  # 2s
        #
        # o_energy = np.sum(np.square(o_window))
        #
        # # Second feature last_detected_frequency
        # abs_out = np.abs(out)
        # abs_out = abs_out[:, 5:-5]
        # not_purple_index = np.where(abs_out >= 0.0008)
        #
        # a = not_purple_index[0]
        # b = not_purple_index[1]
        #
        # c = np.argmin(a)
        # last_detected_frequency = freq[a[c]]
        #
        # # Third feature max_freq
        # max_arg = abs_out.argmax(0)
        # max_freq = freq[np.min(max_arg)]
        #
        # # maxfreqs = freq[max_arg]
        # # maxfreqs = maxfreqs * (maxfreqs < 1000)
        # # max_freq = maxfreqs.max()
        #
        # non_fall_data = np.vstack((non_fall_data, np.array([o_energy, last_detected_frequency, max_freq])))
