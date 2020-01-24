import json
import logging
import sys
import threading
import time

from gpiozero import RGBLED, AngularServo
from colorzero import Color
from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('agt.alexa_gadget').setLevel(logging.DEBUG)

# GPIO Pins
GPIO_LED_RED = 2
GPIO_LED_GREEN = 3
GPIO_LED_BLUE = 4
GPIO_SERVO_PIN = 14

# Setup RGB LED
# set active_high to False for common anode RGB LED
# else set to True for common cathode RGB LED
RGB_LED = RGBLED(GPIO_LED_RED, GPIO_LED_GREEN, GPIO_LED_BLUE,
                 active_high=True, initial_value=(0, 0, 0))

SERVO = AngularServo(GPIO_SERVO_PIN, initial_angle=-90,
                     min_pulse_width=0.0005, max_pulse_width=0.002)

class CatFeederGadget(AlexaGadget):
    """
    Class that logs each directive received from the Echo device.
    """

    def __init__(self):
        super().__init__()

    def on_custom_catfeedergadget_init(self, directive):
        """
        Handles Custom.CatFeederGadget.Init directive sent from skill
        """
        self._reset_feeder()

        # Turn on the LED
        RGB_LED.color = Color('blue')
        RGB_LED.on()

    def on_custom_catfeedergadget_cleanup(self, directive):
        """
        Handles Custom.CatFeederGadget.Cleanup directive sent from skill
        """
        self._reset_feeder()

    def on_custom_catfeedergadget_feedcat(self, directive):
        """
        Handles Custom.CatFeederGadget.FeedCat directive sent from skill
        """

        # Set angle of servo to 0 degrees
        SERVO.angle = 0
        time.sleep(1)
        SERVO.detach()

        payload = {'feed': True}
        self.send_custom_event(
            'Custom.CatFeederGadget', 'ReportFeeder', payload)

    def _reset_feeder(self):
        # Set angle of servo to -90 degrees
        SERVO.angle = -90
        time.sleep(1)
        SERVO.detach()

        # Turn off the LED
        RGB_LED.color = Color('red')
        RGB_LED.off()

if __name__ == '__main__':
    try:
        CatFeederGadget().main()
    finally:
        logger.debug('Cleaning up GPIO')
        RGB_LED.close()
        SERVO.close()
