import gi
import sys
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import socket, os
from command_server import CommandServer

def on_tag(bus, msg):
    taglist = msg.parse_tag()
    print('on_tag:')
    for key, item in taglist.items():
        print('\t{} = {}'.format(key, item))

class InternetRadio():
    def __init__(self, url=None):
        self.url = url
        Gst.init(sys.argv)
        self.state = Gst.State.NULL
        self.player = player = Gst.ElementFactory.make("playbin", "player")
        if not self.player:
            print("ERROR: Could not create playbin.")
            sys.exit(1)

        self.player.connect("audio-tags-changed", self.tags_changed)
        self.player.connect("text-tags-changed", self.tags_changed)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message::error", self.on_error)
        bus.connect("message::eos", self.on_eos)
        bus.connect("message::state-changed", self.on_state_changed)
        bus.connect("message::application", self.on_application_message)
        print(self.player)
        if self.url is not None:
            self.set_url(self.url)
            self.play()

    def set_url(self, url):
        self.url = url
        self.player.set_property('uri', url)

    def play(self):
        #start playing
        ret = self.player.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("ERROR: Unable to start playing")

    def pause(self):
        self.player.set_state(Gst.State.PAUSED)

    def stop(self):
        self.player.set_state(Gst.State.READY)

    def tags_changed(self, playbin, stream):
        print("Tags Changed")
        self.analyze_stream()
        self.player.post_message(Gst.Message.new_application(self.player,
                                                             Gst.Structure.new_empty("tags-changed")))

    def on_error(self, bus, msg):
        print("Error")
        err, dbg = msg.parse_error()
        print(msg.src.get_name(), ":", err.message)
        if dbg:
            print("Debug info", dbg)

    def on_eos(self, bus, msg):
        print("EOS")
        self.player.set_state(Gst.State.READY)

    def on_state_changed(self, bus, msg):
        print("state changed")
        old, new, pending = msg.parse_state_changed()
        if not msg.src == self.player:
            # not from the player, ignore
            return

        self.state = new
        print("State changed from {0} to {1}".format(
            Gst.Element.state_get_name(old), Gst.Element.state_get_name(new)))

    def analyze_stream(self):
        print(Gst.TAG_AUDIO_CODEC)
        print(Gst.TAG_BITRATE)
        print()
        num_streams = self.player.get_property("n-audio")
        self.stream_properties = []
        print("Analysing", num_streams, "audio streams")
        for i in range(num_streams):
            tags = None
            props = dict()
            tags = self.player.emit("get-audio-tags", i)
            print(tags)
            if tags:
                props['num'] = i
                ret, value = tags.get_string(Gst.TAG_AUDIO_CODEC)
                if ret:
                    props['codec'] = value or "unknown"
                ret, value = tags.get_string(Gst.TAG_LANGUAGE_CODE)
                if ret:
                    props['language'] = value or "unknown"
                ret, value = tags.get_uint(Gst.TAG_BITRATE)
                if ret:
                    props['bitrate'] = value or "unknown"
                self.stream_properties.append(props)

        print(self.stream_properties)


    def on_application_message(self, bus, msg):
        print("app_message")
        if msg.get_structure().get_name() == "tags-changed":
            self.analyze_stream()

def setup_socket():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
      os.remove('/tmp/chatter-sock')
    except OSError:
      pass
    s.bind('/tmp/chatter-sock')
    s.listen(1)
    conn, addr = s.accept()
    return socket


#wait and let the music play
def main():
    #our stream to play
    #music_stream_uri = 'http://live-icy.gss.dr.dk/A/A29L.mp3'
    music_stream_uri = 'http://live-icy.gss.dr.dk/A/A29H.mp3'
    print("HELLO!")
    player = InternetRadio(music_stream_uri)
    while True:
        choice = input('(S)top, (P)lay, P(a)use and (Q)uit')
        choice = str(choice)
        if choice.lower() == 's':
            player.stop()
        elif choice.lower() == 'p':
            player.play()
        elif choice.lower() == 'a':
            player.pause()
        elif choice.lower() == 'q':
            exit(0)
        else:
            print("Did not understand command {}".format(choice))

if __name__ == "__main__":
    main()
