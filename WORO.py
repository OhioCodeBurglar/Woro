#API used:Openweathermap.org,NOAA Api

import math
import requests
import threading
import time
import queue
import curses

WIND_KEY = "cb74d8052fc04a7f847bb7cdf2450ef9"
WAVE_KEY = "AzbGQWqzFYqgIXMssbgaimmCMcvsXyor"
latitude = 51.505488
longitude = -71.175589

stop_event = threading.Event()  # Event to signal termination
print_queue = queue.Queue()  # Queue for printing data

def fetch_wind_data():
    while not stop_event.is_set():
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WIND_KEY}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            wind_speed = data["wind"]["speed"]
            wind_direction = data["wind"]["deg"]
            print_queue.put((wind_speed, wind_direction))
        else:
            print_queue.put(("Failed to retrieve data",))
        
        time.sleep(5)  # Wait for 5 seconds before fetching data again

def waveHeight(wind_speed):
    
    # Calculate the fetch distance
    if wind_speed != 0:
        fetch_distance = 3000 / (wind_speed ** 2)
    else:
        return 0
    # Calculate wave height using the fetch distance
    wave_height = 0.01 * (wind_speed ** 2) * fetch_distance ** 0.5
    wave_height = round(wave_height,2)
    return wave_height

def calculate_velocity(wind_speed, wind_direction_degrees):
    if wind_speed == 0:
        return (0.0, 0.0)  # No wind, no movement
    
    wind_direction_radians = math.radians(wind_direction_degrees)
    
    x_velocity = wind_speed * math.cos(wind_direction_radians)
    y_velocity = wind_speed * math.sin(wind_direction_radians)
    
    x_velocity = round(x_velocity, 3)  # Round to 3 decimal places
    y_velocity = round(y_velocity, 3)

    return (x_velocity, y_velocity)

def estimate_wind(wind_speed, wind_direction):
    wind_labels = {
        0.2: "calm breeze",
        1.5: "light breeze",
        3.3: "gentle breeze",
        5.3: "moderate breeze",
        7.9: "strong breeze",
        10.7: "near gale breeze",
        13.7: "gale breeze",
        17: "strong gale breeze",
        20.6: "storm",
        28.3: "violent storm",
    }
    direction_labels = {
        (337.5, 22.5): "north",
        (22.5, 67.5): "northeast",
        (67.5, 112.5): "east",
        (112.5, 157.5): "southeast",
        (157.5, 202.5): "south",
        (202.5, 247.5): "southwest",
        (247.5, 292.5): "west",
        (292.5, 337.5): "northwest"
    }

    wind_label = None
    for upper_limit, label in wind_labels.items():
        if wind_speed < upper_limit:
            wind_label = label
            break
    if wind_label is None:
        wind_label = "HURRICANE"

    direction_label = None
    for (lower_limit, upper_limit), label in direction_labels.items():
        if lower_limit <= wind_direction < upper_limit:
            direction_label = label
            break

    return wind_label, direction_label

def main(stdscr):
    global latitude, longitude
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    wind_speed = 0.0
    # Define the precise_round function
    def precise_round(value):
        if value > 0.15:
            return 1
        elif -0.15 < value < 0.15:
            return 0
        else:
            return -1

    # Create a thread for fetching wind data
    wind_thread = threading.Thread(target=fetch_wind_data)
    wind_thread.start()

    # Define a dictionary to map key presses to velocity changes
    key_velocity_mapping = {
        ord('j'): (0.308333, 0.0),   # East
        ord('g'): (-0.308333, 0.0),  # West
        ord('y'): (0.0, 0.308333),   # North
        ord('n'): (0.0, -0.308333),  # South
        ord('u'): (0.308333, 0.308333),  # North East
        ord('t'): (-0.308333, 0.308333), # North West
        ord('b'): (0.308333, -0.308333), # South East
        ord('m'): (-0.308333, -0.308333) # South West
    }

    velocity = (0.0, 0.0)  # Default velocity (East)
    try:
        # Main loop
        while True:
            latitude += velocity[0]
            longitude += velocity[1]
            try:
                wind_speed, wind_direction = print_queue.get_nowait()
                wind_label,direction_label = estimate_wind(wind_speed,wind_direction)
                stdscr.addstr(0, 0, f"{wind_label} coming from the {direction_label}")
                stdscr.addstr(1, 0, '----------------------------------')
            except queue.Empty:
                pass

            # Convert velocities to rounded tuples based on your requirements
            rounded_velocity = (
                precise_round(velocity[0]),
                precise_round(velocity[1])
            )
            
            # Define the direction text
            direction_text = {
                (0, 0): 'stopped',
                (1, 0): 'going east',
                (-1, 0): 'going west',
                (0, 1): 'going north',
                (0, -1): 'going south',
                (1, 1): 'going northeast',
                (-1, 1): 'going northwest',
                (1, -1): 'going southeast',
                (-1, -1): 'going southwest'
            }
            wave_height = waveHeight(wind_speed)
            stdscr.addstr(2, 0, direction_text[rounded_velocity])
            stdscr.addstr(3, 0, f"x velocity: {velocity[0]}")
            stdscr.addstr(4, 0, f"y velocity: {velocity[1]}")
            stdscr.addstr(5,0, '----------------------------------')
            stdscr.addstr(6,0, f"average wave height:{wave_height}m")
            stdscr.refresh()


            # Check for user input
            key = stdscr.getch()
            if key in key_velocity_mapping:
                velocity = key_velocity_mapping[key]
            if key == ord('q'):
                stop_event.set()  # Signal the other thread to terminate
                wind_thread.join()  # Wait for the wind thread to finish before exiting
                break

            time.sleep(1)  # Allow some time for the other thread to print data

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

curses.wrapper(main)

