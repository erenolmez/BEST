#%%
import time
import numpy as np
import os
import mmap
import socket
from pipe_reader import ReadFromPipe
import sys
print(sys.path)
#%%
#%%

def udp_client(host, port):
    readobj = ReadFromPipe("fifo1")
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout for the socket operations (optional)
    client_socket.settimeout(1.0)

    while True:
        try:
            message = readobj.return_one_frame()
            client_socket.sendto(message.encode(), (host, port))

            # Wait for 1 second before sending the next message
            time.sleep(0.045)
        except socket.timeout:
            print("Timeout occurred, retrying...")

    # Close the socket (this line will never be reached in this example)
    client_socket.close()

# Usage example
host = "139.179.42.27"  # Replace with the server's IP address or hostname
port = 8888  # Replace with the server's port number
udp_client(host, port)
