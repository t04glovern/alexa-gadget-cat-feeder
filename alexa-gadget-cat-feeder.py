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
        self._open_feeder(open_feeder=True)

        # Sending the "feed" status back to the Alexa skill
        payload = {'feed': True}
        self.send_custom_event(
            'Custom.CatFeederGadget', 'ReportFeeder', payload)

    def _reset_feeder(self):
        self._open_feeder(open_feeder=False)

    def _open_feeder(self, open_feeder):
        SERVO.start(0)
        if open_feeder:
            # PWM Signal to open the servo
            SERVO.ChangeDutyCycle(30)
        else:
            # PWM Signal to close the servo
            SERVO.ChangeDutyCycle(15)

if __name__ == '__main__':
    try:
        CatFeederGadget().main()
    finally:
        logger.debug('Cleaning up')
        IO.cleanup()
