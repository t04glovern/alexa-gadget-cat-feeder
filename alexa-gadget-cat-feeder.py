import json
import logging
import sys
import threading
import time

from gpiozero import RGBLED
from colorzero import Color
from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('agt.alexa_gadget').setLevel(logging.DEBUG)

# GPIO Pins
GPIO_LED_RED = 2
GPIO_LED_GREEN = 3
GPIO_LED_BLUE = 4

# Setup RGB LED
# set active_high to False for common anode RGB LED
# else set to True for common cathode RGB LED
RGB_LED = RGBLED(GPIO_LED_RED, GPIO_LED_GREEN, GPIO_LED_BLUE,
                 active_high=True, initial_value=(0, 0, 0))

class CatFeederGadget(AlexaGadget):
    """
    Class that logs each directive received from the Echo device.
    """

    def __init__(self):
        super().__init__()

        # Color animation states
        self.color = None
        self.interval_ms = 0
        self.iterations = 0
        self.cycle_count = 0
        self.keep_cycling = False
        self.feeder_active = False

        # Setup a lock to be used for avoiding race conditions
        # during color animation state updates
        self.lock = threading.Lock()
        # Setup a separate thread for LED to cycle through colors
        self.led_thread = threading.Thread(target=self._led_blink)
        self.led_thread.start()

    def on_custom_catfeedergadget_blink(self, directive):
        """
        Handles Custom.CatFeederGadget.Blink directive sent from skill
        by triggering LED color cycling animations based on the received parameters
        """
        payload = json.loads(directive.payload.decode("utf-8"))

        self.lock.acquire()
        # Initialize the color animation states based on parameters received from skill
        self.interval_ms = payload['intervalMs']
        self.iterations = payload['iterations']
        self.cycle_count = 0
        self.feeder_active = bool(payload['startFeeder'])
        self.keep_cycling = True
        self.lock.release()

    def on_custom_catfeedergadget_stopblink(self, directive):
        """
        Handles Custom.CatFeederGadget.StopBlink directive sent from skill
        by stopping the LED animations
        """
        logger.info('StopBlink directive received: Turning off LED')

        # Turn off the LED and disable the color animation states to stop the LED cycling animation
        RGB_LED.off()
        self.lock.acquire()
        self.keep_cycling = False
        self.feeder_active = False
        self.lock.release()

    def _led_blink(self):
        """
        Plays the LED cycling animation based on the color animation states
        """
        while True:
            # If cycling animation is still active
            if self.keep_cycling and self.cycle_count < self.iterations:
                self.lock.acquire()
                self.color = 'GREEN'
                self.cycle_count = self.cycle_count + 1
                self.lock.release()

                # Set the color for the LED
                RGB_LED.color = Color(self.color.lower())

                # Display the color for specified interval before switching again
                time.sleep(self.interval_ms/1000)

            # If button is pressed, display the current color for 5 seconds
            elif not self.keep_cycling and self.feeder_active:
                time.sleep(5)
                RGB_LED.off()
                self.lock.acquire()
                self.feeder_active = False
                self.lock.release()
            else:
                RGB_LED.off()
                time.sleep(0.1)

if __name__ == '__main__':
    try:
        CatFeederGadget().main()
    finally:
        RGB_LED.close()
