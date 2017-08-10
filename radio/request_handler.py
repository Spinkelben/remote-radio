from message_pb2 import Request, Response

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
        request = Request()
        request.ParseFromString(message)
        self._action_map[request.type](request)

    def _play(self, request):
        self.radio.play()

    def _pause(self, request):
        self.radio.pause()

    def _stop(self, request):
        self._stop()

    def _set_channel(self, request):
        self.radio.set_url(request.channel)

    def _get_info(self, request):
        pass
