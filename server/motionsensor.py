import random
import socket
import time

# Simulated IoT device configuration
device_id = "motion_sensor_123"
server_ip = "192.168.1.100"  # Replace with the actual server IP address
server_port = 12345  # Replace with the actual server port
update_interval = 1  # Update interval in seconds

# Simulated motion sensor function
def generate_motion_event():
    # Simulate motion events with a random chance
    return random.random() < 0.3  # Adjust the threshold as needed

while True:
    motion_event = generate_motion_event()
   
    # Prepare data to send to the server
    data = {
        "device_id": device_id,
        "motion_detected": motion_event
    }
   
    try:
        # Create a socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
           
            # Send data to the server
            data_str = f"{data}\n"
            s.send(data_str.encode('utf-8'))
           
            if motion_event:
                print("Motion detected and sent to the server.")
            else:
                print("No motion detected.")
    except Exception as e:
        print(f"Failed to send data. Error: {e}")
   
    time.sleep(update_interval)