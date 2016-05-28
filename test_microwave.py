import unittest
import microwave
from mock import Mock, patch

class MockWidget:
    """Old style class to mock base class Tkinter widgets."""

    def __init__(self, *args, **kwargs):
        self.master = args[0]
        self.config = dict()

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


class TestMicrowave(unittest.TestCase):

    def setUp(self):
        microwave.threading = Mock()
        microwave.time = Mock()

    def tearDown(self):
        pass

    @patch('microwave.Frame', MockWidget)
    @patch('microwave.Label', MockWidget)
    @patch('microwave.Button', MockWidget)
    def test_states(self):
        # Mock Tkinter.Frame & Tkinter.Button base classes
        microwave.FrameComponent.__bases__ = (MockWidget,)
        microwave.NumPadButton.__bases__ = (MockWidget,)
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
        # TODO: Cooking -> start() = Cooking
        micro.set_state(microwave.CookingState(micro))
        micro.state.start()
        self.assertTrue(isinstance(micro.state, microwave.CookingState))
        # TODO: Cooking -> stop() = Stoped
        micro.set_state(microwave.CookingState(micro))
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
