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

# TODO: Open door state?

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
        # TODO: Isn't this another state (StoppedWithTime)
        if self.microwave.timer.total != "0000":
            print "Cooking . . ."
            self.microwave.set_state(CookingState(self.microwave))
            thread = threading.Thread(target=self.microwave.timer.countdown)
            thread.start()  # FIXME: call this threads join() from main thread?

    def stop(self):
        """Clear timer if stopped and stop is pressed."""
        self.microwave.timer.total = "0000"
        self.microwave.timer.refresh()


class CookingState(State):

    def stop(self):
        self.microwave.set_state(StoppedState(self.microwave))
        print "Stopped"

# TODO: Door Graphic (black -> stopped, yellow -> cooking

class FrameComponent(Frame):
    """Base class for Composite pattern."""

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
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
        self.total = "0000"
        FrameComponent.__init__(self, master)

    def create(self):
        self.timer_label = Label(self, width=8, borderwidth=10, font=('arial', 15, 'bold'), bg='black', fg="green")
        self.refresh()
        self.timer_label.pack()

    def refresh(self):
        self.timer_label["text"] = self.total[:2] + ":" + self.total[2:]

    def countdown(self):
        self.validate_timer()
        mins = int(self.total[:2])
        secs = int(self.total[2:])
        total_secs = mins * 60 + secs
        while total_secs > 0:
            if isinstance(self.master.state, StoppedState):
                return
            total_secs -= 1
            new_mins, new_secs = divmod(total_secs, 60)
            self.total = "{:02d}{:02d}".format(new_mins, new_secs)
            self.refresh()
            time.sleep(1)

        print 'Ping!'
        self.master.set_state(StoppedState(self.master))

    def validate_timer(self):
        """Correct a max value of '99:99' to '99:59'"""
        if int(self.total) > 9959:
            self.total = "9959"


class NumberPad(FrameComponent):

    def create(self):
        num = 0
        for r in range(4):
            for c in range(3):
                num += 1
                if num in (10, 12):
                    continue  # numberpad doesnt have 10 / 12
                elif num == 11:
                    text = "0"
                else:
                    text=str(num)
                NumPadButton(self, text=text, font=('arial', 10, 'normal'), fg="white", bg="black",
                    borderwidth=2, activebackground="green").grid(row=r,column=c)


class NumPadButton(Button):

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["command"] = self.press_num

    def press_num(self):
        microwave = self.master.master
        if isinstance(microwave.state, StoppedState):
            if microwave.timer.total.startswith("0"):
                microwave.timer.total = microwave.timer.total[1:] + self["text"]
                microwave.timer.refresh()


class Controls(FrameComponent):

    def create(self):
        start = Button(self, text="Start", borderwidth=2,
                command=self.start_oven, font=('arial', 10, 'normal'), fg="white", bg="black",
                    activebackground="green")
        start.pack(side=LEFT)
        stop = Button(self, text="Stop / Clear", borderwidth=2,
                command=self.stop_oven, font=('arial', 10, 'normal'), fg="white", bg="black",
                    activebackground="green")
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
