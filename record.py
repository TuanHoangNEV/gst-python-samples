from threading import Thread

import gi
gi.require_version("Gst", "1.0")

import time
from threading import Thread
from gi.repository import Gst, GLib
Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

cmd  = "rtspsrc location=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4 ! rtph264depay ! h264parse ! mp4mux ! filesink location=file.mp4"
#cmd += "uridecodebin uri=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4 ! videoscale ! video/x-raw, width=320, height=240 ! m. "
#cmd += "uridecodebin uri=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4 ! videoscale ! video/x-raw, width=320, height=240 ! m. "
#cmd += "uridecodebin uri=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4 ! videoscale ! video/x-raw, width=320, height=240 ! m. "
#cmd += "uridecodebin uri=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4 ! videoscale ! video/x-raw, width=320, height=240 ! m. "


pipeline = Gst.parse_launch(cmd)
pipeline.set_state(Gst.State.PLAYING)

time.sleep(10)

pipeline.set_sate(Gst.State.NULL)
main_loop.quit()
thread.join()