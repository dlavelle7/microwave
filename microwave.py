#!/usr/bin/env python
"""Simple example of a microwave ovens control panel.

Implemented using the Tkinter library for the GUI and combining the State and
Composite design patterns.
"""
import sys
import time
import traceback
import threading
from Tkinter import Tk, Frame, Button, Label, LEFT

# TODO: Open door state

class State(object):
    """Base class for State pattern."""

    def __init__(self, microwave):
        self.microwave = microwave

    def start(self):
        pass

    def stop(self):
        pass


class StoppedState(State):

    def start(self):
        if self.microwave.timer.secs:
            print "Cooking . . ."
            self.microwave.set_state(CookingState(self.microwave))
            thread = threading.Thread(target=self.microwave.timer.countdown)
            thread.start()

    def stop(self):
        """Clear timer if stopped and stop is pressed."""
        self.microwave.timer.secs = 0
        self.microwave.timer.refresh()


class CookingState(State):

    def stop(self):
        self.microwave.set_state(StoppedState(self.microwave))
        print "Stopped"

# TODO: Door Graphic (black -> stopped, yellow -> cooking

class FrameComponent(Frame):
    """Base class for Composite pattern."""

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

# TODO: Convert seconds to formatted minutes

class Timer(FrameComponent):

    def __init__(self, master):
        self.secs = 0
        FrameComponent.__init__(self, master)

    def create(self):
        self.timer_label = Label(self, borderwidth=10)
        self.refresh()
        self.timer_label.pack()

    def refresh(self):
        self.timer_label["text"] = str(self.secs)

    def countdown(self):
        while self.secs > 0 and not isinstance(self.master.state, StoppedState):
            self.secs -= 1
            self.refresh()
            time.sleep(1)

        if self.secs == 0:
            print 'Ping!'

        self.master.set_state(StoppedState(self.master))


class NumberPad(FrameComponent):

    def create(self):
        num = 0
        for r in range(4):
            for c in range(3):
                num += 1
                if num in (10, 12):
                    pass  # numberpad doesnt have 10 / 12
                elif num == 11:
                    NumPadButton(self, text="0",
                        borderwidth=2).grid(row=r,column=c)
                else:
                    NumPadButton(self, text=str(num),
                        borderwidth=2).grid(row=r,column=c)


class NumPadButton(Button):

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["command"] = self.press_num

    def press_num(self):
        microwave = self.master.master
        if isinstance(microwave.state, StoppedState):
            microwave.timer.secs = int(str(microwave.timer.secs) + self["text"])
            microwave.timer.refresh()


class Controls(FrameComponent):

    def create(self):
        start = Button(self, text="Start", command=self.start_oven)
        start.pack(side=LEFT)
        stop = Button(self, text="Stop", command=self.stop_oven)
        stop.pack(side=LEFT)

    def start_oven(self):
        self.master.state.start()

    def stop_oven(self):
        self.master.state.stop()


def main():
    top = Tk()
    top.title('Microwave')
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
