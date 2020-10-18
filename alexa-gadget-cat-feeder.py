import RPi.GPIO as IO
import json
import logging
import sys
import threading
import time

from agt import AlexaGadget

IO.setmode(IO.BCM)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('agt.alexa_gadget').setLevel(logging.DEBUG)

# GPIO pins
GPIO_SERVO_PIN = 18

IO.setup(GPIO_SERVO_PIN,IO.OUT)
SERVO = IO.PWM(GPIO_SERVO_PIN,100)

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

    def on_custom_catfeedergadget_cleanup(self, directive):
        """
        Handles Custom.CatFeederGadget.Cleanup directive sent from skill
        """
        self._reset_feeder()

    def on_custom_catfeedergadget_feedcat(self, directive):
        """
        Handles Custom.CatFeederGadget.FeedCat directive sent from skill
        """
        SERVO.start(0)
        SERVO.ChangeDutyCycle(30)
        time.sleep(0.5)

        payload = {'feed': True}
        self.send_custom_event(
            'Custom.CatFeederGadget', 'ReportFeeder', payload)

    def _reset_feeder(self):
        SERVO.start(0)
        SERVO.ChangeDutyCycle(15)
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        CatFeederGadget().main()
    finally:
        logger.debug('Cleaning up')
