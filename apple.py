from Foundation import NSObject
from AppKit import NSSpeechRecognizer, NSApp, NSApplication, NSRunLoop, NSEventTrackingRunLoopMode
from PyObjCTools import AppHelper

class Listener(NSObject):
    def heardit_(self, notification):
        print("Heard:", notification.userInfo()["NSSpeechRecognizerResult"])

recog = NSSpeechRecognizer.alloc().init()
recog.setCommands_(["start", "stop", "quit"])
recog.setListensInForegroundOnly_(False)

listener = Listener.alloc().init()
recog.setDelegate_(listener)

recog.startListening()

AppHelper.runConsoleEventLoop()