import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def main(args):
    if len(args) != 2:
        sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
        sys.exit(1)

    GObject.threads_init()
    Gst.init(None)

    playbin = Gst.ElementFactory.make("playbin", None)
    if not playbin:
        sys.stderr.write("'playbin' gstreamer plugin missing\n")
        sys.exit(1)

    if Gst.uri_is_valid(args[1]):
      uri = args[1]
    else:
      uri = Gst.filename_to_uri(args[1])
    playbin.set_property('uri', uri)

    loop = GObject.MainLoop()

    bus = playbin.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)
    
    playbin.set_state(Gst.State.PLAYING)
    try:
      loop.run()
    except:
      pass
    
    playbin.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))