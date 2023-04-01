import time
from sortedcontainers import SortedSet
from inputimeout import inputimeout, TimeoutOccurred

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
buttons=[]
buttons = [0 for i in range(NUM_FLOORS)] 

def lowest_button_on(buttons):
    
    for i, x in enumerate(buttons):
        
        if x == 1:
            return int(i+1)
  
def highest_button_on(buttons):
    j = 0
    for i, x in enumerate(reversed(buttons)):
        
        if x == 1:
            return int(NUM_FLOORS-i)
 
def any_button_pressed(buttons):
    for i, x in enumerate (buttons):
        if x == 1:
            return True
    return False

### Endless loop

while(True):
    if (DEBUG_ON):
        print("*** time cycle begin ***")
    # Buttons read section begin
    if __name__ == "__main__":
        # Try reading keyboard input for INPUT_TIMEOUT seconds
        try:
            c = inputimeout(prompt='Input floor now\n', timeout=INPUT_TIMEOUT)
        # timeout, nothing read
        except TimeoutOccurred:
            c = 'timeout'
        print(c)

    # read a valid floor number followed by the Enter key
    if c != 'timeout' and c!='':
        f = eval(c)
        if f >= BOTTOM_FLOOR and f <= TOP_FLOOR:
            # Light/set button on button column
            buttons[f-1]=1
    
    # Buttons read section end

    ## Debug section begin
    if (DEBUG_ON):
        print("*** Buttons: ", buttons)
        print("*** Lowest button: ", lowest_button_on(buttons))
        print("*** Highest button: ", highest_button_on(buttons))
        print("*** Any button pressed: ", any_button_pressed(buttons))
        print("*** Direction: ", direction)
        
    ## Debug section end
    
    print("*** curr_floor", curr_floor)

    ## Controller section begin
    if any_button_pressed(buttons) and direction == ST and lowest_button_on(buttons) > curr_floor:
        direction = UP

    if any_button_pressed(buttons) and direction == ST and highest_button_on(buttons) < curr_floor:
        direction = DN

    if any_button_pressed(buttons)==False:
        direction = ST

    ## End Controller section

    ## Begin Elevator car section
   
    # Arrived on a floor whose button was pushed
    if any_button_pressed(buttons) and (direction == UP or direction == DN) and buttons[curr_floor-1] == 1:
        # Unlight/clear button
        buttons[curr_floor-1] = 0
        print("Open door on floor: ", curr_floor)
        time.sleep(DOOR_WAIT)
        print ("Close door on floor:", curr_floor)
        # No more buttons pressed, stop the elevator car
        if any_button_pressed(buttons) == False:
            direction = ST
        
        # Logic for no overruns. This is the situation when elevator gets to the highest floor it was directed to, moving up, and there are no more floors above called, but
        # there are lower floors we need to go. This means changing direction of travel from up to down. 
       
        if any_button_pressed(buttons) == True and highest_button_on(buttons) < curr_floor:
            direction = DN

        # Similarly, when going down, once stopped on the lowest floor, and there
        # is an higher floor pushed, change direction to up.

        if any_button_pressed(buttons) == True and lowest_button_on(buttons) > curr_floor:
            direction = UP


    # Move elevator car
    if direction == UP and any_button_pressed(buttons):
        curr_floor = curr_floor + 1 
    if direction == DN and any_button_pressed(buttons):
        curr_floor = curr_floor - 1
    ## End Elevator car section

    if (DEBUG_ON):
        print ("***--- Cycle end ***")
