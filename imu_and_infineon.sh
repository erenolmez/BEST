#!/bin/bash
chmod 0666 /dev/ttyUSB1
chmod 0666 /dev/ttyUSB0
sleep 1;
python3 /home/remote/Desktop/build/imu_data1.py &
sleep 1;
python3 /home/remote/Desktop/build/record_data.py &
sleep 1; python3 /home/remote/Desktop/build/udp_client.py &
# sleep 1; ./s2glp_basics > fifo
# sleep 1; exec 3<> fifo; ~/setfifo fifo 1048576; ./s2glp_basics | tee fifo fifo1 &

wait
