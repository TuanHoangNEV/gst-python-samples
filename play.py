import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk, GstVideo

rtpsUrl = [
        "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
        "rtsp://rtsp.stream/pattern",
        "rtsp://rtsp.stream/pattern",
        "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
        "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
        "rtsp://rtsp.stream/pattern",
        "rtsp://rtsp.stream/pattern",
        "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4",
    ]

class GTK_Main:
    def __init__(this):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("RTSP Player")
        window.set_default_size(500, 400)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        this.movie_window = Gtk.DrawingArea()
        vbox.add(this.movie_window)
        hbox = Gtk.HBox()
        vbox.pack_start(hbox, False, False, 0)
        hbox.set_border_width(10)
        hbox.pack_start(Gtk.Label(), False, False, 0)
        this.button = Gtk.Button("Start")
        this.button.connect("clicked", this.start_stop)
        hbox.pack_start(this.button, False, False, 0)
        this.button2 = Gtk.Button("Quit")
        this.button2.connect("clicked", this.exit)
        hbox.pack_start(this.button2, False, False, 0)
        this.button3 = Gtk.Button("Record")
        this.button3.connect("clicked", this.recording)
        hbox.pack_start(this.button3, False, False, 0)
        hbox.add(Gtk.Label())
        window.show_all()

        # Set up the gstreamer pipeline
        this.recordPipelines = []
        streamCmd = 'compositor name=comp'
        for index, val in enumerate(rtpsUrl):
            streamCmd += ' sink_'+ str(index) + '::xpos=' + str(320*index) + ' sink_'+ str(index) + '::ypos=0 sink_'+ str(index) + '::width=320 sink_'+ str(index) + '::height=240'
            recordCmd = Gst.parse_launch ('rtspsrc location="' + val + '" ! application/x-rtp, media=video, encoding-name=H264  ! queue ! rtph264depay ! h264parse ! matroskamux ! filesink location=output' + str(index) + '.mkv')
            #this.recordPipelines.append(recordCmd)
            recordCmd.set_state(Gst.State.PLAYING)

        streamCmd += ' ! decodebin ! videoconvert ! autovideosink'
        for index, val in enumerate(rtpsUrl):
            streamCmd += ' rtspsrc location="' + val + '" ! rtph264depay ! avdec_h264 ! queue2 ! comp.sink_' + str(index)

        this.player = Gst.parse_launch (streamCmd)
        bus = this.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", this.on_message)
        bus.connect("sync-message::element", this.on_sync_message)

    def start_stop(this, w):
        if this.button.get_label() == "Start":
            this.button.set_label("Stop")
            this.player.set_state(Gst.State.PLAYING)
        else:
            this.player.set_state(Gst.State.NULL)
            this.button.set_label("Start")

    def exit(this, widget, data=None):
        Gtk.main_quit()

    def recording(this, w):
        if this.button3.get_label() == "Record":
            this.button3.set_label("Stop")
            #for x in this.recordPipelines:
                #x.set_state(Gst.State.PLAYING)
        else:
            this.button3.set_label("Record")
            #for x in this.recordPipelines:
                #x.set_state(Gst.State.NULL)

    def on_message(this, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            this.player.set_state(Gst.State.NULL)
            this.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print ("Error: %s" % err, debug)
            this.player.set_state(Gst.State.NULL)
            this.button.set_label("Start")

    def on_sync_message(this, bus, message):
        struct = message.get_structure()
        if not struct:
            return
        message_name = struct.get_name()
        if message_name == "prepare-window-handle":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            imagesink.set_window_handle(this.movie_window.get_property('window').get_xid())

Gst.init(None)
GTK_Main()
GObject.threads_init()
Gtk.main()