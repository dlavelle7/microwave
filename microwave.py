#!/usr/bin/env python
import sys
import traceback
from Tkinter import *


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
#        # Timer / Clock
#        # Number pad
        num = 0
        for r in range(4):
            for c in range(3):
                num += 1
                if num in (10, 12):
                    Button(self).grid_forget()
                elif num == 11:
                    Button(self, text="0",
                        borderwidth=1 ).grid(row=r,column=c)
                else:
                    Button(self, text="{0}".format(num),
                        borderwidth=1 ).grid(row=r,column=c)


        # Controls
#        self.start = Button(self)
#        self.start["text"] = "Start"
#        self.start["command"] = self.start_oven
#        self.start.pack(side=LEFT)
#
#        self.stop = Button(self)
#        self.stop["text"] = "Stop"
#        self.stop["command"] = self.stop_oven
#        self.stop.pack(side=LEFT)
#
#        self._open = Button(self)
#        self._open["text"] = "Open"
#        self._open["command"] = self.open_oven
#        self._open.pack(side=LEFT)

    def start_oven(self):
        print "Start . . ."

    def stop_oven(self):
        print "Stop . . ."

    def open_oven(self):
        print "Open . . ."


def main():
    top = Tk()
    app = Application(master=top)
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print 'Keyboard Interrupt, exiting . . .'
        sys.exit(1)
    except Exception as e:
        traceback.print_exc()
        print 'Something went wrong, exiting . . .'
        sys.exit(1)
