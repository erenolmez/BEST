#!/bin/bash
chmod 0666 /dev/ttyUSB1
chmod 0666 /dev/ttyUSB0
aplay Oy\ asiye\ roblox.wav;
node-red &
sleep 3;
python3 /home/remote/Desktop/build/record_data.py &
sleep 3; ./s2glp_basics > fifo &
wait
