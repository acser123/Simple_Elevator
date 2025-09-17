import time
from inputimeout import inputimeout, TimeoutOccurred
from elevator import Elevator, ST, UP, DN

# Building setup
TOP_FLOOR = 10
BOTTOM_FLOOR = 1
INPUT_TIMEOUT = 2
DEBUG_ON = True

def main():
    elevator = Elevator(BOTTOM_FLOOR, TOP_FLOOR)

    while True:
        if DEBUG_ON:
            print("*** time cycle begin ***")

        try:
            c = inputimeout(prompt='Input floor now: ', timeout=INPUT_TIMEOUT)
            if c:
                floor = int(c)
                if BOTTOM_FLOOR <= floor <= TOP_FLOOR:
                    elevator.add_request(floor)
                else:
                    print(f"Invalid floor. Please enter a number between {BOTTOM_FLOOR} and {TOP_FLOOR}.")
        except TimeoutOccurred:
            pass
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")

        elevator.move()

        if DEBUG_ON:
            print(f"*** Current Floor: {elevator.current_floor}, Direction: {elevator.direction}, Requests: {elevator.requests}")
            print("***--- Cycle end ***")

        time.sleep(1) # To prevent busy-waiting and make the simulation observable

if __name__ == "__main__":
    main()
