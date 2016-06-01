import unittest
import microwave
from mock import Mock, patch, call

class MockWidget:
    """Old style class to mock base class Tkinter widgets."""

    def __init__(self, *args, **kwargs):
        self.master = args[0]
        self.config = dict()
        for name, value in kwargs.iteritems():
            self.__setitem__(name, value)

    def __setitem__(self, name, value):
        self.config[name] = value

    def __getitem__(self, name):
        return self.config[name]

    def grid(self, *args, **kwargs):
        pass

    def pack(self, *args, **kwargs):
        pass

    def next(self):
        return Mock()

    def create_rectangle(self, *args, **kwargs):
        pass

    def itemconfig(self, *args, **kwargs):
        pass


class TestMicrowave(unittest.TestCase):

    def setUp(self):
        microwave.threading = Mock()

    @patch('microwave.Canvas', MockWidget)
    @patch('microwave.Frame', MockWidget)
    @patch('microwave.Label', MockWidget)
    @patch('microwave.Button', MockWidget)
    @patch('microwave.time.sleep', Mock())
    def test_states(self):
        # Mock Tkinter.Frame & Tkinter.Button base classes
        microwave.FrameComponent.__bases__ = (MockWidget,)
        microwave.NumPadButton.__bases__ = (MockWidget,)
        microwave.Door.__bases__ = (MockWidget,)
        # Create microwave instance
        micro = microwave.Microwave(Mock())
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        self.assertEquals('0000', micro.timer.total)
        # Stopped -> stop() = Stopped & resets total
        micro.timer.total = '1234'
        micro.state.stop()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        self.assertEquals('0000', micro.timer.total)
        # Stopped -> start() & no total = Stopped
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))
        # Stopped -> start() with total = Cooking
        micro.timer.total = '1234'
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.CookingState))
        # Cooking -> start() = Cooking
        micro.set_state(microwave.CookingState)
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.CookingState))
        # Cooking -> stop() = Stoped
        micro.set_state(microwave.CookingState)
        micro.state.stop()
        self.assertTrue(isinstance(micro.state, microwave.StoppedState))

    @patch('microwave.Frame', MockWidget)
    @patch('microwave.Label', MockWidget)
    @patch('microwave.time.sleep')
    def test_countdown(self, mock_sleep):
        microwave.FrameComponent.__bases__ = (MockWidget,)
        timer = microwave.Timer(Mock())
        # When created total is "0000" and label is "00:00"
        self.assertEqual("0000", timer.total)
        self.assertEqual("00:00", timer.timer_label["text"])

        # Timer set to 5secs -> sleep called 5 times, pings and sets stopped
        timer.total = "0005"
        timer.countdown()
        self.assertEqual(5, mock_sleep.call_count)
        self.assertEqual(timer.total, "0000")
        self.assertEqual(timer.timer_label["text"], "00:00")
        self.assertEqual(1, timer.master.controls.stop_oven.call_count)

        # Countdown stopped after 1 sec -> timer keeps this value
        mock_sleep.reset_mock()
        timer.master.controls.stop_oven.reset_mock()
        def stop_countdown(secs):
            """Mimic user stopping microwave during countdown."""
            if mock_sleep.called:
                timer.master.state = microwave.StoppedState(Mock())
        mock_sleep.side_effect = stop_countdown
        timer.total = "1234"
        timer.countdown()
        self.assertEqual(timer.total, "1233")
        self.assertEqual(timer.timer_label["text"], "12:33")
        self.assertFalse(timer.master.controls.stop_oven.called)

        # Corrects user entered secs e.g: "00:90" -> "01:30"
        mock_sleep.reset_mock()
        timer.master.state = Mock()
        timer.total = "0091"
        timer.countdown()  # stops after one sleep
        self.assertEqual(timer.total, "0130")
        self.assertEqual(timer.timer_label["text"], "01:30")

    @patch('microwave.Frame', MockWidget)
    @patch('microwave.Label', MockWidget)
    @patch('microwave.time.sleep')
    def test_validate_timer(self, mock_sleep):
        microwave.FrameComponent.__bases__ = (MockWidget,)
        timer = microwave.Timer(Mock())
        # When total is set to above '9959' corrects to '9959'
        timer.total = "9960"
        timer.validate_timer()
        self.assertEqual("9959", timer.total)
        # When total is below '9959' total is unchanged
        timer.total = "9958"
        timer.validate_timer()
        self.assertEqual("9958", timer.total)

    @patch('microwave.Button', MockWidget)
    def test_num_pad_button(self):
        microwave.NumPadButton.__bases__ = (MockWidget,)
        timer = Mock(total="0000")
        micro = Mock(timer=timer)
        number_pad = Mock(master=micro)
        # Cooking state & press_num() => No time change
        micro.state = microwave.CookingState(micro)
        button9 = microwave.NumPadButton(number_pad, text="9")
        button9["command"]()
        self.assertEqual("0000", button9.master.master.timer.total)
        # Stopped state, timer == '0000' & press_num() '9' => timer == '0009'
        micro.state = microwave.StoppedState(micro)
        button9["command"]()
        self.assertEqual("0009", button9.master.master.timer.total)
        # Stopped state, timer == '0009' & press_num() '8' => timer == '0098'
        button8 = microwave.NumPadButton(number_pad, text="8")
        button8["command"]()
        self.assertEqual("0098", button8.master.master.timer.total)
        # Stopped state, timer == '0098' & press_num() '7' => timer == '0987'
        button7 = microwave.NumPadButton(number_pad, text="7")
        button7["command"]()
        self.assertEqual("0987", button7.master.master.timer.total)
        # Stopped state, timer == '0987' & press_num() '6' => timer == '9876'
        button6 = microwave.NumPadButton(number_pad, text="6")
        button6["command"]()
        self.assertEqual("9876", button6.master.master.timer.total)
        # Stopped state, timer == '9876' & press_num() '5' => No time change
        button5 = microwave.NumPadButton(number_pad, text="5")
        button5["command"]()
        self.assertEqual("9876", button5.master.master.timer.total)
