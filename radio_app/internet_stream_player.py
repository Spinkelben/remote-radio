import gi
import sys
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import time
import threading
import logging

class InternetStreamPlayer():
    def __init__(self, url=None):
        self.url = url
        Gst.init(sys.argv)
        self.loop = GLib.MainLoop()
        self.state = Gst.State.NULL
        self.player = Gst.ElementFactory.make("playbin", "player")
        if not self.player:
            logging.error("ERROR: Could not create playbin.")
            sys.exit(1)

        self.player.connect("audio-tags-changed", self.tags_changed)
        self.player.connect("text-tags-changed", self.tags_changed)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message::error", self.on_error)
        bus.connect("message::eos", self.on_eos)
        bus.connect("message::state-changed", self.on_state_changed)
        bus.connect("message::application", self.on_application_message)
        bus.connect("message", self.on_message)
        logging.debug(self.player)
        self.stream_properties = {}
        if self.url is not None:
            self.set_url(self.url)
            self.play()

    def __enter__(self):
        logging.debug("Starting event loop...")
        t = threading.Thread(target=self.loop.run)
        t.start()
        logging.info("Started event loop")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info("Stopping event loop")
        self.stop()
        self.loop.quit()

    def set_url(self, url):
        self.url = url
        self.player.set_property('uri', url)
        self.stream_properties = {}
        logging.debug("Setting url to {}".format(self.url))

    def play(self):
        # start playing
        logging.debug("Playing stream")
        ret = self.player.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            logging.error("ERROR: Unable to start playing")

    def pause(self):
        self.player.set_state(Gst.State.PAUSED)

    def stop(self):
        self.player.set_state(Gst.State.READY)

    def tags_changed(self, playbin, stream):
        logging.info("Tags Changed")
        self.analyze_stream()
        self.player.post_message(Gst.Message.new_application(self.player,
                                                             Gst.Structure.new_empty("tags-changed")))

    def on_error(self, bus, msg):
        logging.error("Error")
        err, dbg = msg.parse_error()
        logging.error(msg.src.get_name(), ":", err.message)
        if dbg:
            logging.error("Debug info {}".format(dbg))

    def on_eos(self, bus, msg):
        logging.error("EOS")
        self.player.set_state(Gst.State.READY)

    def on_state_changed(self, bus, msg):
        if not msg.src == self.player:
            # not from the player, ignore
            return
        old, new, pending = msg.parse_state_changed()
        self.state = new
        logging.debug("State changed from {0} to {1}".format(
            Gst.Element.state_get_name(old), Gst.Element.state_get_name(new)))

    def analyze_stream(self):
        logging.debug(Gst.TAG_AUDIO_CODEC)
        logging.debug(Gst.TAG_BITRATE)
        num_streams = self.player.get_property("n-audio")
        logging.info("Analysing {} audio streams".format(num_streams))
        for i in range(num_streams):
            tags = None
            tags = self.player.emit("get-audio-tags", i)
            logging.debug(tags)
            if tags:
                self.stream_properties['num'] = i
                ret, value = tags.get_string(Gst.TAG_AUDIO_CODEC)
                if ret:
                    self.stream_properties['codec'] = value or "unknown"
                ret, value = tags.get_string(Gst.TAG_LANGUAGE_CODE)
                if ret:
                    self.stream_properties['language'] = value or "unknown"
                ret, value = tags.get_uint(Gst.TAG_BITRATE)
                if ret:
                    self.stream_properties['bitrate'] = value or "unknown"

        logging.debug(self.stream_properties)


    def on_application_message(self, bus, msg):
        if msg.get_structure().get_name() == "tags-changed":
            self.analyze_stream()
        #if msg.type = Gst.MessageType.STATE_CHANGED:

    def on_message(self, bus, msg):
        if msg.type == Gst.MessageType.STATE_CHANGED:
            pass
        if msg.type == Gst.MessageType.TAG:
            tags = Gst.Message.parse_tag(msg)
            tag_strings = []
            for i in range(0, tags.n_tags()):
                tag_strings.append(tags.nth_tag_name(i))
            logging.info("TEST: Tag message with {} tags from {}".format(tag_strings, Gst.Object.get_name(msg.src)))
            tags.foreach(self._handle_tag, None)
        else:
            logging.debug("TEST: Message {} from {}".format(msg.type, msg.src))
            #pass

    def _handle_tag(self, tag_list, tag, user_data):
        # tag_value_boolean = tag_list.get_boolean(tag)
        # tag_value_date = tag_list.get_date(tag)
        # tag_value_double = tag_list.get_double(tag)
        tag_value_float = tag_list.get_float(tag)
        tag_value_int = tag_list.get_int(tag)
        # tag_value_pointer = tag_list.get_pointer(tag)
        # tag_value_sample = tag_list.get_sample(tag)
        tag_value_string = tag_list.get_string(tag)
        tag_value_uint = tag_list.get_uint(tag)
        # tag_value_uint64 = tag_list.get_uint64(tag)

        # logging.debug("Tag {} can have values: {}".format(tag, [tag_value_boolean,
        #                                                       tag_value_date,
        #                                                       tag_value_double,
        #                                                       tag_value_float,
        #                                                       tag_value_int,
        #                                                       tag_value_pointer,
        #                                                       tag_value_sample,
        #                                                       tag_value_string,
        #                                                       tag_value_uint,
        #                                                       tag_value_uint64]))
        actual_value = None
        if tag_value_string[0]:
            actual_value = tag_value_string[1]
        elif tag_value_int[0] and tag_value_int[1] != 0:
            actual_value = tag_value_int[1]
        elif tag_value_float[0] and tag_value_float[1] != 0:
            actual_value = tag_value_float[1]
        elif tag_value_uint[0] and tag_value_uint[1] != 0:
            actual_value = tag_value_uint[1]
        self.stream_properties[tag] = actual_value
        logging.debug("Tag: {} has actual value {}".format(tag, actual_value))
