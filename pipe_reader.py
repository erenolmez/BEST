

#%%
import time
import numpy as np
import socket
from matplotlib import pyplot as plt
import os
import Ramil_Feature_Extraction
import Eren_Machine_Learning
import threading
#import matplotlib
#matplotlib.use('tkagg')
#import matplotlib.animation as animation

# import fcwt
# import raw_stft

#%%

def clear():
    os.system( 'cls' )
#%%
class ReadFromPipe:
    value_array = np.array([])
    time_array = np.array([])
    def __init__(self, pipe_name,sleep_value = 0.0001,count=128,sec = 5):
        self.pipe_name = pipe_name
        self.fd = open(self.pipe_name,"r")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1.0)
        self.host = "139.179.42.27"  # Replace with the server's IP address or hostname
        # self.port1 = 8890  # Replace with the server's port number
        self.port2 = 8888
        # self.fd1 = open("a.txt","a+")
        # self.sleep_value = sleep_value
        # self.count = count
        # self.sec = sec
        # self.total_bytes_read = 0
        # self.frame_number = 0
        # self.fname = './pods.txt'
        # if not os.path.isfile(self.fname):
        #     # create initial file
        #     with open(self.fname, "w+b") as fd:
        #         fd.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        # self.f2 = open(self.fname, "r+b")
        # self.mm = mmap.mmap(self.f2.fileno(), 8, access=mmap.ACCESS_WRITE, offset=0)       
        
    def my_thread_function(self):
        while(True):
            data = self.return_one_frame()
            try:
                self.client_socket.sendto(data.encode(), (self.host, self.port2))
            except socket.timeout:
                print("Timeout occurred, retrying...")
        
        # print("Thread is running")
        
    def threadd(self):
        my_thread = threading.Thread(target = self.my_thread_function)
        my_thread.start()


    def print_numpy_arrays(self):
        while(True):
            data = self.fd.read(2319)
            real_array = np.fromstring(data[11:1162], dtype=float, sep=',')
            complex_array = np.fromstring(data[1165:2316], dtype=float, sep=',')
            print(real_array)
            print(complex_array)
                         
    def print(self):
        while(True):
            data = self.fd.read(2319)
            # print(data)
            
    def return_one_frame(self):
        data = self.fd.read(2319)
        return data
    
    def return_data(self):
            data = self.fd.read(2319)
            # self.client_socket.sendto(data.encode(), (self.host, self.port2))
            # try:
            #     self.client_socket.sendto(data.encode(), (self.host, self.port2))
            # except socket.timeout:
            #     print("Timeout occurred, retrying...")
            real_array = np.fromstring(data[11:1162], dtype=float, sep=',')
            complex_array = np.fromstring(data[1165:2316], dtype=float, sep=',')
            return real_array,complex_array
    
    def record_data(self,sec,name):
        real_data = np.zeros(128*(sec*20+1))
        complex_data = np.zeros(128*(sec*20+1))
        time_array = np.linspace(0,sec,real_data.size)
        data = self.return_data()
        print("Recording is started")
        init_time = time.time()
        i = 0
        while(time.time() <= init_time + sec):
            r,c = self.return_data()
            real_data[i*128:(i+1)*128] = r
            complex_data[i*128:(i+1)*128] = c
            i = i+1
        print(i)
        
        abs_data = real_data**2 + complex_data**2
        abs_data = np.sqrt(abs_data)
        
        np.save(name,abs_data)
        # plt.plot(abs_data)
        # plt.show()
        
        return
    
    def return_secs_of_data(self,sec):
        real_data = np.zeros(128*(int(sec*120)+10))
        complex_data = np.zeros(128*(int(sec*120) + 10))
        r,c = self.return_data()
        init_time = time.time()
        i = 0
        real_data[i*128:(i+1)*128] = r
        complex_data[i*128:(i+1)*128] = c
        i = 1
        while(time.time() <= init_time + sec):
            r,c = self.return_data()
            real_data[i*128:(i+1)*128] = r
            complex_data[i*128:(i+1)*128] = c
            i = i+1
        real_data = real_data[:i*128]
        complex_data = complex_data[:i*128]
        abs_data = real_data**2 + complex_data**2
        abs_data = np.sqrt(abs_data)
        return abs_data
    
    
    def return_features(self,sec):
        abs_data = self.return_secs_of_data(sec)
        time1 = time.time()
        features = Ramil_Feature_Extraction.feature_extraction_ramil(abs_data,sec)
        print(features)
        elapsed_time = time.time() - time1
        print(f"elpased time for feature extraction = {elapsed_time}")
        return features, elapsed_time
        
        
    def predict_fall(self,sec):
        Eren_ML_object = Eren_Machine_Learning.KNN()    
        elapsed_time = 0
        # self.threadd()


        while 1:
            features = self.return_features(sec-elapsed_time) 
            features_0 = features[0]
            # message = f"{features_0[0]},{features_0[1]},{features_0[2]}"
            # try:
            #     self.client_socket.sendto(message.encode(), (self.host, self.port1))
            # except socket.timeout:
            #     print("Timeout occurred, retrying...")
            
            time1 = features[1]
            time2 = time.time()
            Eren_ML_object.predicton_based_on_feature_extraction(features_0)
            time3 = time.time() - time2
            elapsed_time = time1 + time3
            print(f"elapsed time for machine learning + feature extraction {elapsed_time}")
            
        self.client_socket.close()
        
    
    
    def send_values_to_pc(self):
        ip_addr = "139.179.221.48"
        port = 8000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def close(self):
        
# connect the socket to the server's address and port
        server_address = (ip_addr, port)
        sock.connect(server_address)
        while(True):
                message = self.return_one_frame()
                sock.sendall(message.encode())

        
        abs_val = np.sqrt(real_data**2 + complex_data**2)
        # #fig1 = plt.figure()
        # #plt.plot(abs_val)
        # #plt.xlabel("Time (s)")
        # #plt.ylabel("Magnitude")
        # #plt.title('Sine')
        file = f"Time-Series_Data/{name}.npy".format(name=name)
        np.save(file,abs_val)
	
	    
        
        # fig2 = plt.figure()
        # init_time = time.time()
        # times,frequencies,spectogram = raw_stft.SignalProcessing.stft(256,256,128,abs_val,2560)
        # elapsed_time = time.time() - init_time
        # print("elapsed time for stft : ",elapsed_time)
        # plt.pcolormesh(times, frequencies, spectogram,vmin=0,vmax=1000)
        # plt.title("stft Graph of raw data")
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # file = f"STFT/{name}.png".format(name=name)
        # plt.savefig(file)
        
        # fig3 = plt.figure()
        # init_time = time.time()
        # frequencies,spectogram = fcwt.cwt(abs_val,2560,1,640,640)
        # elapsed_time = time.time() - init_time
        # print("elapsed time for CWT : ",elapsed_time)
        # plt.pcolormesh(time_array, frequencies, np.abs(spectogram))
        # plt.title("CWT Graph of raw data")
        # plt.ylabel('Frequency [Hz]')
        # plt.xlabel('Time [sec]')
        # file = f"CWT/{name}.png".format(name=name)
        # plt.savefig(file)
        
        
        #plt.show()
        


class PlotFromPipe(ReadFromPipe):
    def __init__(self, pipe_name,sleep_value = 0.0001,count=128,sec = 5):
        super().__init__(pipe_name,sleep_value = 0.0001,count=128,sec = 5)



    def animate(self,i):

        #real_values = self.return_raw_data(0,2)
        #complex_values = self.return_raw_data(1,2)
        real_values, complex_values = self.return_data()

        # vel_values = self.return_velocity()
        x_data = np.arange(self.count) + self.count*i*np.ones(self.count)
        

        if(self.count*i >= (self.x_upper_bound - self.window_swap_ratio*self.window_size)):
            self.x_upper_bound = self.x_upper_bound + self.window_add_size_every_swap
            self.axis.set_xlim(self.x_upper_bound - self.window_size,self.x_upper_bound)
            self.xdata = self.xdata[self.window_add_size_every_swap:]
            self.ydata = self.ydata[self.window_add_size_every_swap:]
            self.y1data = self.y1data[self.window_add_size_every_swap:]
            

        self.xdata = np.concatenate((self.xdata,x_data))
        self.ydata = np.concatenate((self.ydata,real_values))
        self.y1data = np.concatenate((self.y1data,complex_values))

        self.line1.set_data(self.xdata,self.ydata)
        self.line2.set_data(self.xdata,self.y1data)
        return self.line1,self.line2
    
    def animate1(self,i):

        #real_values = self.return_raw_data(0,2)
        #complex_values = self.return_raw_data(1,2)
        real_values, complex_values = self.return_data()

        # vel_values = self.return_velocity()
        x_data = np.arange(self.count) + self.count*i*np.ones(self.count)
        

        if(self.count*i >= (self.x_upper_bound - self.window_swap_ratio*self.window_size)):
            self.x_upper_bound = self.x_upper_bound + self.window_add_size_every_swap
            self.ax1.set_xlim(self.x_upper_bound - self.window_size,self.x_upper_bound)
            self.ax2.set_xlim(self.x_upper_bound - self.window_size,self.x_upper_bound)     
            self.xdata = self.xdata[self.window_add_size_every_swap:]
            self.ydata = self.ydata[self.window_add_size_every_swap:]
            self.y1data = self.y1data[self.window_add_size_every_swap:]
            

        self.xdata = np.concatenate((self.xdata,x_data))
        self.ydata = np.concatenate((self.ydata,real_values))
        self.y1data = np.concatenate((self.y1data,complex_values))

        self.line1.set_data(self.xdata,self.ydata)
        self.line2.set_data(self.xdata,self.y1data)
        return self.line1,self.line2
    
    
    def animate2(self,i):

        #real_values = self.return_raw_data(0,2)
        #complex_values = self.return_raw_data(1,2)
        real_values, complex_values = self.return_data()
        abs_val = np.sqrt(real_values**2 + complex_values**2)
        abs_val = abs_val
        sum_val = real_values + complex_values
        
                

        # vel_values = self.return_velocity()
        # x_data = list(range(self.count*i,self.count*(i+1)))
        self.y2data[0:self.count] = self.y2data[self.count:2*self.count]
        self.y2data[self.count:2*self.count] = abs_val
        hammed_data = self.y2data * np.hamming(2*self.count)
        y1_data = np.fft.fft(hammed_data)
        y1_data = np.abs(y1_data)
        centered_y = np.zeros(2*self.count)
        centered_y[0:self.count] = y1_data[self.count:2*self.count]
        centered_y[self.count:2*self.count] = y1_data[0:self.count]
        self.stft = np.vstack((self.stft,centered_y))
        np.save('abcd.npy', self.stft)  
        
        

        # if(self.count*i >= (self.x_upper_bound - self.window_swap_ratio*self.window_size)):
        #     self.x_upper_bound = self.x_upper_bound + self.window_add_size_every_swap
        #     self.ax1.set_xlim(self.x_upper_bound - self.window_size,self.x_upper_bound)
        #     # self.ax2.set_xlim(self.x_upper_bound - self.window_size,self.x_upper_bound)     
        #     self.xdata = self.xdata[self.window_add_size_every_swap:]
        #     self.ydata = self.ydata[self.window_add_size_every_swap:]
        #     # self.y1data = self.y1data[self.window_add_size_every_swap:]
            
        
            

        self.ydata[0:200*128] = self.ydata[128:201*128]
        self.ydata[200*128:201*128] = real_values  
        # self.ydata = self.ydata + real_values
        # self.ydata = np.concatenate((self.ydata,real_values))
        self.y1data = centered_y

        self.line1.set_data(self.xdata,self.ydata)
        self.line2.set_data(self.x1data,self.y1data)
        return self.line1,self.line2


    
    def real_time_animation(self):
        ani = animation.FuncAnimation(self.fig,self.animate,interval =50,blit = True)
        plt.show()
    
    def real_time_complex_animation(self):
        self.fig = plt.figure()
        self.window_size = 40000
        self.x_upper_bound = 40000
        self.window_swap_ratio = 1/4
        self.window_add_size_every_swap = 20000
        self.axis = plt.axes(xlim =(self.x_upper_bound - self.window_size, self.x_upper_bound),ylim =(-0.05,1.05))
        self.line1, = self.axis.plot(np.array([]), np.array([]),'-b',label="Real Data", lw = 2)
        self.axis2 = self.axis.twinx()
        self.line2, = self.axis2.plot(np.array([]), np.array([]),'-r',label = "Complex Data" ,lw = 2) 
        self.line1.set_data(np.array([]),np.array([]))
        self.line2.set_data(np.array([]),np.array([]))
        self.xdata = np.array([])
        self.y1data = np.array([])
        self.ydata = np.array([])
        self.axis.legend([self.line1, self.line2], [self.line1.get_label(), self.line2.get_label()], loc=0)
 
        self.axis.set_xlabel("X")
        plt.title("Real time Plot of raw data of Sense2Gol Pulse Radar")
        plt.xlabel("Samples")
        plt.ylabel("Radar Readings")
        ani = animation.FuncAnimation(self.fig,self.animate,interval =50,blit = True)
        plt.show()
    
    def real_and_complex_subplot(self):

        self.fig,(self.ax1,self.ax2) = plt.subplots(2,1)
        self.fig.set_figheight(6)
        self.fig.set_figwidth(10)
        plt.figure(figsize=(10,6))
        self.window_size = 40000
        self.x_upper_bound = 40000
        self.window_swap_ratio = 1/4
        self.window_add_size_every_swap = 20000
        # self.window_size = window_size
        # self.x_upper_bound = upper_bound
        # self.window_swap_ratio = window_swap_ratio
        # self.window_add_size_every_swap = window_add_size_every_swap

        self.line1, =self.ax1.plot(np.array([]), np.array([]),'-b',lw=2) 
        self.line2, =self.ax2.plot(np.array([]), np.array([]),'-b',lw=2) 
        self.line1.set_data(np.array([]),np.array([]))
        self.line2.set_data(np.array([]),np.array([]))

        self.xdata = np.array([])
        self.y1data = np.array([])
        self.ydata = np.array([])
        for ax in [self.ax1, self.ax2]:
            ax.set_ylim(-0.05, 1.05)
            ax.set_xlim(self.x_upper_bound - self.window_size, self.x_upper_bound)

        self.ax1.set_xlabel("Sample Count")
        self.ax2.set_xlabel("Sample Count")
        self.ax1.set_ylabel("Sensor Readings (Real Part)")
        self.ax2.set_ylabel("Sensor Readings (Complex Part)")
        self.ax1.set_title("Real time Plot of raw data of Sense2Gol Pulse Radar")
        ani = animation.FuncAnimation(self.fig,self.animate1,interval =50,blit = True)
        plt.show()
    
    def abs_and_dft(self):
        
        self.fig,(self.ax1,self.ax2) = plt.subplots(2,1)
        self.fig.set_figheight(6)
        self.fig.set_figwidth(10)
        plt.figure(figsize=(10,6))
        # self.window_size = 40000
        # self.x_upper_bound = 40000
        # self.window_swap_ratio = 1/4
        # self.window_add_size_every_swap = 20000
        self.y2data = np.zeros(256)
        self.stft = np.zeros(2*self.count)
        # self.window_size = window_size
        # self.x_upper_bound = upper_bound
        # self.window_swap_ratio = window_swap_ratio
        # self.window_add_size_every_swap = window_add_size_every_swap

        self.line1, =self.ax1.plot(np.array([]), np.array([]),'-b',lw=2) 
        self.line2, = self.ax2.plot(np.array([]), np.array([]),'-r',lw = 2) 
        self.line1.set_data(np.array([]),np.array([]))
        self.line2.set_data(np.array([]),np.array([]))

        self.ydata = np.zeros(201*128)
        self.xdata = np.arange(201*128)
        self.x1data = np.linspace(-1000,1000,256)
        self.y1data = np.array([])
        self.ax1.set_xlim(0, 201*128)
        self.ax1.set_ylim(-0.05, 1.05)
        self.ax2.set_xlim(-1000,1000)
        self.ax2.set_ylim(-5,5)
        self.ax1.set_xlabel("Sample Count")
        self.ax2.set_xlabel("Frequency")
        self.ax1.set_ylabel("Absolute Value of sensor readings (Only Positive frequency components)")
        self.ax2.set_ylabel("Magnitude")
        self.ax1.set_title("Ploy of absolute value and its fft")
        
        
        ani = animation.FuncAnimation(self.fig,self.animate2,interval =50,blit = True)
        plt.show()






if __name__ == "__main__":
    readobj = PlotFromPipe("fifo")
    readobj.print_numpy_arrays()
    


# # %%
# a = np.zeros(3)
# # %%
# a = np.vstack((a,np.array([1,2,3])))
# # %%
# a = np.load("abcd.npy")
# print(a)
# a = np.transpose((a))
# #%%
# a = np.load("walk13.npy")
# # %%
# plt.pcolormesh(a,vmin=10,vmax=20, shading='gouraud')
# plt.title('STFT Magnitude')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()
# #%%
# filename = "frame_index.txt" # specify the name of the file to read

# with open(filename, "r") as f:
#     for line in f:
#         print(line.strip())


# # %%
# file = open("frame_index.txt","r")
# #%%
# file.seek(0,2)
# line = file.readline()
# print(line)
# # %%
# with open('frame_index.txt', 'rb') as f:
#     try:  # catch OSError in case of a one line file 
#         f.seek(-2, os.SEEK_END)
#         while f.read(1) != b'\n':
#             f.seek(-2, os.SEEK_CUR)
#     except OSError:
#         f.seek(0)
#     last_line = f.readline()
#     print(last_line)
# # %%
# with open('frame_index.txt', 'r') as f:
#     last_line = f.readlines()[-1]
#     print(last_line)
# # %%
# def follow(thefile):
#     thefile.seek(0,2)
#     line = thefile.readline()
#     yield line

    
# # %%
# logfile = open("frame_index.txt","r")
# loglines = follow(logfile)
# for line in loglines:
#     print(line)
# # %%
# f2 = open("frame_index.txt", "rt")
# a = f2.read()

# # %%
#%%
np.fromstring('1,2,', dtype=int, sep=',')
# %%
