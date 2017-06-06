import gi
import sys
gi.require_version("Gtk", "3.0")
from gi.repository import Gst

def on_tag(bus, msg):
    taglist = msg.parse_tag()
    print('on_tag:')
    for key, item in taglist.items():
        print('\t{} = {}'.format(key, item))

#our stream to play
music_stream_uri = 'http://live-icy.gss.dr.dk/A/A29L.mp3'

Gst.init(None)

#creates a playbin (plays media form an uri)
player = Gst.ElementFactory.make("playbin", "player")
if not player:
    print("ERROR: Could not create playbin.")
    sys.exit(1)

#set the uri
player.set_property('uri', music_stream_uri)

#start playing
player.set_state(Gst.State.PLAYING)

#listen for tags on the message bus; tag event might be called more than once
bus = player.get_bus()
bus.enable_sync_message_emission()
bus.add_signal_watch()
bus.connect('message::tag', on_tag)



def new_uri(uri):
    player.set_state(Gst.State.NULL)
    player.set_property('uri', uri)
    player.set_state(Gst.State.PLAYING)


#wait and let the music play

while True:
    choice = str(input('(S)top, (P)lay, P(a)use and (Q)uit'))
    if choice.lower() == 's':
        next_state = Gst.State.NULL
    elif choice.lower() == 'p':
        next_state = Gst.State.PLAYING
    elif choice.lower() == 'a':
        next_state = Gst.State.PAUSED
    elif choice.lower() == 'q':
        exit(0)
    else:
        print("Did not understand command {}".format(choice))
    player.set_state(next_state)
