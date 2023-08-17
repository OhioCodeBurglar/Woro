#API used:Openweathermap.org

import math
import requests
import threading
import time
import queue
import curses
import datetime
import random
food = 10
dizziness = 0
holes = 0

WIND_KEY = "cb74d8052fc04a7f847bb7cdf2450ef9"
WAVE_KEY = "AzbGQWqzFYqgIXMssbgaimmCMcvsXyor"
latitude = 51.505488
longitude = -71.175589

stop_event = threading.Event()  # Event to signal termination
print_queue = queue.Queue()  # Queue for printing data

def logo(stdscr):
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor
    screen_height,screen_width = stdscr.getmaxyx()

    # ASCII art for the logo
    logo_art = [
        "░██╗░░░░░░░██╗░█████╗░██████╗░░█████╗░",
        "░██║░░██╗░░██║██╔══██╗██╔══██╗██╔══██╗",
        "░╚██╗████╗██╔╝██║░░██║██████╔╝██║░░██║",
        "░░████╔═████║░██║░░██║██╔══██╗██║░░██║",
        "░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║╚█████╔╝",
        "░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝░╚════╝░",
    ]

    # Calculate center position for the logo
    start_row = max(0, screen_height // 2 - len(logo_art) // 2)
    start_col = max(0, screen_width // 2 - len(logo_art[0]) // 2)

    # Display the logo at the center
    for row, line in enumerate(logo_art, start=start_row):
        stdscr.addstr(row, start_col, line)
    
    # Refresh the screen
    stdscr.refresh()
    curses.napms(4200)

def die(stdscr,cause:str):
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    curses.curs_set(0)  # Hide the cursor
    while not stop_event.is_set():
        died_art = """██╗░░░██╗░█████╗░██╗░░░██╗  ██████╗░██╗███████╗██████╗░
        ╚██╗░██╔╝██╔══██╗██║░░░██║  ██╔══██╗██║██╔════╝██╔══██╗
        ░╚████╔╝░██║░░██║██║░░░██║  ██║░░██║██║█████╗░░██║░░██║
        ░░╚██╔╝░░██║░░██║██║░░░██║  ██║░░██║██║██╔══╝░░██║░░██║
        ░░░██║░░░╚█████╔╝╚██████╔╝  ██████╔╝██║███████╗██████╔╝
        ░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚═════╝░╚═╝╚══════╝╚═════╝░"""
        stdscr.clear()
        stdscr.addstr(0,0,died_art)
        stdscr.addstr(7,0,cause)

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
    wave_height /= 1.5
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
        (337.5, 22.5): "north      ",
        (22.5, 67.5): "northeast",
        (67.5, 112.5): "east      ",
        (112.5, 157.5): "southeast",
        (157.5, 202.5): "south      ",
        (202.5, 247.5): "southwest",
        (247.5, 292.5): "west      ",
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

def get_ocean(latitude, longitude):
    if 20 < longitude <= 180:
        if latitude > 0:
            return "North Atlantic Ocean"
        else:
            return "South Atlantic Ocean"
    elif -30 < longitude <= 20:
        return "Indian Ocean"
    elif -120 < longitude <= -30:
        if latitude > 0:
            return "North Pacific Ocean"
        else:
            return "South Pacific Ocean"
    else:
        return "Unknown"
def fish_population(ocean,wind_speed,latitude):
    #GET MONTH
    month = datetime.datetime.now().month
    #TEMPERATURE CALCULATIONS
    base_temperature = 20  # A rough starting point
    latitude_adjustment = abs(latitude) / 50  # Normalize latitude to a 0-1 range

    if month >= 4 and month <= 9:  # Warmer months
        temperature_adjustment = 0.5
    else:
        temperature_adjustment = 0

    estimated_temperature = base_temperature + latitude_adjustment + temperature_adjustment
    fish_population = 0.1*wind_speed+0.01*month+0.001*latitude+(estimated_temperature/10)
    fish_population = (fish_population - 0) / (20 - 0)
    # Map normalized value to probability range (e.g., 0% to 100%)
    mapped_probability = fish_population * 100

    # Simulate the chance of catching a fish
    random_number = random.uniform(0, 100)
    if random_number <= mapped_probability:
        return 1
    else:
        return 0
def hunger(stdscr):
    global food
    time.sleep(30)
    if food <= 1:
        die(stdscr,"You died because of starvation,next time fish more, or go to more fish friendly areas")
    else:
        food-=1
def main(stdscr):
    global latitude, longitude,food,dizziness,holes
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    curses.curs_set(0)  # Hide the cursor

    stdscr.clear() 
    is_fishing = False
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
    
    #Create a food depletion thread
    hunger_thread = threading.Thread(target=hunger,args=(stdscr,))
    hunger_thread.start()
    # Define a dictionary to map key presses to velocity changes
    key_velocity_mapping = {
        ord('h'): (0.0,0.0), #anchored
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
                stdscr.addstr(1, 0, f"{wind_label} coming from the {direction_label}")
                stdscr.addstr(2, 0, '----------------------------------')
            except queue.Empty:
                pass

            # Convert velocities to rounded tuples based on your requirements
            rounded_velocity = (
                precise_round(velocity[0]),
                precise_round(velocity[1])
            )
            
            # Define the direction text
            direction_text = {
                (0, 0): 'anchored            ',
                (1, 0): 'going east         ',
                (-1, 0): 'going west        ',
                (0, 1): 'going north    ',
                (0, -1): 'going south    ',
                (1, 1): 'going northeast    ',
                (-1, 1): 'going northwest    ',
                (1, -1): 'going southeast    ',
                (-1, -1): 'going southwest    '
            }
            wave_height = waveHeight(wind_speed)
            ocean = get_ocean(longitude,latitude)
            visual_velocity = (round(velocity[0],2),round(velocity[1],2))
            stdscr.addstr(0,0, "Boat Info:")
            stdscr.addstr(3, 0, direction_text[rounded_velocity])
            stdscr.addstr(4, 0, f"x velocity: {visual_velocity[0]}")
            stdscr.addstr(5, 0, f"y velocity: {visual_velocity[1]}")
            stdscr.addstr(6,0, '----------------------------------')
            stdscr.addstr(7,0, f"average wave height:{wave_height}m")
            stdscr.addstr(8,0, f"Current Ocean: {ocean}")
            stdscr.addstr(9,0, '----------------------------------') 
            stdscr.addstr(10,0, "Personal Info")
            stdscr.addstr(11,0, f"Food: {food}")
            stdscr.addstr(12,0, f"Dizziness: {dizziness}") 
            stdscr.refresh()


            # Check for user input
            key = stdscr.getch()
            if key == ord('q'):
                stop_event.set()  # Signal the other thread to terminate
                wind_thread.join()# Wait for the wind thread to finish before exiting
                hunger_thread.join()#same for the hunger thread
                break
            elif key == ord('+'):
                stop_event.set()
                break
            elif key in key_velocity_mapping:
                velocity = key_velocity_mapping[key]
            elif key == ord('*'):
                if is_fishing:
                    stdscr.addstr(13, 0, "")
                    is_fishing = False
                else:
                    velocity = (0.0, 0.0)
                    stdscr.addstr(13, 0, "Fishing...       ")
                    stdscr.refresh()
                    stdscr.nodelay(False)  # Disable non-blocking getch
                    if fish_population(ocean, wind_speed, latitude) == 1:
                        fish_catch_message = "You caught a fish!"
                        food += 1
                    else:
                        fish_catch_message = ""
                    stdscr.nodelay(True)  # Re-enable non-blocking getch
                    is_fishing = True
                    time.sleep(3)
                    stdscr.addstr(13, 0, fish_catch_message)
                    stdscr.refresh()

            time.sleep(1)  # Allow some time for the other thread to print data

    except KeyboardInterrupt:
        print("Exiting...       ")

    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

curses.wrapper(logo)

curses.wrapper(main)

