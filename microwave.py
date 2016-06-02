#!/usr/bin/env python
"""Microwave oven example.

Implemented using pythons Tkinter library for the GUI and the State design
pattern.
"""
import sys
import time
import threading
import traceback
from Tkinter import Tk, Frame, Button, Label, LEFT, Canvas, FALSE

BUTTON_STYLE = {"borderwidth": 2, "font": ('Helvetica', 10, 'bold'),
                "fg": "white", "bg": "black", "activebackground": "green"}


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
        if self.microwave.timer.total != "0000":
            print "Cooking . . ."
            self.microwave.door.itemconfig(
                self.microwave.door.window, fill="yellow")
            self.microwave.set_state(CookingState)
            # No Lock required as 'timer.total' changes happen asynchronously
            self.microwave.timer_thread = threading.Thread(
                target=self.microwave.timer.countdown)
            self.microwave.timer_thread.start()

    def stop(self):
        """Clear timer if stopped and stop is pressed."""
        self.microwave.timer.total = "0000"
        self.microwave.timer.refresh()


class CookingState(State):

    def stop(self):
        self.microwave.set_state(StoppedState)
        print "Stopped"
        self.microwave.door.itemconfig(self.microwave.door.window, fill="grey")


class FrameComponent(Frame):

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
        self.timer_thread = None

    def create(self):
        self.door = Door(self)
        self.timer = Timer(self)
        self.number_pad = NumberPad(self)
        self.controls = Controls(self)

    def set_state(self, state_class):
        self.state = state_class(self)

    def shutdown(self):
        """Stop microwave, and wait for last active thread to terminate"""
        self.controls.stop_oven()
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        self.master.destroy()


class Timer(FrameComponent):

    def __init__(self, master):
        self.total = "0000"
        FrameComponent.__init__(self, master)

    def create(self):
        self.timer_label = Label(
            self, width=8, borderwidth=10, font=('Helvetica', 15, 'bold'),
            bg='black', fg="green")
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
        self.master.controls.stop_oven()

    def validate_timer(self):
        """Correct a max value of '99:99' to '99:59'"""
        if int(self.total) > 9959:
            self.total = "9959"


class NumberPad(FrameComponent):

    def create(self):
        num = 0
        for row in range(4):
            for column in range(3):
                num += 1
                if num in (10, 12):
                    continue  # numberpad doesnt have 10 / 12
                elif num == 11:
                    text = "0"
                else:
                    text = str(num)
                button = NumPadButton(self, text=text, **BUTTON_STYLE)
                button.grid(row=row, column=column)


class NumPadButton(Button):

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["command"] = self.press_num

    def press_num(self):
        microwave = self.master.master
        if isinstance(microwave.state, StoppedState) and \
                microwave.timer.total.startswith("0"):
            microwave.timer.total = microwave.timer.total[1:] + self["text"]
            microwave.timer.refresh()


class Controls(FrameComponent):

    def create(self):
        start = Button(
            self, text="Start", command=self.start_oven, **BUTTON_STYLE)
        start.pack(side=LEFT)
        stop = Button(
            self, text="Stop / Clear", command=self.stop_oven, **BUTTON_STYLE)
        stop.pack(side=LEFT)

    def start_oven(self):
        self.master.state.start()

    def stop_oven(self):
        self.master.state.stop()


class Door(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master, height=222, width=400, bg="black")
        self.create()
        self.pack(side=LEFT)

    def create(self):
        # (x0, y0), (x1, y1) => top left & top right coords (returns shape id)
        self.window = self.create_rectangle((50, 50), (350, 175), fill="grey")


if __name__ == "__main__":
    top = Tk()
    top.title('Microwave')
    top.resizable(width=FALSE, height=FALSE)
    microwave = None

    try:
        microwave = Microwave(top)
        top.protocol("WM_DELETE_WINDOW", microwave.shutdown)
        top.mainloop()
    except BaseException as exception:
        if microwave:
            microwave.shutdown()
        traceback.print_exc()
        sys.exit(1)
