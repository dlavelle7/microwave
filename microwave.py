#!/usr/bin/env python
import sys
import time
import traceback
import threading
from Tkinter import *
from collections import deque


# TODO: Refine Composite and State patterns
# TODO: OpenState


class State(object):

    def __init__(self, microwave):
        self.microwave = microwave

    def start(self):
        pass

    def stop(self):
        pass


class StoppedState(State):

    def start(self):
        print "Cooking . . ."
        self.microwave.set_state(CookingState(self.microwave))
        thread = threading.Thread(target=self.microwave.timer.countdown)
        thread.start()


    def stop(self):
        """Clear timer if stopped and stop is pressed."""
        self.microwave.timer.time.clear()
        self.microwave.timer.refresh()


class CookingState(State):

    def stop(self):
        print "Stopped"
        self.microwave.set_state(StoppedState(self.microwave))


class FrameComponent(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.create()
        self.pack()

    def create(self):
        pass


class Microwave(FrameComponent):

    def __init__(self, master):
        FrameComponent.__init__(self, master)
        self.state = StoppedState(self)

    def create(self):
        self.timer = Timer(self)
        self.number_pad = NumberPad(self)
        self.controls = Controls(self)

    def set_state(self, state):
        self.state = state


class Timer(FrameComponent):

    def __init__(self, master):
        self.time = deque(maxlen=4)
        FrameComponent.__init__(self, master)

    def create(self):
        self.timer_label = Label(self, borderwidth=10)
        self.refresh()
        self.timer_label.pack()

    def refresh(self):
        self.timer_label["text"] = "".join(self.time)

    def countdown(self):
        if self.timer_label["text"]:
            secs = int(self.timer_label["text"])
            while secs > 0:
                time.sleep(1)
                secs -= 1
                self.timer_label["text"] = str(secs)
            print 'Ping!'
            self.time.clear()


class NumberPad(FrameComponent):

    def create(self):
        num = 0
        for r in range(4):
            for c in range(3):
                num += 1
                if num in (10, 12):
                    Button(self).grid_forget()
                elif num == 11:
                    NumPadButton(self, text="0",
                        borderwidth=2).grid(row=r,column=c)
                else:
                    NumPadButton(self, text="{0}".format(num),
                        borderwidth=2).grid(row=r,column=c)


class NumPadButton(Button):

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["command"] = self.press_num

    def press_num(self):
        self.master.master.timer.time.append(self["text"])
        self.master.master.timer.refresh()


class Controls(FrameComponent):

    def create(self):
        self.start = Button(self, text="Start",
                command=self.start_oven)
        self.start.pack(side=LEFT)
        self.stop = Button(self, text="Stop",
                command=self.stop_oven)
        self.stop.pack(side=LEFT)

    def start_oven(self):
        self.master.state.start()

    def stop_oven(self):
        self.master.state.stop()


def main():
    top = Tk()
    Microwave(top)
    top.mainloop()


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
