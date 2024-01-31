#!/bin/bash
chmod 0666 /dev/ttyUSB0
chmod 0666 /dev/ttyUSB1
node-red &
sleep 3; 
# ssh -R remote.serveo.net:80:localhost:1880 serveo.net &
# sleep 3; 

python3 /home/remote/Desktop/build/imu_data.py &
# python3 /home/remote/Desktop/build/seeed-rpi-deneme.py &
python3 /home/remote/Desktop/build/record_data.py &
sleep 1; python3 /home/remote/Desktop/build/udp_client.py &
sleep 3; exec 3<> fifo; ~/setfifo fifo 1048576; ./s2glp_basics > fifo &
# sleep 1; exec 3<> fifo; ~/setfifo fifo 1048576; ./s2glp_basics | tee fifo fifo1 &

wait
