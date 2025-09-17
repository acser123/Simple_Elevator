import time

ST = "stopped"
UP = "moving_up"
DN = "moving_dn"

class Elevator:
    def __init__(self, bottom_floor, top_floor):
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.current_floor = bottom_floor
        self.direction = ST
        self.requests = set()
        self.door_wait_time = 5

    def add_request(self, floor):
        if self.bottom_floor <= floor <= self.top_floor:
            self.requests.add(floor)

    def move(self):
        if self.direction == ST:
            # If we are stopped, is there a request for the current floor?
            if self.current_floor in self.requests:
                self.requests.remove(self.current_floor)
                print(f"Open door on floor: {self.current_floor}")
                time.sleep(self.door_wait_time)
                print(f"Close door on floor: {self.current_floor}")

            self._update_direction()
            # If we decided to start moving, don't move until the next cycle.
            if self.direction != ST:
                return

        # If we are moving, then move.
        if self.direction == UP:
            self.current_floor += 1
        elif self.direction == DN:
            self.current_floor -= 1

        # After moving, check if we arrived at a requested floor.
        if self.current_floor in self.requests:
            self.requests.remove(self.current_floor)
            print(f"Open door on floor: {self.current_floor}")
            time.sleep(self.door_wait_time)
            print(f"Close door on floor: {self.current_floor}")
            self.direction = ST

    def _update_direction(self):
        if not self.requests:
            self.direction = ST
            return

        if self.direction == ST:
            next_target = min(self.requests, key=lambda x: abs(x - self.current_floor))
            if next_target > self.current_floor:
                self.direction = UP
            elif next_target < self.current_floor:
                self.direction = DN

        elif self.direction == UP:
            if not any(r > self.current_floor for r in self.requests):
                self.direction = DN if self.requests else ST

        elif self.direction == DN:
            if not any(r < self.current_floor for r in self.requests):
                self.direction = UP if self.requests else ST
