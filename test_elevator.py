import unittest
from unittest.mock import patch
from elevator import Elevator, ST, UP, DN

class TestElevator(unittest.TestCase):

    def setUp(self):
        self.elevator = Elevator(bottom_floor=1, top_floor=10)
        self.elevator.door_wait_time = 0

    @patch('time.sleep', return_value=None)
    def test_initial_state(self, patched_time_sleep):
        self.assertEqual(self.elevator.current_floor, 1)
        self.assertEqual(self.elevator.direction, ST)
        self.assertEqual(len(self.elevator.requests), 0)

    @patch('time.sleep', return_value=None)
    def test_add_request(self, patched_time_sleep):
        self.elevator.add_request(5)
        self.assertIn(5, self.elevator.requests)

    @patch('time.sleep', return_value=None)
    def test_add_invalid_request(self, patched_time_sleep):
        self.elevator.add_request(11)
        self.assertNotIn(11, self.elevator.requests)
        self.elevator.add_request(0)
        self.assertNotIn(0, self.elevator.requests)

    @patch('time.sleep', return_value=None)
    def test_move_up(self, patched_time_sleep):
        self.elevator.add_request(3)
        self.elevator.move() # Direction becomes UP
        self.assertEqual(self.elevator.direction, UP)
        self.elevator.move() # Moves from 1 to 2
        self.assertEqual(self.elevator.current_floor, 2)

    @patch('time.sleep', return_value=None)
    def test_move_down(self, patched_time_sleep):
        self.elevator.current_floor = 5
        self.elevator.add_request(2)
        self.elevator.move() # Direction becomes DN
        self.assertEqual(self.elevator.direction, DN)
        self.elevator.move() # Moves from 5 to 4
        self.assertEqual(self.elevator.current_floor, 4)

    @patch('time.sleep', return_value=None)
    def test_stop_at_floor(self, patched_time_sleep):
        self.elevator.add_request(2)
        self.elevator.move() # Direction -> UP
        self.elevator.move() # Move to 2, open/close door
        self.assertNotIn(2, self.elevator.requests)
        self.assertEqual(self.elevator.current_floor, 2)
        # After serving the only request, it should stop
        self.elevator.move()
        self.assertEqual(self.elevator.direction, ST)

    @patch('time.sleep', return_value=None)
    def test_change_direction_up_to_down(self, patched_time_sleep):
        self.elevator.current_floor = 3
        self.elevator.add_request(5)
        self.elevator.move() # Direction -> UP
        self.assertEqual(self.elevator.direction, UP)
        self.elevator.add_request(2)
        # Move to 4
        self.elevator.move()
        self.assertEqual(self.elevator.current_floor, 4)
        # Move to 5, serve request
        self.elevator.move()
        self.assertEqual(self.elevator.current_floor, 5)
        self.assertNotIn(5, self.elevator.requests)
        # Next move should change direction to DN
        self.elevator.move()
        self.assertEqual(self.elevator.direction, DN)

if __name__ == '__main__':
    unittest.main()
