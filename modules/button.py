import RPi.GPIO as gpio
import time


class GPIOButton:
    def __init__(self, pin_number: int):
        self.pin = pin_number
        self.is_pressed = False
        self.is_pressed_prev = False
        if gpio is not None:
            gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    def update_state(self):
        """ Update button state """
        self.is_pressed_prev = self.is_pressed
        self.is_pressed = self._pin_read(self.pin) == 0

    def is_button_pressed(self) -> bool:
        """ Button was pressed by user """
        return self.is_pressed and not self.is_pressed_prev

    def is_button_hold(self) -> bool:
        """ Button still pressed by user """
        return self.is_pressed and self.is_pressed_prev

    def is_button_released(self) -> bool:
        """ Button released by user """
        return not self.is_pressed and self.is_pressed_prev

    def reset_state(self):
        """ Clear the button state """
        self.is_pressed = False
        self.is_pressed_prev = False

    def _pin_read(self, pin: int) -> int:
        """ Read pin value """
        return gpio.input(pin) if gpio is not None else 0

class VirtualButton(GPIOButton):
    def __init__(self, delay_sec: int):
        super().__init__(pin_number=-1)
        self.start_time = time.monotonic()
        self.delay_sec = delay_sec

    def update_state(self):
        """ Update button state: button is pressed first N seconds """
        self.is_pressed_prev = self.is_pressed
        self.is_pressed = time.monotonic() - self.start_time < self.delay_sec

