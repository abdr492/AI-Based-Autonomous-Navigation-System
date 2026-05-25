import time
import random

# Simulating HC-SR04 on Raspberry Pi
# (Since RPi.GPIO is not available on Windows, we mock the hardware interaction)

class HCSR04_Virtual:
    def __init__(self, trig_pin=23, echo_pin=24):
        self.trig = trig_pin
        self.echo = echo_pin
        print(f"Virtual HC-SR04 Initialized on TRIG:{self.trig}, ECHO:{self.echo}")

    def measure_distance(self):
        """Simulates distance measurement by returning a random value or a simulated scenario"""
        # Simulating distance returning between 2cm and 400cm
        # We will make it randomly drop below 20 cm to simulate an obstacle
        
        if random.random() < 0.1: # 10% chance to detect an obstacle
            distance = random.uniform(5.0, 19.9)
        else:
            distance = random.uniform(20.0, 150.0)
            
        return round(distance, 2)

def simulate_obstacle_avoidance():
    print("Starting Obstacle Avoidance Module...")
    sensor = HCSR04_Virtual()
    
    try:
        while True:
            dist = sensor.measure_distance()
            print(f"Distance Measured: {dist} cm")
            
            if dist < 20:
                print(">>> WARNING: Obstacle Detected! Applying Brakes and Recalculating Path...")
                time.sleep(1) # Simulate time taken for recalculation
                print(">>> Path Recalculated. Resuming...")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nSimulation Stopped.")

if __name__ == "__main__":
    simulate_obstacle_avoidance()
