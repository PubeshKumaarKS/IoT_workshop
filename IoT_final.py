import grovepi
import time

# Connect the humidity sensor to a digital port on the Grove Pi
humidity_sensor_port = 7  # Use D7 port

rotaryanglesensor = 14     # Pin 14 is A0 Port.

grovepi.pinMode(rotaryanglesensor,"INPUT")

relay = 5

grovepi.pinMode(relay,"OUTPUT")

buzzer_relay_port = 3  # Use D3 port for buzzer relay
led_relay_port = 4  # Use D4 port for LED relay

dht_type = 0

ultrasonicsensor = 4
ac = 2


grovepi.pinMode(ac,"OUTPUT")

# Threshold values for humidity and temperature
high_humidity_threshold = 70  # Adjust as needed
high_temperature_threshold = 28  # Adjust as needed
low_humidity_threshold = 30  # Adjust as needed
low_temperature_threshold = 20  # Adjust as needed

# Initialize Grove Pi
grovepi.pinMode(buzzer_relay_port, "OUTPUT")
grovepi.pinMode(led_relay_port, "OUTPUT")

# Function to control the buzzer and LED based on conditions
def control_devices(humidity, temperature):
    if humidity > high_humidity_threshold or temperature > high_temperature_threshold:
        grovepi.digitalWrite(buzzer_relay_port, 1)  # Turn on the buzzer
        grovepi.digitalWrite(led_relay_port, 0)  # Turn off the LED
        
        print("High humidity or temperature! Buzzer turned on.")

        grovepi.digitalWrite(relay,1) # switch on ac
        time.sleep(3)
        grovepi.digitalWrite(relay,0)

    elif humidity < low_humidity_threshold or temperature < low_temperature_threshold:

        grovepi.digitalWrite(led_relay_port, 1)  # Turn on the LED
        grovepi.digitalWrite(buzzer_relay_port, 0)  # Turn off the buzzer
        grovepi.digitalWrite(relay,1) # switch on thermostat
        time.sleep(3)
        grovepi.digitalWrite(relay,0)

        print("Low humidity or temperature! LED turned on.")
    else:
        grovepi.digitalWrite(buzzer_relay_port, 0)  # Turn off the buzzer
        grovepi.digitalWrite(led_relay_port, 0)  # Turn off the LED
        grovepi.digitalWrite(relay,0)
        print("Conditions are normal. Devices turned off.")

    sensor_value = grovepi.analogRead(rotaryanglesensor)
    print ("sensor_value = %d" %sensor_value)
    # Give rotary angle sensor output to AC
    grovepi.analogWrite(ac,int(sensor_value))
    sensor_value += 5 #inc temp
    time.sleep(.1)
    
def initialize_sensors():
    # Set ultrasonic sensor to INPUT mode
    grovepi.pinMode(ultrasonicsensor, "INPUT")
    
    # Set LED to OUTPUT mode
    grovepi.pinMode(led_relay_port, "OUTPUT")
    
    # Wait for sensor initialization
    time.sleep(1)

# Function to control LED based on distance
def control_led_based_on_distance():
    try:
        while True:
            # Read distance from the ultrasonic sensor
            distance = grovepi.ultrasonicRead(ultrasonicsensor)
            
            # LED control based on distance
            if distance > 100:
                grovepi.digitalWrite(led, 1)  # Switch on LED
                print("LED ON!")
            else:
                grovepi.digitalWrite(led, 0)  # Switch off LED
                print("LED OFF!")
            
            print("Distance: ", distance, "cm")
            
            time.sleep(1)
            
try:
    while True:
        initialize_sensors()
        # Read the humidity and temperature from the sensor
        [temp, humidity] = grovepi.dht(humidity_sensor_port, dht_type)
        initialize_sensors()
        control_led_based_on_distance()
        
        if isnan(temp) is False and isnan(humidity) is False:
            print(f"Temperature: {temp}°C, Humidity: {humidity}%")
            control_devices(humidity, temp)
        
        else:
            print("Failed to read data from the sensor")

        time.sleep(5)  # Wait for a few seconds before reading again
        
except KeyboardInterrupt:
    grovepi.digitalWrite(buzzer_relay_port, 0)  # Turn off the buzzer
    grovepi.digitalWrite(led_relay_port, 0)  # Turn off the LED
    
    print("Program terminated by user")
except IOError:
    print("Error: Unable to communicate with Grove Pi")    
