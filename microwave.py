#!/usr/bin/env python
import sys
import traceback
from Tkinter import *
from collections import deque


# TODO: Refine Composite and State patterns
# TODO: OpenState


class State(object):

    def __init__(self, microwave):
        self.microwave = microwave

    def start_stop(self):
        pass


class StoppedState(State):

    def start(self):
        print "Cooking . . ."
        self.microwave.set_state(CookingState(self.microwave))


class CookingState(State):

    def stop(self):
        print "Stopped"
        self.microwave.set_state(StoppedState(self.microwave))


class OpenState(State):
    pass


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
        self._timer = deque(maxlen=4)
        FrameComponent.__init__(self, master)

    def create(self):
        self.timer = Label(self, borderwidth=10)
        self.refresh()
        self.timer.pack()

    def refresh(self):
        self.timer["text"] = "".join(self._timer)


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
                        borderwidth=1 ).grid(row=r,column=c)
                else:
                    NumPadButton(self, text="{0}".format(num),
                        borderwidth=1 ).grid(row=r,column=c)


class NumPadButton(Button):

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["command"] = self.press_num

    def press_num(self):
        self.master.master.timer._timer.append(self["text"])
        self.master.master.timer.refresh()


class Controls(FrameComponent):

    def create(self):
        self.start = Button(self, text="Start",
                command=self.master.state.start)
        self.start.pack()

        self.stop = Button(self, text="Stop",
                command=self.master.state.stop)
        self.stop.pack()


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
