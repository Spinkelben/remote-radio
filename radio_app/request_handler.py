from message_pb2 import Request, Response
import logging
import json
from gi.repository import Gst

class RequestHandler():

    def __init__(self, radio):
        self._action_map = {
            Request.PLAY: self._play,
            Request.PAUSE: self._pause,
            Request.STOP: self._stop,
            Request.SET_CHANNEL: self._set_channel,
            Request.INFO: self._get_info,
        }
        self.radio = radio

    def on_message(self, message):
        logging.debug("Reading request")
        request = Request()
        request.ParseFromString(message)
        logging.debug("Request type {}".format(request.type))
        response = self._action_map[request.type](request)
        logging.debug("Sending response")
        return response.SerializeToString()

    def _play(self, request):
        self.radio.play()
        return self._create_response(request)

    def _pause(self, request):
        self.radio.pause()
        return self._create_response(request)

    def _stop(self, request):
        self.radio.stop()
        return self._create_response(request)

    def _set_channel(self, request):
        self.radio.stop()
        self.radio.set_url(request.channel)
        self.radio.play()
        return self._create_response(request)

    def _get_info(self, request):
        props = dict(self.radio.stream_properties)
        response = self._create_response(request)
        logging.info("Radio state is: {}".format(self.radio.state))
        if self.radio.state != Gst.State.PLAYING:
            return response
        logging.info(props)
        response.bitrate = props.pop('nominal-bitrate', 0)
        response.codec = props.pop('codec', "")
        response.name = props.pop('organization', "")
        response.title = props.pop('title', "")
        response.location = props.pop('location', "")
        response.stereo = "stereo" in  props.pop('channel-mode', "")
        response.extra = json.dumps(props)
        return response


    def _create_response(self, request):
        response = Response()
        response.success = True
        return response
