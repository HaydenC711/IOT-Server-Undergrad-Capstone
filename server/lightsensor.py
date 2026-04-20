import random
import time

# Function to simulate light intensity readings
def generate_light_intensity():
    return round(random.uniform(0, 1000), 2)

# Function to print light intensity readings
def print_light_intensity(sensor_id, light_intensity):
    print(f"Sensor ID: {sensor_id}, Light Intensity: {light_intensity}")

# Main simulation loop
def main():
	
	# Unique id for the sensor
    sensor_id = "light_sensor456"
    
    while True:
        light_intensity = generate_light_intensity()
        print_light_intensity(sensor_id, light_intensity)
        
        # Adjust the sleep interval based on your desired data generation frequency
        time.sleep(10)

main()
