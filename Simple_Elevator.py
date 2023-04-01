import time
from inputimeout import inputimeout, TimeoutOccurred
import numpy as np

DEBUG_ON = True

# Building setup
TOP_FLOOR = 10
BOTTOM_FLOOR = 1
NUM_FLOORS = TOP_FLOOR - BOTTOM_FLOOR + 1
NO_FLOOR = 0
# Elevator car travel direction
ST = "stopped"
UP = "moving_up"
DN = "moving_dn"
direction = ST
curr_floor = BOTTOM_FLOOR

# Wait time
INPUT_TIMEOUT = 2
DOOR_WAIT = 5


# elevator buttons
# buttons = [0 for i in range(NUM_FLOORS)]
buttons = np.zeros(NUM_FLOORS, dtype=int)

# def any_button_pressed():
#     return buttons.any()


### Endless loop

while True:
    if (DEBUG_ON):
        print("*** time cycle begin ***")

   # 1) Why eliminate reusable functions around data structures?
   # 2) Which functional area (section) does this code belong to? Buttons read, Controller or Elevator car?
    buttons_pressed = np.flatnonzero(buttons)
 
    if buttons_pressed.size > 0:
        buttons_pressed += 1
        lowest_button_on = np.min(buttons_pressed) 
        highest_button_on = np.max(buttons_pressed)
    else:
        lowest_button_on = None
        highest_button_on = None

    # Buttons read section begin
    if __name__ == "__main__":
        # Try reading keyboard input for INPUT_TIMEOUT seconds
        try:
            c = inputimeout(prompt='Input floor now: ', timeout=INPUT_TIMEOUT)
        # timeout, nothing read
        except TimeoutOccurred:
            c = 'timeout'
        print(c)

    # read a valid floor number followed by the Enter key
    if c != 'timeout' and c is not None:
        f = eval(c)
        if f >= BOTTOM_FLOOR and f <= TOP_FLOOR:
            # Light/set button on button column
            buttons[f-1]=1
    
    # Buttons read section end

    ## Debug section begin
    if (DEBUG_ON):
        print("*** Buttons: ", buttons)
        print("*** Lowest button: ", lowest_button_on)
        print("*** Highest button: ", highest_button_on)
        print("*** Any button pressed: ", bool(buttons_pressed))
        print("*** Direction: ", direction)
        
    ## Debug section end
    
    print("*** curr_floor: ", curr_floor)

    ## Controller section begin
    if buttons_pressed.size > 0 and direction == ST and lowest_button_on > curr_floor:
        direction = UP

    if buttons_pressed.size > 0 and direction == ST and highest_button_on < curr_floor:
        direction = DN

    if not buttons_pressed.size > 0:
        direction = ST

    ## End Controller section

    ## Begin Elevator car section
   
    # Arrived on a floor whose button was pushed
    if buttons_pressed.size > 0 and (direction == UP or direction == DN) and buttons[curr_floor-1] == 1:
        # Unlight/clear button
        buttons[curr_floor-1] = 0
        print("Open door on floor: ", curr_floor)
        time.sleep(DOOR_WAIT)
        print ("Close door on floor:", curr_floor)
        # No more buttons pressed, stop the elevator car
        if not buttons_pressed.size > 0:
            direction = ST
        
        # Logic for no overruns. This is the situation when elevator gets to the highest floor it was directed to, moving up, and there are no more floors above called, but
        # there are lower floors we need to go. This means changing direction of travel from up to down. 
       
        if buttons_pressed.size > 0 and highest_button_on < curr_floor:
            direction = DN

        # Similarly, when going down, once stopped on the lowest floor, and there
        # is an higher floor pushed, change direction to up.

        if buttons_pressed.size > 0 and lowest_button_on > curr_floor:
            direction = UP


    # Move elevator car
    if direction == UP and buttons_pressed.size > 0:
        curr_floor += 1 
    if direction == DN and buttons_pressed.size > 0:
        curr_floor -= 1
    ## End Elevator car section

    if (DEBUG_ON):
        print (buttons)
        print ("***--- Cycle end ***")
