import logging
import sys

from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('agt.alexa_gadget').setLevel(logging.DEBUG)

class AnnotatedGadgetGadget(AlexaGadget):
    """
    Class that logs each directive received from the Echo device.
    """

    def on_connected(self, device_addr):
        # XX:XX:XX:XX:XX:XX
        """
        Gadget connected to the paired Echo device.

        :param device_addr: the address of the device we connected to
        """
        pass

    def on_disconnected(self, device_addr):
        # XX:XX:XX:XX:XX:XX
        """
        Gadget disconnected from the paired Echo device.

        :param device_addr: the address of the device we disconnected from
        """
        pass

    def on_alexa_gadget_statelistener_stateupdate(self, directive):
        # header {
        #   namespace: "Alexa.Gadget.StateListener"
        #   name: "StateUpdate"
        # }
        # payload {
        #   states {
        #     name: "timeinfo"
        #     value: "2020-01-12T20:35:05+08:00"
        #   }
        # }
        """
        Alexa.Gadget.StateListener StateUpdate directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alexa-gadget-statelistener-interface.html#StateUpdate-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass

    def on_notifications_setindicator(self, directive):
        # header {
        #   namespace: "Notifications",
        #   name: "SetIndicator"
        # }
        # payload {
        #   playAudioIndicator: True,
        #   asset: {},
        #   persistVisualIndicator: True
        # }
        """
        Notifications SetIndicator directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/notifications-interface.html#SetIndicator-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass

    def on_notifications_clearindicator(self, directive):
        # header {
        #   namespace: "Notifications"
        #   name: "ClearIndicator"
        # }
        # payload {
        # }
        """
        Notifications ClearIndicator directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/notifications-interface.html#ClearIndicator-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass

    def on_alexa_gadget_speechdata_speechmarks(self, directive):
        # header {
        #   namespace: "Alexa.Gadget.SpeechData"
        #   name: "Speechmarks"
        # }
        # payload {
        #   speechmarksData {
        #     value: "k"
        #     type: "VISEME"
        #     startOffsetInMilliSeconds: 6
        #   }
        # }

        """
        Alexa.Gadget.SpeechData Speechmarks directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alexa-gadget-speechdata-interface.html#Speechmarks-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass

    def on_alexa_gadget_musicdata_tempo(self, directive):
        # header {
        #   namespace: "Alexa.Gadget.MusicData",
        #   name: "Tempo"
        # }
        # payload {
        #   playerOffsetInMilliSeconds: 681
        #   tempoData: [
        #     { value: 118 }
        #   ]
        # }
        """
        Alexa.Gadget.MusicData Tempo directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alexa-gadget-musicdata-interface.html#Tempo-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass

    def on_alerts_setalert(self, directive):
        # header {
        #   namespace: "Alerts"
        #   name: "SetAlert"
        # }
        # payload {
        #   token: "3725511653"
        #   type: "TIMER"
        #   scheduledTime: "2020-01-12T20:31:42+08:00"
        # }
        """
        Alerts SetAlert directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alerts-interface.html#SetAlert-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass

    def on_alerts_deletealert(self, directive):
        # header {
        #   namespace: "Alerts"
        #   name: "DeleteAlert"
        # }
        # payload {
        #   token: "3725511653"
        # }
        """
        Alerts DeleteAlert directive received.

        For more info, visit:
            https://developer.amazon.com/docs/alexa-gadgets-toolkit/alerts-interface.html#DeleteAlert-directive

        :param directive: Protocol Buffer Message that was send by Echo device.
        """
        pass


if __name__ == '__main__':
    AnnotatedGadgetGadget().main()
